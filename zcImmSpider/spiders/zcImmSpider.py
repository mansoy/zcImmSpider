import scrapy
import arrow
import json
import requests
from scrapy.http import Request
from scrapy.selector import Selector
from ..db.MySqlItems import LSItem
from ..db.MySqlItems import MatchDataItem
from ..db.MySqlItems import RqOddsItem
from ..db.MySqlItems import BfOddsItem
from ..db.MySqlItems import OuOddsItem
from ..db.MySqlItems import YaOddsItem
from ..db.MySqlItems import SizeOddsItem
from ..db.MySqlItems import YaOddsDetailItem
from ..db.MySqlItems import SizeOddsDetailItem
from ..comm import funs
from .. import config as cf


class zcImmSpider(scrapy.Spider):
    name = 'zcImmSpider'
    allowed_domains = ['500.com']
    # start_urls = ['http://liansai.500.com/']

    def __init__(self, params=None, *args, **kwargs):
        super(zcImmSpider, self).__init__(*args, **kwargs)
        self.params = json.loads(params)

    def start_requests(self):
        try:
            self.wtype = self.params['wtype']
            if self.wtype == cf.WT_WORLDCUP:
                url = 'http://www.500.com/worldcup/ajax.php?act=getallmatch'
                yield Request(url=url, callback=self.parseWorldcup)
            elif self.wtype == cf.WT_HISTORY:
                sDate = arrow.get(self.params['startDate'])
                eData = arrow.get(self.params['endDate'])
                for day in arrow.Arrow.range('day', sDate, eData.shift(days=-1)):
                    ssdate = day.format('YYYY-MM-DD')
                    url = 'http://trade.500.com/jczq/?date={0}'.format(ssdate)
                    yield Request(url, self.parseHistory, meta={'year': ssdate[4:], 'date': ssdate, 'ou': self.params['ou'], 'ya': self.params['ya'], 'dx': self.params['dx'], 'rq': self.params['rq'], 'bf': self.params['bf']})
            elif self.wtype == cf.WT_LIANSAI:
                url = 'http://liansai.500.com/'
                yield Request(url=url, callback=self.parseLsscore)
            elif self.wtype == cf.WT_OUGUAN or self.wtype == cf.WT_OUCUP:
                url = 'http://liansai.500.com/'
                yield Request(url, self.parseCupMatch, meta={'lsName': self.params['lsName']})
        except Exception as e:
            print(e)

    # 获取赛季名称
    def getSeason(self, data):
        try:
            url = Selector(text=data).xpath('//span[@class="league"]/a/@href').extract()[0]
            response = requests.get(url)
            ret = Selector(text=response.text).xpath('//div[@class="ldrop_bd"]//li[@class="ldrop_list_on"]/a/text()').extract()[0]
            return ret
        except Exception as e:
            print(e)
            return ''

    def parseHistory(self, response):
        datas = Selector(response).xpath('//tr[@isend="1" or @isend="0"]').extract()
        for data in datas:
            try:
                st = Selector(text=data)
                item = MatchDataItem()
                item['mMid'] = st.xpath('//tr/@fid').extract()[0]
                item['mlsName'] = st.xpath('//tr/@lg').extract()[0].replace(' ', '').replace('　', '')
                item['mSsName'] = self.getSeason(data)
                item['mMtName'] = st.xpath('//td[@class="left_team"]/a/text()').extract()[0].replace(' ', '')
                item['mMtFName'] = st.xpath('//td[@class="left_team"]/a/@title').extract()[0].replace(' ', '')
                item['mDtName'] = st.xpath('//td[@class="right_team"]/a/text()').extract()[0].replace(' ', '')
                item['mDtFName'] = st.xpath('//td[@class="right_team"]/a/@title').extract()[0].replace(' ', '')
                item['mDate'] = st.xpath('//tr/@pdate').extract()[0]

                isend = funs.s2i(st.xpath('//tr/@isend').extract()[0], 0)

                item['mStatus'] = 0 if isend == 0 else 3
                # 提取比赛得分
                tmpNode = st.xpath('//a[@class="score"]/text()').extract()
                if len(tmpNode) > 0:
                    clst = tmpNode[0].split(':')
                    item['mQj'] = funs.s2i(clst[0])  # 进球数
                    item['mQs'] = funs.s2i(clst[1])  # 失球数
                else:
                    item['mQj'] = 0
                    item['mQs'] = 0


                # 提取比赛时间
                item['mTime'] = st.xpath('//span[@class="match_time"]/text()').extract()[0]

                item['mClass1'] = ''
                item['mClass2'] = ''

                yield item

                mid = item['mMid']
                mdate = item['mDate']

                if response.meta['ou'] == 1:
                    # 欧赔页面url
                    url = 'http://odds.500.com/fenxi/ouzhi-{0}.shtml'.format(mid)
                    yield Request(url=url, callback=self.getOpData, meta={'mid': mid, 'date': mdate})

                if response.meta['ya'] == 1:
                    # 亚赔页面url
                    url = 'http://odds.500.com/fenxi/yazhi-{0}.shtml'.format(mid)
                    yield Request(url=url, callback=self.getYpData, meta={'mid': mid, 'year': mdate[:4], 'date': mdate})

                if response.meta['dx'] == 1:
                    # 大小指数url
                    url = 'http://odds.500.com/fenxi/daxiao-{0}.shtml'.format(mid)
                    yield Request(url=url, callback=self.getSizeData, meta={'mid': mid, 'year': mdate[:4], 'date': mdate})

                if response.meta['rq'] == 1:
                    # 让球指数url
                    url = 'http://odds.500.com/fenxi/rangqiu-{0}.shtml'.format(mid)
                    yield Request(url=url, callback=self.parseRqData, meta={'mid': mid, 'date': mdate, 'page': 1})

                if response.meta['bf'] == 1:
                    # 比分指数
                    url = 'http://odds.500.com/fenxi/bifen-{0}.shtml'.format(mid)
                    yield Request(url=url, callback=self.parseBfData, meta={'mid': mid, 'date': mdate, 'page': 1})
            except Exception as e:
                self.logger.error('[Parse Error]HomePage Error[{0}]'.format(e))

    def parseWorldcup(self, response):
        __vjson = json.loads(response.body)
        datas = __vjson['data']
        for idx, data in enumerate(datas):
            try:
                imItem = MatchDataItem()
                imItem['mMid'] = data['fid']
                imItem['mlsName'] = '世界杯'
                imItem['mSsName'] = '2018赛季'
                imItem['mMtName'] = data['homesxname']
                imItem['mMtFName'] = ''
                imItem['mQj'] = funs.s2i(data['homescore'])
                imItem['mDtName'] = data['awaysxname']
                imItem['mDtFName'] = ''
                imItem['mQs'] = funs.s2i(data['awayscore'])
                imItem['mDate'] = data['matchdate']
                imItem['mTime'] = data['matchtime']
                status = int(data['status'])
                # TODO 正在比赛中的状态,需要在比赛期间看一下
                if status == 4:
                    imItem['mStatus'] = 3
                else:
                    imItem['mStatus'] = 0
                imItem['mClass1'] = data['stage']
                imItem['mClass2'] = data['group']
                yield imItem
            except Exception as e:
                print(e)

    def parseLsscore(self, response):
        datas = Selector(response=response).xpath('//div[@class="lallrace_main"]').extract()
        for idx, data in enumerate(datas):
            # 联赛分区
            couns = Selector(text=data).xpath('//li[not(@class)]').extract()
            for coun in couns:
                lsItem = LSItem()
                url = ''
                if idx == 0:
                    # 解析国际赛事
                    lsItem['mAName'] = '国际赛事'
                    lsItem['mCName'] = '国际'
                    lsItem['mLsName'] = Selector(text=coun).xpath('//span/text()').extract()[0]
                    lsItem['mLsFullName'] = lsItem['mLsName']
                    url = Selector(text=coun).xpath('//a/@href').extract()[0]
                    # TODO: 国际赛事暂时不解析
                else:
                    if idx == 1:
                        lsItem['mAName'] = '欧洲赛事'
                    elif idx == 2:
                        lsItem['mAName'] = '美洲赛事'
                    elif idx == 3:
                        lsItem['mAName'] = '亚洲赛事'
                    elif idx == 4:
                        lsItem['mAName'] = '非洲赛事'
                    # print('--------------------------------------------------------')
                    # 国家名
                    lsItem['mCName'] = Selector(text=coun).xpath('//a/span/text()').extract()[0]
                    lmatchs = Selector(text=coun).xpath('//div/a').extract()
                    for lmatch in lmatchs:
                        try:
                            lsItem['mLsName'] = Selector(text=lmatch).xpath('//a/text()').extract()[0].replace(' ', '')
                            lsItem['mLsFullName'] = Selector(text=lmatch).xpath('//a/@title').extract()[0]
                            print('{0}:{1}'.format(lsItem['mCName'], lsItem['mLsName']))
                            yield lsItem
                            suburl = Selector(text=lmatch).xpath('//a/@href').extract()[0]
                            sid = suburl[7:][:-1]
                            url = 'http://liansai.500.com{0}'.format(suburl)
                            shtml = requests.get(url)
                            shtml = Selector(text=shtml.text)
                            ssName = shtml.xpath('//div[@class="ldrop_bd"]//li[@class="ldrop_list_on"]/a/text()').extract()[0]
                            url = 'http://liansai.500.com/index.php?c=match&a=getmatch&sid={0}&round=1'.format(sid)
                            yield Request(url=url, callback=self.parseLsData, meta={'lsName': lsItem['mLsName'], 'sid': sid, 'ssName': ssName, 'pageindex': 1})
                        except Exception as e:
                            print('SID:{0}Error:{1}'.format(sid, e))

    # 解析杯赛数据
    def parseCupMatch(self, response):
        datas = Selector(response).xpath('//table[@class="lrace_bei"]//td/a').extract()
        for data in datas:
            try:
                lsName = Selector(text=data).xpath('//a/text()').extract()[0]
                if lsName == response.meta['lsName']:
                    url = Selector(text=data).xpath('//a/@href').extract()[0]
                    url = 'http://liansai.500.com{0}'.format(url)
                    html = requests.get(url)
                    ssName = Selector(text=html.text).xpath('//div[@class="ldrop_bd"]//li[@class="ldrop_list_on"]/a/text()').extract()[0]
                    url = Selector(text=html.text).xpath('//div[@class="lcol_tit_r"]/a/@href').extract()[0]
                    url = 'http://liansai.500.com{0}'.format(url)
                    # 获取第一分类地址
                    html = requests.get(url)
                    classes = Selector(text=html.text).xpath('//div[@id="match_stage"]/a[@data-id]').extract()
                    for cs in classes:
                        url = Selector(text=cs).xpath('//a/@href').extract()[0]
                        istid = url.find('jifen-')
                        stid = url[istid + 6:][:-1]
                        url = 'http://liansai.500.com{0}'.format(url)
                        mClass1 = Selector(text=cs).xpath('//a/text()').extract()[0]
                        yield Request(url=url, callback=self.parseBsData, meta={'lsName': response.meta['lsName'], 'ssName': ssName, 'stid': stid, 'mClass1': mClass1})
                    return
            except Exception as e:
                print('parseBsData fail: {0}'.format(e))

    # 解析杯赛数据
    def parseBsData(self, response):
        groups = Selector(response=response).xpath('//div[@id="div_group_list"]/a[@data-group!="all"]').extract()
        if len(groups) > 0:
            for group in groups:
                gId = Selector(text=group).xpath('//a/@data-group').extract()[0]
                gName = Selector(text=group).xpath('//a/text()').extract()[0]
                url = 'http://liansai.500.com/index.php?c=score&a=getmatch&stid={0}&round={1}'.format(response.meta['stid'], gId)
                yield Request(url=url, callback=self.parseGroupData, meta={'lsName': response.meta['lsName'], 'ssName': response.meta['ssName'], 'mClass1': response.meta['mClass1'], 'mClass2': gName})
        else:
            datas = Selector(response=response).xpath('//tbody[@class="jTrInterval"]/tr').extract()
            for data in datas:
                try:
                    st = Selector(text=data)
                    item = MatchDataItem()
                    item['mMid'] = st.xpath('//tr/@data-fid').extract()[0]
                    item['mlsName'] = response.meta['lsName']
                    item['mSsName'] = response.meta['ssName']
                    item['mMtName'] = st.xpath('//td[@class="td_lteam"]/a/text()').extract()[0].replace(' ', '')
                    item['mMtFName'] = st.xpath('//td[@class="td_lteam"]/a/@title').extract()[0].replace(' ', '')
                    item['mDtName'] = st.xpath('//td[@class="td_rteam"]/a/text()').extract()[0].replace(' ', '')
                    item['mDtFName'] = st.xpath('//td[@class="td_rteam"]/a/@title').extract()[0].replace(' ', '')

                    dateTime = st.xpath('//td[@class="td_time"]/text()').extract()[0]
                    item['mDate'] = dateTime[:10]
                    item['mTime'] = dateTime[-5:]

                    status = funs.s2i(st.xpath('//tr/@data-status').extract()[0], 0)
                    if status == 5:
                        item['mStatus'] = 3
                    elif status == 1:
                        item['mStatus'] = 0
                    else:
                        item['mStatus'] = 0
                    # 提取比赛得分
                    item['mQj'] = funs.s2i(st.xpath('//tr/@data-hscore').extract()[0])  # 进球数
                    item['mQs'] = funs.s2i(st.xpath('//tr/@data-ascore').extract()[0])  # 失球数
                    # 分类名称
                    item['mClass1'] = response.meta['mClass1']
                    item['mClass2'] = ''
                    yield item
                except Exception as e:
                    print('parseBsData fail: {0}'.format(e))

    def parseGroupData(self, response):
        try:
            datas = json.loads(response.body)
        except Exception as e:
            print('parseGroupData LoadJson Error: {0}'.format(e))
            return
        for data in datas:
            try:
                imItem = MatchDataItem()
                imItem['mMid'] = data['fid']
                imItem['mlsName'] = response.meta['lsName']
                imItem['mSsName'] = response.meta['ssName']
                imItem['mMtName'] = data['hsxname'].replace(' ', '')
                imItem['mMtFName'] = data['hname']
                imItem['mQj'] = funs.s2i(data['hscore'])
                imItem['mDtName'] = data['gsxname'].replace(' ', '')
                imItem['mDtFName'] = data['gname']
                imItem['mQs'] = funs.s2i(data['gscore'])
                imItem['mDate'] = data['stime'][:10]
                imItem['mTime'] = data['stime'][-5:]
                status = int(data['status'])
                # TODO 正在比赛中的状态,需要在比赛期间看一下
                if status == 5:
                    imItem['mStatus'] = 3
                elif status == 1:
                    imItem['mStatus'] = 0
                else:
                    imItem['mStatus'] = 0
                imItem['mClass1'] = response.meta['mClass1']
                imItem['mClass2'] = response.meta['mClass2']

                yield imItem
            except Exception as e:
                print('parseLsData parse error:{0}'.format(e))

    def parseLsData(self, response):
        lsName = response.meta['lsName']
        ssName = response.meta['ssName']
        pindex = funs.s2i(response.meta['pageindex'], 1)
        sid = response.meta['sid']
        try:
            datas = json.loads(response.body)
        except Exception as e:
            datas = json.loads('[]')
            print('parseLsData LoadJson Error: {0}'.format(e))
            return
        for data in datas:
            try:
                imItem = MatchDataItem()
                imItem['mMid'] = data['fid']
                imItem['mlsName'] = lsName
                imItem['mSsName'] = ssName
                imItem['mMtName'] = data['hsxname'].replace(' ', '')
                imItem['mMtFName'] = data['hname']
                imItem['mQj'] = funs.s2i(data['hscore'])
                imItem['mDtName'] = data['gsxname'].replace(' ', '')
                imItem['mDtFName'] = data['gname']
                imItem['mQs'] = funs.s2i(data['gscore'])
                imItem['mDate'] = data['stime'][:10]
                imItem['mTime'] = data['stime'][-5:]
                status = int(data['status'])
                # TODO 正在比赛中的状态,需要在比赛期间看一下
                if status == 5:
                    imItem['mStatus'] = 3
                elif status == 1:
                    imItem['mStatus'] = 0
                else:
                    imItem['mStatus'] = 0
                imItem['mClass1'] = '第{0}轮'.format(pindex)
                imItem['mClass2'] = ''

                yield imItem
            except Exception as e:
                print('parseLsData parse error:{0}'.format(e))
        if len(datas) > 0 and pindex < 50:
            pindex += 1
            url = 'http://liansai.500.com/index.php?c=match&a=getmatch&sid={0}&round={1}'.format(sid, pindex)
            yield Request(url=url, callback=self.parseLsData, meta={'lsName': lsName, 'sid': sid, 'ssName': ssName, 'pageindex': pindex})

    # 获取欧赔数据
    def getOpData(self, response):
        mid = response.meta['mid']
        spdate = response.meta['date']
        try:
            tmpNode = Selector(response=response).xpath(
                '//div[@class="table_btm"]//span[@id="nowcnum"]/text()').extract()
            lyCount = funs.s2i(tmpNode[0])
            pageCount = lyCount // 30 + (1 if lyCount % 30 > 0 else 0)
            for i in range(pageCount):
                url = 'http://odds.500.com/fenxi1/ouzhi.php?id={0}&ctype=1&start={1}&r=1&style=0&guojia=0&chupan=1'.format(mid, i * 30)
                yield Request(url=url, callback=self.parseOpData, meta={'mid': mid, 'date': spdate})
        except Exception as e:
            self.logger.error('[Parse Error][{0} - {1}]GetOuOdds Error{2}'.format(spdate, mid, e))

    # 解析欧赔一页数据
    def parseOpData(self, response):
        mid = response.meta['mid']
        spdate = response.meta['date']
        datas = Selector(response).xpath('//tr[@ttl="zy"]').extract()
        for data in datas:
            try:
                item = OuOddsItem()
                st = Selector(text=data)
                # 提取博彩公司名称
                lmName = st.xpath('//td[@class="tb_plgs"]/@title').extract()[0]

                item['mMid'] = mid
                item['mlyName'] = lmName.replace(' ', '')
                # 提取数据(20个数据一次按顺序对应相关数据)
                numdatas = st.xpath('//table[@class="pl_table_data"]//tr/td/text()').extract()

                # 即时欧赔
                item['mOdds11'] = funs.s2f(numdatas[0].strip())
                item['mOdds12'] = funs.s2f(numdatas[1].strip())
                item['mOdds13'] = funs.s2f(numdatas[2].strip())

                item['mOdds21'] = funs.s2f(numdatas[3].strip())
                item['mOdds22'] = funs.s2f(numdatas[4].strip())
                item['mOdds23'] = funs.s2f(numdatas[5].strip())

                # 即时概率
                item['mChance11'] = funs.s2f(numdatas[6].strip().replace('%', ''))
                item['mChance12'] = funs.s2f(numdatas[7].strip().replace('%', ''))
                item['mChance13'] = funs.s2f(numdatas[8].strip().replace('%', ''))

                item['mChance21'] = funs.s2f(numdatas[9].strip().replace('%', ''))
                item['mChance22'] = funs.s2f(numdatas[10].strip().replace('%', ''))
                item['mChance23'] = funs.s2f(numdatas[11].strip().replace('%', ''))

                # 返还率
                item['mRetRatio1'] = funs.s2f(numdatas[12].strip().replace('%', ''))
                item['mRetRatio2'] = funs.s2f(numdatas[13].strip().replace('%', ''))

                # 即时凯利
                item['mKaili11'] = funs.s2f(numdatas[14].strip())
                item['mKaili12'] = funs.s2f(numdatas[15].strip())
                item['mKaili13'] = funs.s2f(numdatas[16].strip())

                item['mKaili21'] = funs.s2f(numdatas[17].strip())
                item['mKaili22'] = funs.s2f(numdatas[18].strip())
                item['mKaili23'] = funs.s2f(numdatas[19].strip())

                yield item
                # self.logger.error('[Parse Ok][{0}]Op Data[{1} - {2}]'.format(response.meta['date'], mid, lmName))
            except Exception as e:
                self.logger.error('[Parse Error][{0} - {1}]Parse OuOdds Error{2}'.format(spdate, mid, e))

    # 获取亚赔数据
    def getYpData(self, response):
        mid = response.meta['mid']
        year = response.meta['year']
        spdate = response.meta['date']
        try:
            tmpNode = Selector(response=response).xpath('//div[@class="table_btm"]//span[@id="nowcnum"]/text()').extract()
            lyCount = funs.s2i(tmpNode[0])
            pageCount = lyCount // 30 + (1 if lyCount % 30 > 0 else 0)
            for i in range(pageCount):
                url = 'http://odds.500.com/fenxi1/yazhi.php?id={0}&ctype=1&start={1}&r=1&style=0&guojia=0'.format(mid, i * 30)
                yield Request(url=url, callback=self.parseYpData, meta={'mid': mid, 'year': year, 'date': spdate})
        except Exception as e:
            self.logger.error('[Parse Error][{0} - {1}]GetYaOdds Error{2}'.format(spdate, mid, e))

    # 解析亚盘数据
    def parseYpData(self, response):
        datas = Selector(response).xpath('//tr[@xls="row"]').extract()
        mid = response.meta['mid']
        year = response.meta['year']
        spdate = response.meta['date']
        for data in datas:
            try:
                item = YaOddsItem()
                st = Selector(text=data)
                item['mMid'] = mid

                # 提取博彩公司名称
                lmName = st.xpath('//span[@class="quancheng"]/text()').extract()[0]
                item['mlyName'] = lmName.replace(' ', '')

                oddss = st.xpath('//tr[@xls="row"]//table[@class="pl_table_data"]').extract()

                # 提取即时盘口数据
                tds = Selector(text=oddss[0]).xpath('//td/text()').extract()
                sOdds = tds[0]

                item['mImmOdds1'] = funs.s2f(tds[0].replace('↑', '').replace('↓', ''))
                item['mImmDisc'] = tds[1]
                item['mImmOdds2'] = funs.s2f(tds[2].replace('↑', '').replace('↓', ''))
                item['mImmStatus'] = 1

                tmpNode = st.xpath('//td[@class="ying"]/text()').extract()
                if len(tmpNode) > 0:
                    if tmpNode[0] == tds[2]:
                        item['mImmStatus'] = 2

                # 提取初始盘口数据
                tds = Selector(text=oddss[1]).xpath('//td/text()').extract()
                item['mInitOdds1'] = funs.s2f(tds[0].replace('↑', '').replace('↓', ''))
                item['mInitDisc'] = tds[1]
                item['mInitOdds2'] = funs.s2f(tds[2].replace('↑', '').replace('↓', ''))

                oddsTimes = st.xpath('//time/text()').extract()
                # 即时盘口变化时间
                item['mImmDate'] = '{0}-{1}'.format(year, oddsTimes[0])
                # 初始盘口变化时间
                item['mInitDate'] = '{0}-{1}'.format(year, oddsTimes[0])

                item['mmyId'] = st.xpath('//tr/@id').extract()[0]
                item['mDtDate'] = st.xpath('//tr/@dt').extract()[0]

                yield item

                # 解析明细数据
                sTimpstamp = int(arrow.now().float_timestamp * 1000)
                url = 'http://odds.500.com/fenxi1/inc/ajax.php?_={0}&t=yazhi&p=1&r=1&fixtureid={1}&companyid={2}&updatetime={3}'.format(sTimpstamp, mid, item['mmyId'],
                                                                                                                                        item['mDtDate'])
                # yield Request(url=url, callback=self.parseYpDetailData, meta={'mid': mid, 'lyName': item['mlyName'], 'date': spdate})

                # self.logger.error('[Parse Ok][{0}]Yp Data[{1} - {2}]'.format(response.meta['date'], mid, lmName))
            except Exception as e:
                self.log('[Parse Error][{0} - {1}]Parse YaOdds Error{1}'.format(spdate, mid, e))

    def parseYpDetailData(self, response):
        mid = response.meta['mid']
        lyName = response.meta['lyName']
        spdate = response.meta['date']
        try:
            datas = json.loads(response.body)
            for key, data in enumerate(datas):
                if key == 0: continue
                item = YaOddsDetailItem()
                item['mMid'] = mid
                item['mlyName'] = lyName
                item['mOdds1'] = funs.s2f(data[0])
                item['mDisc'] = data[1]
                item['mOdds2'] = funs.s2f(data[2])
                yield item
            self.logger.warn('[Parse Ok][{0}]Yp Detail Data[{1} - {2}]'.format(response.meta['date'], mid, lyName))
        except Exception as e:
            self.log('[Parse Error][{0} - {1}]Parse YaOdds Details Error{1}'.format(spdate, mid, e))

    # 获取大小指数
    def getSizeData(self, response):
        mid = response.meta['mid']
        year = response.meta['year']
        spdate = response.meta['date']
        try:
            tmpNode = Selector(response=response).xpath('//div[@class="table_btm"]//span[@id="nowcnum"]/text()').extract()
            lyCount = funs.s2i(tmpNode[0])
            pageCount = lyCount // 30 + (1 if lyCount % 30 > 0 else 0)
            for i in range(pageCount):
                url = 'http://odds.500.com/fenxi1/daxiao.php?id={0}&ctype=1&start={1}&r=1&style=0&guojia=0'.format(mid, i * 30)
                yield Request(url=url, callback=self.parseSizeData, meta={'mid': mid, 'year': year, 'date': spdate})
        except Exception as e:
            self.logger.error('[Parse Error][{0} - {1}]GetSizeOdds Error{2}'.format(spdate, mid, e))

    # 解析大小指数
    def parseSizeData(self, response):
        datas = Selector(response).xpath('//tr[@xls="row"]').extract()
        mid = response.meta['mid']
        year = response.meta['year']
        spdate = response.meta['date']
        for data in datas:
            try:
                item = SizeOddsItem()
                st = Selector(text=data)
                item['mMid'] = mid

                # 提取博彩公司名称
                lmName = st.xpath('//span[@class="quancheng"]/text()').extract()[0]
                item['mlyName'] = lmName.replace(' ', '')

                oddss = st.xpath('//tr[@xls="row"]//table[@class="pl_table_data"]').extract()

                # 提取即时盘口数据
                tds = Selector(text=oddss[0]).xpath('//td/text()').extract()
                item['mImmOdds1'] = funs.s2f(tds[0].replace('↑', '').replace('↓', ''))
                item['mImmDisc'] = tds[1].replace('↑', '').replace('↓', '')
                item['mImmOdds2'] = funs.s2f(tds[2].replace('↑', '').replace('↓', ''))
                item['mImmStatus'] = 1

                tmpNode = st.xpath('//td[@class="ying"]/text()').extract()
                if len(tmpNode) > 0:
                    if tmpNode[0] == tds[2]:
                        item['mImmStatus'] = 2

                # 提取初始盘口数据
                tds = Selector(text=oddss[1]).xpath('//td/text()').extract()
                item['mInitOdds1'] = funs.s2f(tds[0].replace('↑', '').replace('↓', ''))
                item['mInitDisc'] = tds[1]
                item['mInitOdds2'] = funs.s2f(tds[2].replace('↑', '').replace('↓', ''))

                oddsTimes = st.xpath('//time/text()').extract()
                # 即时盘口变化时间
                item['mImmDate'] = '{0}-{1}'.format(year, oddsTimes[0])
                # 初始盘口变化时间
                item['mInitDate'] = '{0}-{1}'.format(year, oddsTimes[0])

                item['mmyId'] = st.xpath('//tr/@id').extract()[0]
                item['mDtDate'] = st.xpath('//tr/@dt').extract()[0]

                yield item

                # 解析明细数据
                sTimpstamp = int(arrow.now().float_timestamp * 1000)
                url = 'http://odds.500.com/fenxi1/inc/ajax.php?_={0}&t=daxiao&p=1&r=1&fixtureid={1}&companyid={2}&updatetime={3}'.format(sTimpstamp, mid, item['mmyId'],
                                                                                                                                         item['mDtDate'])
                # yield Request(url=url, callback=self.parseSizeDetailData, meta={'mid': mid, 'lyName': item['mlyName'], 'date': spdate})

                # self.logger.error('[Parse Ok][{0}]Sp Data[{1} - {2}]'.format(response.meta['date'], mid, lmName))
            except Exception as e:
                self.log('[Parse Error][{0} - {1}]Parse YaOdds Error{2}'.format(spdate, mid, e))

    # 解析大小指数明细数据
    def parseSizeDetailData(self, response):
        mid = response.meta['mid']
        lyName = response.meta['lyName']
        spdate = response.meta['date']
        try:
            datas = json.loads(response.body)
            for key, data in enumerate(datas):
                if key == 0: continue
                item = SizeOddsDetailItem()
                item['mMid'] = mid
                item['mlyName'] = lyName
                item['mOdds1'] = funs.s2f(data[0])
                item['mDisc'] = data[1]
                item['mOdds2'] = funs.s2f(data[2])
                yield item
            self.logger.warn('[Parse Ok][{0}]Yp Detail Data[{1} - {2}]'.format(response.meta['date'], mid, lyName))
        except Exception as e:
            self.log('[Parse Error][{0} - {1}]Parse SizeOdds Details Error{2}'.format(spdate, mid, e))

    # 解析让球一页数据
    def parseRqData(self, response):
        mid = response.meta['mid']
        spdate = response.meta['date']
        page = response.meta['page']
        datas = Selector(response).xpath('//tr[@ttl="zy"]').extract()
        for data in datas:
            try:
                item = RqOddsItem()
                st = Selector(text=data)
                # 提取博彩公司名称
                lmName = st.xpath('//td[@class="tb_plgs"]/@title').extract()[0]
                item['mMid'] = mid
                item['mlyName'] = lmName.replace(' ', '')
                # 提取让球数
                num = st.xpath('//td/text()').extract()
                item['mNum'] = funs.s2i(num[2])
                # 提取数据(20个数据一次按顺序对应相关数据)
                numdatas = st.xpath('////table[@class="pl_table_data"]//tr/td/text()').extract()

                # 即时欧赔
                item['mOdds11'] = funs.s2f(numdatas[0].strip())
                item['mOdds12'] = funs.s2f(numdatas[1].strip())
                item['mOdds13'] = funs.s2f(numdatas[2].strip())

                item['mOdds21'] = funs.s2f(numdatas[3].strip())
                item['mOdds22'] = funs.s2f(numdatas[4].strip())
                item['mOdds23'] = funs.s2f(numdatas[5].strip())

                # 即时概率
                item['mChance11'] = funs.s2f(numdatas[6].strip().replace('%', ''))
                item['mChance12'] = funs.s2f(numdatas[7].strip().replace('%', ''))
                item['mChance13'] = funs.s2f(numdatas[8].strip().replace('%', ''))

                item['mChance21'] = funs.s2f(numdatas[9].strip().replace('%', ''))
                item['mChance22'] = funs.s2f(numdatas[10].strip().replace('%', ''))
                item['mChance23'] = funs.s2f(numdatas[11].strip().replace('%', ''))

                # 返还率
                item['mRetRatio1'] = funs.s2f(numdatas[12].strip().replace('%', ''))
                item['mRetRatio2'] = funs.s2f(numdatas[13].strip().replace('%', ''))

                # 即时凯利
                item['mKaili11'] = funs.s2f(numdatas[14].strip())
                item['mKaili12'] = funs.s2f(numdatas[15].strip())
                item['mKaili13'] = funs.s2f(numdatas[16].strip())

                item['mKaili21'] = funs.s2f(numdatas[17].strip())
                item['mKaili22'] = funs.s2f(numdatas[18].strip())
                item['mKaili23'] = funs.s2f(numdatas[19].strip())

                yield item
                # self.logger.error('[Parse Ok][{0}]Op Data[{1} - {2}]'.format(response.meta['date'], mid, lmName))
            except Exception as e:
                self.logger.error('[Parse Error][{0} - {1}]Parse RqOdds Error{2}'.format(spdate, mid, e))

        if len(datas) == 30:
            url = 'http://odds.500.com/fenxi1/rangqiu.php?id={0}&ctype=1&start={1}&r=1&style=0&guojia=0&chupan=1&lot=all'.format(mid, page * 30)
            yield Request(url=url, callback=self.parseRqData, meta={'mid': mid, 'date': spdate, 'page': page + 1})

    # 解析比分指数
    def parseBfData(self, response):
        mid = response.meta['mid']
        spdate = response.meta['date']
        datas = Selector(text=response.text).xpath('//tr[@class="tr1" or @class="tr2"]').extract()
        for data in datas:
            try:
                item = BfOddsItem()
                st = Selector(text=data)
                # 提取博彩公司名称
                lmName = st.xpath('//td[@class="tb_plgs"]/p/a/text()').extract()[0]
                item['mMid'] = mid
                item['mlyName'] = lmName.replace(' ', '')
                # 提取主胜比分赔率
                numdatas = st.xpath('//span[@class="bd_btm"]/text()').extract()
                item['mMw10'] = funs.s2f(numdatas[1])
                item['mMw20'] = funs.s2f(numdatas[2])
                item['mMw21'] = funs.s2f(numdatas[3])
                item['mMw30'] = funs.s2f(numdatas[4])
                item['mMw31'] = funs.s2f(numdatas[5])
                item['mMw32'] = funs.s2f(numdatas[6])
                item['mMw40'] = funs.s2f(numdatas[7])
                item['mMw41'] = funs.s2f(numdatas[8])
                item['mMw42'] = funs.s2f(numdatas[9])
                item['mMw43'] = funs.s2f(numdatas[10])
                # 提取客胜 平 数据
                numdatas = st.xpath('//td/text()').extract()
                item['mDw10'] = funs.s2f(numdatas[1])
                item['mDw20'] = funs.s2f(numdatas[2])
                item['mDw21'] = funs.s2f(numdatas[3])
                item['mDw30'] = funs.s2f(numdatas[4])
                item['mDw31'] = funs.s2f(numdatas[5])
                item['mDw32'] = funs.s2f(numdatas[6])
                item['mDw40'] = funs.s2f(numdatas[7])
                item['mDw41'] = funs.s2f(numdatas[8])
                item['mDw42'] = funs.s2f(numdatas[9])
                item['mDw43'] = funs.s2f(numdatas[10])
                # 平
                item['mD00'] = funs.s2f(numdatas[11])
                item['mD11'] = funs.s2f(numdatas[12])
                item['mD22'] = funs.s2f(numdatas[13])
                item['mD33'] = funs.s2f(numdatas[14])
                item['mD44'] = funs.s2f(numdatas[15])
                yield item
            except Exception as e:
                self.logger.error('[Parse Error][{0} - {1}]Parse BfOdds Error{2}'.format(spdate, mid, e))
