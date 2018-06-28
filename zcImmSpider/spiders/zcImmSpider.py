import scrapy
import arrow
import json
from scrapy.http import Request
from scrapy.selector import Selector
from ..db.MySqlItems import TeamScoreItem
from ..db.MySqlItems import LSItem
from ..db.MySqlItems import InterMatchItem
from ..db.MySqlItems import RqOddsItem
from ..db.MySqlItems import BfOddsItem
from ..db.MySqlItems import OuOddsItem
from ..db.MySqlItems import YaOddsItem
from ..db.MySqlItems import SizeOddsItem
from ..db.MySqlItems import YaOddsDetailItem
from ..db.MySqlItems import SizeOddsDetailItem
from .. import config as cf


class zcImmSpider(scrapy.Spider):
    name = 'zcImmSpider'
    allowed_domains = ['500.com']
    base_url = 'http://liansai.500.com'
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
                self.startDate = arrow.get(self.params['startDate'])
                self.endData = arrow.get(self.params['endDate'])


            # url = 'http://liansai.500.com/'
            # yield Request(url=url, callback=self.parseLsscore)
        except Exception as e:
            print(e)

    def parseWorldcup(self, response):
        __vjson = json.loads(response.body)
        datas = __vjson['data']
        for idx, data in enumerate(datas):
            try:
                imItem = InterMatchItem()
                imItem['mLsName'] = '世界杯'
                imItem['mSeason'] = '2018赛季'
                imItem['mGroup'] = data['group']
                imItem['mStage'] = data['stage']
                imItem['mIndex'] = idx
                imItem['mMid'] = data['fid']
                imItem['mMtName'] = data['homesxname']
                imItem['mMScore'] = data['homescore']
                imItem['mDtName'] = data['awaysxname']
                imItem['mDScore'] = data['awayscore']
                imItem['mMDate'] = data['matchdate']
                imItem['mMTime'] = data['matchtime']
                imItem['mStatus'] = data['status']
                imItem['mStatusDesc'] = data['status_desc']
                # yield imItem
                mid = imItem['mMid']
                mdata = imItem['mMDate']
                if mid != '':
                    # yield self.requestOdds(mid, mdata)
                    # # 欧赔页面url
                    # url = 'http://odds.500.com/fenxi/ouzhi-{0}.shtml'.format(mid)
                    # yield Request(url=url, callback=self.getOpData, meta={'mid': mid, 'date': mdata})
                    #
                    # # 亚赔页面url
                    # url = 'http://odds.500.com/fenxi/yazhi-{0}.shtml'.format(mid)
                    # yield Request(url=url, callback=self.getYpData, meta={'mid': mid, 'year': mdata[:4], 'date': mdata})
                    #
                    # # 大小指数url
                    # url = 'http://odds.500.com/fenxi/daxiao-{0}.shtml'.format(mid)
                    # yield Request(url=url, callback=self.getSizeData, meta={'mid': mid, 'year': mdata[:4], 'date': mdata})

                    # # 让球指数url
                    # url = 'http://odds.500.com/fenxi/rangqiu-{0}.shtml'.format(mid)
                    # # url = 'http://odds.500.com/fenxi1/rangqiu.php?id={0}&ctype=1&start={1}&r=1&style=0&guojia=0&chupan=1&lot=all'.format(mid, 0)
                    # yield Request(url=url, callback=self.parseRqData, meta={'mid': mid, 'date': mdata, 'page': 1})

                    # 比分指数
                    url = 'http://odds.500.com/fenxi/bifen-{0}.shtml'.format(mid)
                    yield Request(url=url, callback=self.parseBfData, meta={'mid': mid, 'date': mdata})
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
                    print('--------------------------------------------------------')
                    # 国家名
                    lsItem['mCName'] = Selector(text=coun).xpath('//a/span/text()').extract()[0]
                    lmatchs = Selector(text=coun).xpath('//div/a').extract()
                    # if lsItem['mCName'] == '巴西': continue
                    for lmatch in lmatchs:
                        try:
                            lsItem['mLsName'] = Selector(text=lmatch).xpath('//a/text()').extract()[0].replace(' ', '')
                            lsItem['mLsFullName'] = Selector(text=lmatch).xpath('//a/@title').extract()[0]
                            print(lsItem['mLsName'])
                            yield lsItem
                            url = Selector(text=lmatch).xpath('//a/@href').extract()[0]
                            url = '{0}{1}'.format(self.base_url, url)
                            yield Request(url=url, callback=self.parseScore, meta={'lsName': lsItem['mLsName']})
                        except Exception as e:
                            print(e)

    def parseScore(self, response):
        lsName = response.meta['lsName']
        # 赛季名称
        ssName = Selector(response).xpath('//div[@class="ldrop_bd"]//li[@class="ldrop_list_on"]/a/text()').extract()
        datas = Selector(response).xpath('//table[@class="lstable1 ljifen_top_list_s jTrHover"]//tr').extract()
        if len(datas) <= 1:
            return
        for idx, data in enumerate(datas):
            if idx == 0:
                continue
            item = TeamScoreItem()
            tds = Selector(text=data).xpath('//td').extract()
            # 赛季
            item['mSeason'] = ssName
            # 提取球队信息
            item['mLsName'] = lsName
            sTmp = Selector(text=tds[1]).xpath('//a/text()').extract()[0].replace(' ', '').replace('  ', '')
            item['mTeamName'] = sTmp
            item['mTeamFullName'] = Selector(text=tds[1]).xpath('//a/@title').extract()[0].replace(' ', '').replace('  ', '')
            # 提取比赛信息
            # 场次
            stmp = Selector(text=tds[2]).xpath('//text()').extract()[0].replace(' ', '').replace('  ', '')
            item['mMTimes'] = int(stmp)
            # 胜场次数
            stmp = Selector(text=tds[3]).xpath('//text()').extract()[0].replace(' ', '').replace('  ', '')
            item['mWTimes'] = int(stmp)
            # 平场次数
            stmp = Selector(text=tds[4]).xpath('//text()').extract()[0].replace(' ', '').replace('  ', '')
            item['mETimes'] = int(stmp)
            # 负场次数
            stmp = Selector(text=tds[5]).xpath('//text()').extract()[0].replace(' ', '').replace('  ', '')
            item['mLTimes'] = int(stmp)
            # 胜场次数
            stmp = Selector(text=tds[6]).xpath('//text()').extract()[0].replace(' ', '').replace('  ', '')
            item['mScore'] = int(stmp)

            yield item

    # 获取欧赔数据
    def getOpData(self, response):
        mid = response.meta['mid']
        spdate = response.meta['date']
        try:
            tmpNode = Selector(response=response).xpath(
                '//div[@class="table_btm"]//span[@id="nowcnum"]/text()').extract()
            lyCount = int(tmpNode[0])
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
                numdatas = st.xpath('////table[@class="pl_table_data"]//tr/td/text()').extract()

                # 即时欧赔
                item['mOdds11'] = float(numdatas[0].strip())
                item['mOdds12'] = float(numdatas[1].strip())
                item['mOdds13'] = float(numdatas[2].strip())

                item['mOdds21'] = float(numdatas[3].strip())
                item['mOdds22'] = float(numdatas[4].strip())
                item['mOdds23'] = float(numdatas[5].strip())

                # 即时概率
                item['mChance11'] = float(numdatas[6].strip().replace('%', ''))
                item['mChance12'] = float(numdatas[7].strip().replace('%', ''))
                item['mChance13'] = float(numdatas[8].strip().replace('%', ''))

                item['mChance21'] = float(numdatas[9].strip().replace('%', ''))
                item['mChance22'] = float(numdatas[10].strip().replace('%', ''))
                item['mChance23'] = float(numdatas[11].strip().replace('%', ''))

                # 返还率
                item['mRetRatio1'] = float(numdatas[12].strip().replace('%', ''))
                item['mRetRatio2'] = float(numdatas[13].strip().replace('%', ''))

                # 即时凯利
                item['mKaili11'] = float(numdatas[14].strip())
                item['mKaili12'] = float(numdatas[15].strip())
                item['mKaili13'] = float(numdatas[16].strip())

                item['mKaili21'] = float(numdatas[17].strip())
                item['mKaili22'] = float(numdatas[18].strip())
                item['mKaili23'] = float(numdatas[19].strip())

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
            lyCount = int(tmpNode[0])
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

                item['mImmOdds1'] = float(tds[0].replace('↑', '').replace('↓', ''))
                item['mImmDisc'] = tds[1]
                item['mImmOdds2'] = float(tds[2].replace('↑', '').replace('↓', ''))
                item['mImmStatus'] = 1

                tmpNode = st.xpath('//td[@class="ying"]/text()').extract()
                if len(tmpNode) > 0:
                    if tmpNode[0] == tds[2]:
                        item['mImmStatus'] = 2

                # 提取初始盘口数据
                tds = Selector(text=oddss[1]).xpath('//td/text()').extract()
                item['mInitOdds1'] = float(tds[0].replace('↑', '').replace('↓', ''))
                item['mInitDisc'] = tds[1]
                item['mInitOdds2'] = float(tds[2].replace('↑', '').replace('↓', ''))

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
                item['mOdds1'] = float(data[0])
                item['mDisc'] = data[1]
                item['mOdds2'] = float(data[2])
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
            lyCount = int(tmpNode[0])
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
                item['mImmOdds1'] = float(tds[0].replace('↑', '').replace('↓', ''))
                item['mImmDisc'] = tds[1].replace('↑', '').replace('↓', '')
                item['mImmOdds2'] = float(tds[2].replace('↑', '').replace('↓', ''))
                item['mImmStatus'] = 1

                tmpNode = st.xpath('//td[@class="ying"]/text()').extract()
                if len(tmpNode) > 0:
                    if tmpNode[0] == tds[2]:
                        item['mImmStatus'] = 2

                # 提取初始盘口数据
                tds = Selector(text=oddss[1]).xpath('//td/text()').extract()
                item['mInitOdds1'] = float(tds[0].replace('↑', '').replace('↓', ''))
                item['mInitDisc'] = tds[1]
                item['mInitOdds2'] = float(tds[2].replace('↑', '').replace('↓', ''))

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
                item['mOdds1'] = float(data[0])
                item['mDisc'] = data[1]
                item['mOdds2'] = float(data[2])
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
                item['mNum'] = int(num[2])
                # 提取数据(20个数据一次按顺序对应相关数据)
                numdatas = st.xpath('////table[@class="pl_table_data"]//tr/td/text()').extract()

                # 即时欧赔
                item['mOdds11'] = float(numdatas[0].strip())
                item['mOdds12'] = float(numdatas[1].strip())
                item['mOdds13'] = float(numdatas[2].strip())

                item['mOdds21'] = float(numdatas[3].strip())
                item['mOdds22'] = float(numdatas[4].strip())
                item['mOdds23'] = float(numdatas[5].strip())

                # 即时概率
                item['mChance11'] = float(numdatas[6].strip().replace('%', ''))
                item['mChance12'] = float(numdatas[7].strip().replace('%', ''))
                item['mChance13'] = float(numdatas[8].strip().replace('%', ''))

                item['mChance21'] = float(numdatas[9].strip().replace('%', ''))
                item['mChance22'] = float(numdatas[10].strip().replace('%', ''))
                item['mChance23'] = float(numdatas[11].strip().replace('%', ''))

                # 返还率
                item['mRetRatio1'] = float(numdatas[12].strip().replace('%', ''))
                item['mRetRatio2'] = float(numdatas[13].strip().replace('%', ''))

                # 即时凯利
                item['mKaili11'] = float(numdatas[14].strip())
                item['mKaili12'] = float(numdatas[15].strip())
                item['mKaili13'] = float(numdatas[16].strip())

                item['mKaili21'] = float(numdatas[17].strip())
                item['mKaili22'] = float(numdatas[18].strip())
                item['mKaili23'] = float(numdatas[19].strip())

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
        datas = Selector(response).xpath('//tr[@class="tr1" or @class="tr2"]').extract()
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
                item['mMw10'] = float(numdatas[1])
                item['mMw20'] = float(numdatas[2])
                item['mMw21'] = float(numdatas[3])
                item['mMw30'] = float(numdatas[4])
                item['mMw31'] = float(numdatas[5])
                item['mMw32'] = float(numdatas[6])
                item['mMw40'] = float(numdatas[7])
                item['mMw41'] = float(numdatas[8])
                item['mMw42'] = float(numdatas[9])
                item['mMw43'] = float(numdatas[10])
                # 提取客胜 平 数据
                numdatas = st.xpath('//td/text()').extract()
                item['mDw10'] = float(numdatas[1])
                item['mDw20'] = float(numdatas[2])
                item['mDw21'] = float(numdatas[3])
                item['mDw30'] = float(numdatas[4])
                item['mDw31'] = float(numdatas[5])
                item['mDw32'] = float(numdatas[6])
                item['mDw40'] = float(numdatas[7])
                item['mDw41'] = float(numdatas[8])
                item['mDw42'] = float(numdatas[9])
                item['mDw43'] = float(numdatas[10])
                # 平
                item['mD00'] = float(numdatas[11])
                item['mD11'] = float(numdatas[12])
                item['mD22'] = float(numdatas[13])
                item['mD33'] = float(numdatas[14])
                item['mD44'] = float(numdatas[15])
                yield item
            except Exception as e:
                self.logger.error('[Parse Error][{0} - {1}]Parse BfOdds Error{2}'.format(spdate, mid, e))
