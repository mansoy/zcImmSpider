import scrapy


class MatchDataItem(scrapy.Item):
    mid = scrapy.Field()
    # 比赛场次编号
    mMid = scrapy.Field()
    # 联赛名称
    mlsName = scrapy.Field()
    # 联赛编号
    mlsId = scrapy.Field()
    # 赛季编号
    mSsId = scrapy.Field()
    # 赛季名称
    mSsName = scrapy.Field()
    # 主队名称
    mMtName = scrapy.Field()
    mMtFName = scrapy.Field()
    # 主队编号
    mMtId = scrapy.Field()
    # 客队名称
    mDtName = scrapy.Field()
    mDtFName = scrapy.Field()
    # 客队编号
    mDtId = scrapy.Field()
    # 主队进球
    mQj = scrapy.Field()
    # 客队进球
    mQs = scrapy.Field()
    # 比赛状态
    # TODO 这个状态有几种情况,后续再确定
    mStatus = scrapy.Field()
    # 比赛日期
    mDate = scrapy.Field()
    # 比赛时间
    mTime = scrapy.Field()
    # 分类1
    mClass1 = scrapy.Field()
    # 分类2
    mClass2 = scrapy.Field()

    # 获取联赛编号
    def getLsid(self, cur):
        try:
            sql = 'SELECT id FROM b_lmatch WHERE name=%(name)s or fullname=%(fullname)s'
            values = {
                'name': self['mlsName'],
                'fullname': self['mlsName']
            }

            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    # 增加联赛记录
    def addLsItem(self, cur):
        try:
            sql = 'INSERT INTO b_lmatch(`name`) VALUES(%(name)s)'
            values = {
                # 'cid': self.mCid,
                'name': self['mlsName']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False


    # 获取赛季ID
    def getSsid(self, cur):
        try:
            sql = 'SELECT id FROM season WHERE name=%(name)s and lsid=%(lsid)s'
            values = {
                'name': self['mSsName'],
                'lsid': self['mlsId']
            }

            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    def addSsItem(self, cur):
        try:
            sql = 'INSERT INTO season(`lsid`, `name`) VALUES(%(lsid)s, %(name)s)'
            values = {
                'name': self['mSsName'],
                'lsid': self['mlsId']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False

    # 获取球队ID
    def getTeamId(self, cur, tname, tfname):
        try:
            sql = 'SELECT id FROM b_team WHERE name=%(name)s or fullname=%(name)s or name=%(fullname)s or fullname=%(fullname)s'
            values = {
                'name': tname,
                'fullname': tfname
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    # 增加球队记录
    def addTeamItem(self, cur, tname, tfname):
        try:
            sql = 'INSERT INTO b_team(`name`, `fullname`, `remark`) VALUES(%(name)s, %(fullname)s, %(remark)s)'
            values = {
                'name': tname,
                'fullname': tname,
                'remark': tfname
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False

    # 更新球队记录
    def updTeamItem(self, cur, tid, tname, ftname):
        try:
            sql = '''     
                UPDATE b_team 
                SET `fullname`=CASE WHEN LENGTH(%(fullname)s)>LENGTH(fullname) THEN %(fullname)s ELSE fullname END 
                WHERE id=%(id)s;
                '''
            values = {
                'id': tid,
                'fullname': ftname
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False

    # 获取比赛编号
    def getMdid(self, cur):
        try:
            if self['mMid'] != '':
                sql = '''
                    select id from matchdata where `mid`=%(mid)s
                    '''
                values = {
                    'mid': self['mMid']
                }
            else:
                sql = '''
                    select id from matchdata where `mtid`=%(mtid)s and `dtid`=%(dtid)s and `mdate`=%(mdate)s
                    '''
                values = {
                    'mtid': self['mMtId'],
                    'dtid': self['mDtId'],
                    'mdate': self['mDate']
                }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    # 增加比赛记录
    def addMdItem(self, cur):
        try:
            sql = '''
                INSERT INTO matchdata(`mid`, `ssid`, `mtid`, `jq`, `dtid`, `sq`, `mdate`, `mtime`, `status`, `class1`, `class2`)
                VALUES(%(mid)s, %(ssid)s, %(mtid)s, %(jq)s, %(dtid)s, %(sq)s, %(mdate)s, %(mtime)s, %(status)s, %(class1)s, %(class2)s)                
                '''

            values = {
                'mid': self['mMid'],
                'ssid': self['mSsId'],
                'mtid': self['mMtId'],
                'jq': self['mQj'],
                'dtid': self['mDtId'],
                'sq': self['mQs'],
                'mdate': self['mDate'],
                'mtime': self['mTime'],
                'status': self['mStatus'],
                'class1': self['mClass1'],
                'class2': self['mClass2']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False

    # 更新比赛记录
    def updMdItem(self, cur):
        try:
            sql = '''
                UPDATE matchdata
                SET `mid`=%(mid)s, `ssid`=%(ssid)s, `mtid`=%(mtid)s, `jq`=%(jq)s, 
                    `dtid`=%(dtid)s, `sq`=%(sq)s, `mdate`=%(mdate)s, `mtime`=%(mtime)s, 
                    `status`=%(status)s, `class1`= CASE WHEN %(class1)s='' THEN class1 ELSE %(class1)s END, 
                    `class2`=CASE WHEN %(class2)s='' THEN class2 ELSE %(class2)s END  
                WHERE `id` = %(id)s            
                '''

            values = {
                'id': self['mid'],
                'mid': self['mMid'],
                'ssid': self['mSsId'],
                'mtid': self['mMtId'],
                'jq': self['mQj'],
                'dtid': self['mDtId'],
                'sq': self['mQs'],
                'mdate': self['mDate'],
                'mtime': self['mTime'],
                'status': self['mStatus'],
                'class1': self['mClass1'],
                'class2': self['mClass2']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False


# 赛事Item
class LSItem(scrapy.Item):
    # 分区编号
    mAid = scrapy.Field()
    mAName = scrapy.Field()
    # 国家编号
    mCid = scrapy.Field()
    mCName = scrapy.Field()
    # 赛事名称
    mLsid = scrapy.Field()
    mLsName = scrapy.Field()
    mLsFullName = scrapy.Field()

    def getAreaId(self, cur):
        try:
            sql = 'SELECT id FROM b_area WHERE name=%(name)s'
            values = {
                'name': self['mAName']
            }

            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    def addAreaItem(self, cur):
        try:
            sql = 'INSERT INTO b_area(`name`, `fullname`, `remark`) VALUES(%(name)s, %(fullname)s, %(remark)s)'
            values = {
                'name': self['mAName'],
                'fullname': self['mAName'],
                'remark': ''
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False

    def getCountryId(self, cur):
        try:
            sql = 'SELECT id FROM b_country WHERE name=%(name)s'
            values = {
                'name': self['mCName']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    def addCountryItem(self, cur):
        try:
            sql = 'INSERT INTO b_country(`aid`, `name`, `desc`) VALUES(%(aid)s, %(name)s, %(desc)s)'
            values = {
                'aid': self['mAid'],
                'name': self['mCName'],
                'remark': ''
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False

    def getLsid(self, cur):
        try:
            sql = 'SELECT id FROM b_lmatch WHERE name=%(name)s'
            values = {
                'name': self['mLsName']
            }

            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    def addLsItem(self, cur):
        try:
            sql = 'INSERT INTO b_lmatch(`cid`, `name`, `fullname`, `remark`) VALUES(%(cid)s, %(name)s, %(fullname)s, %(remark)s)'
            values = {
                'cid': self['mCid'],
                'name': self['mLsName'],
                'fullname': self['mLsFullName'],
                'remark': ''
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return -1

    def updLsItem(self, cur):
        try:
            sql = 'UPDATE b_lmatch set cid={0}, name="{1}", fullname="{2}" WHERE id={3};'.format(self['mCid'], self['mLsName'], self['mLsFullName'], self['mLsid'])
            values = {
                # 'cid': item['mCid'],
                # 'name': item['mLsName'],
                # 'fullname': item['mLsFullName'],
                # 'id': item['mLsid']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False


# 球队排名Item
class TeamScoreItem(scrapy.Item):
    mid = scrapy.Field()
    # 赛季名称
    mSeason = scrapy.Field()
    # 联赛Id
    mLsid = scrapy.Field()
    mLsName = scrapy.Field()
    # 球队Id
    mTeamId = scrapy.Field()
    mTeamName = scrapy.Field()
    mTeamFullName = scrapy.Field()
    # 比赛数量
    mMTimes = scrapy.Field()
    # 胜场次数
    mWTimes = scrapy.Field()
    # 负场次数
    mLTimes = scrapy.Field()
    # 平场次数
    mETimes = scrapy.Field()
    # 积分
    mScore = scrapy.Field()

    def getLsid(self, cur):
        try:
            sql = 'SELECT id FROM b_lmatch WHERE name=%(name)s'
            values = {
                'name': self['mLsName']
            }

            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    def getTeamId(self, cur):
        try:
            sql = 'SELECT id FROM b_team WHERE name=%(name)s'
            values = {
                'name': self['mTeamName']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)
            return -1

    def addTeamItem(self, cur):
        try:
            sql = 'INSERT INTO b_team(`name`, `fullname`, `remark`) VALUES(%(name)s, %(fullname)s, %(remark)s)'
            values = {
                'name': self['mTeamName'],
                'fullname': self['mTeamFullName'],
                'remark': ''
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False

    def updTeamItem(self, cur):
        try:
            sql = 'UPDATE b_team SET `name`=%(name)s, `fullname`=%(fullname)s WHERE id=%(id)s'
            values = {
                'id': self['mTeamId'],
                'name': self['mTeamName'],
                'fullname': self['mTeamFullName']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False

    def getLsScoreId(self, cur, lmid, tid, season):
        try:
            sql = 'SELECT id FROM lsscore WHERE lsid=%(lsid)s and tid=%(tid)s and season=%(season)s'
            values = {
                'lsid': lmid,
                'tid': tid,
                'season': season
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    # 获取lsscore表的INSERT数据
    def addLsScoreItem(self, cur):
        try:
            sql = '''
                INSERT INTO lsscore(`season`, `lmid`,tid, mtimes, wtimes, etimes, ltimes, score) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                '''
            values = {
                'season': self.mSeason,
                'lmid': self.mLsid,
                'tid': self.mTeamId,
                'mtimes': self.mMTimes,
                'wtimes': self.mWTimes,
                'etimes': self.mETimes,
                'ltimes': self.mLTimes,
                'score': self.mScore
            }
            cur.execute()
            return True
        except Exception as e:
            print(e)
            return False

    # 获取lsscore表的INSERT数据
    def updLsScoreItem(self, cur):
        try:
            sql = 'UPDATE lsscore set `lmid`=%(lmid)s, tid=%(tid)s, mtimes=%(mtimes)s, wtimes=%(wtimes)s, etimes=%(etimes)s, ltimes=%(ltimes)s, score=%(score)s WHERE id=%(id)s'
            values = {
                'lmid': self.mLsid,
                'tid': self.mTeamId,
                'mtimes': self.mMTimes,
                'wtimes': self.mWTimes,
                'etimes': self.mETimes,
                'ltimes': self.mLTimes,
                'score': self.mScore,
                'id': self.mid
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
            return False


# 欧赔Item
class OuOddsItem(scrapy.Item):
    mId = scrapy.Field()
    # 比赛场次编号
    mMid = scrapy.Field()
    # 博彩公司名称
    mlyName = scrapy.Field()
    # 博彩公司编号
    mlyId = scrapy.Field()
    # 即时欧赔
    mOdds11 = scrapy.Field()
    mOdds12 = scrapy.Field()
    mOdds13 = scrapy.Field()
    mOdds21 = scrapy.Field()
    mOdds22 = scrapy.Field()
    mOdds23 = scrapy.Field()
    # 即时概率
    mChance11 = scrapy.Field()
    mChance12 = scrapy.Field()
    mChance13 = scrapy.Field()
    mChance21 = scrapy.Field()
    mChance22 = scrapy.Field()
    mChance23 = scrapy.Field()
    # 返还率
    mRetRatio1 = scrapy.Field()
    mRetRatio2 = scrapy.Field()
    # 即时凯利
    mKaili11 = scrapy.Field()
    mKaili12 = scrapy.Field()
    mKaili13 = scrapy.Field()
    mKaili21 = scrapy.Field()
    mKaili22 = scrapy.Field()
    mKaili23 = scrapy.Field()

    def getLyId(self, cur):
        try:
            sql = 'SELECT id FROM b_lottery WHERE name=%(name)s'
            values = {
                'name': self['mlyName']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def getOddsId(self, cur):
        try:
            sql = '''
                SELECT id FROM ouodds WHERE mid=%(mid)s and lyid=%(lyid)s
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def addOddsItem(self, cur):
        try:
            sql = '''
                INSERT INTO ouodds(`mid`, `lyid`, `odds11`, `odds12`, `odds13`, `odds21`, `odds22`, `odds23`, `chance11`, `chance12`, 
                    `chance13`, `chance21`, `chance22`, `chance23`, `retratio1`, `retratio2`, `kaili11`, `kaili12`, `kaili13`, `kaili21`, `kaili22`, `kaili23`) 
                VALUES(%(mid)s, %(lyid)s, %(odds11)s, %(odds12)s, %(odds13)s, %(odds21)s, %(odds22)s, %(odds23)s, %(chance11)s, %(chance12)s, 
                    %(chance13)s, %(chance21)s, %(chance22)s, %(chance23)s, %(retratio1)s, %(retratio2)s, %(kaili11)s, %(kaili12)s, %(kaili13)s, %(kaili21)s, 
                    %(kaili22)s, %(kaili23)s)
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'odds11': self['mOdds11'],
                'odds12': self['mOdds12'],
                'odds13': self['mOdds13'],
                'odds21': self['mOdds21'],
                'odds22': self['mOdds22'],
                'odds23': self['mOdds23'],
                'chance11': self['mChance11'],
                'chance12': self['mChance12'],
                'chance13': self['mChance13'],
                'chance21': self['mChance21'],
                'chance22': self['mChance22'],
                'chance23': self['mChance23'],
                'retratio1': self['mRetRatio1'],
                'retratio2': self['mRetRatio2'],
                'kaili11': self['mKaili11'],
                'kaili12': self['mKaili12'],
                'kaili13': self['mKaili13'],
                'kaili21': self['mKaili21'],
                'kaili22': self['mKaili22'],
                'kaili23': self['mKaili23']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)

    def updOddsItem(self, cur):
        try:
            sql = '''
                    UPDATE ouodds
                    SET `mid`=%(mid)s, `lyid`=%(lyid)s, `odds11`=%(odds11)s, `odds12`=%(odds12)s, `odds13`=%(odds13)s, 
                        `odds21`=%(odds21)s, `odds22`=%(odds22)s, `odds23`=%(odds23)s, `chance11`=%(chance11)s, `chance12`=%(chance12)s, 
                        `chance13`=%(chance13)s, `chance21`=%(chance21)s, `chance22`=%(chance22)s, `chance23`=%(chance23)s, 
                        `retratio1`=%(retratio1)s, `retratio2`=%(retratio2)s, `kaili11`=%(kaili11)s, `kaili12`=%(kaili12)s, 
                        `kaili13`=%(kaili13)s, `kaili21`=%(kaili21)s, `kaili22`=%(kaili22)s, `kaili23`=%(kaili23)s
                    WHERE `id`=%(id)s 
                    '''
            values = {
                'id': self['mId'],
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'odds11': self['mOdds11'],
                'odds12': self['mOdds12'],
                'odds13': self['mOdds13'],
                'odds21': self['mOdds21'],
                'odds22': self['mOdds22'],
                'odds23': self['mOdds23'],
                'chance11': self['mChance11'],
                'chance12': self['mChance12'],
                'chance13': self['mChance13'],
                'chance21': self['mChance21'],
                'chance22': self['mChance22'],
                'chance23': self['mChance23'],
                'retratio1': self['mRetRatio1'],
                'retratio2': self['mRetRatio2'],
                'kaili11': self['mKaili11'],
                'kaili12': self['mKaili12'],
                'kaili13': self['mKaili13'],
                'kaili21': self['mKaili21'],
                'kaili22': self['mKaili22'],
                'kaili23': self['mKaili23']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)


# 让球Item
class RqOddsItem(scrapy.Item):
    mId = scrapy.Field()
    # 比赛场次编号
    mMid = scrapy.Field()
    # 博彩公司名称
    mlyName = scrapy.Field()
    # 让球数
    mNum = scrapy.Field()
    # 博彩公司编号
    mlyId = scrapy.Field()
    # 即时欧赔
    mOdds11 = scrapy.Field()
    mOdds12 = scrapy.Field()
    mOdds13 = scrapy.Field()
    mOdds21 = scrapy.Field()
    mOdds22 = scrapy.Field()
    mOdds23 = scrapy.Field()
    # 即时概率
    mChance11 = scrapy.Field()
    mChance12 = scrapy.Field()
    mChance13 = scrapy.Field()
    mChance21 = scrapy.Field()
    mChance22 = scrapy.Field()
    mChance23 = scrapy.Field()
    # 返还率
    mRetRatio1 = scrapy.Field()
    mRetRatio2 = scrapy.Field()
    # 即时凯利
    mKaili11 = scrapy.Field()
    mKaili12 = scrapy.Field()
    mKaili13 = scrapy.Field()
    mKaili21 = scrapy.Field()
    mKaili22 = scrapy.Field()
    mKaili23 = scrapy.Field()

    def getLyId(self, cur):
        try:
            sql = 'SELECT id FROM b_lottery WHERE name=%(name)s'
            values = {
                'name': self['mlyName']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def getOddsId(self, cur):
        try:
            sql = '''
                SELECT id FROM rqodds WHERE mid=%(mid)s and lyid=%(lyid)s and num=%(num)s
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'num': self['mNum']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def addOddsItem(self, cur):
        try:
            sql = '''
                INSERT INTO rqodds(`mid`, `lyid`, `num`, `odds11`, `odds12`, `odds13`, `odds21`, `odds22`, `odds23`, `chance11`, `chance12`, 
                    `chance13`, `chance21`, `chance22`, `chance23`, `retratio1`, `retratio2`, `kaili11`, `kaili12`, `kaili13`, `kaili21`, `kaili22`, `kaili23`) 
                VALUES(%(mid)s, %(lyid)s, %(num)s, %(odds11)s, %(odds12)s, %(odds13)s, %(odds21)s, %(odds22)s, %(odds23)s, %(chance11)s, %(chance12)s, 
                    %(chance13)s, %(chance21)s, %(chance22)s, %(chance23)s, %(retratio1)s, %(retratio2)s, %(kaili11)s, %(kaili12)s, %(kaili13)s, %(kaili21)s, 
                    %(kaili22)s, %(kaili23)s)
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'num': self['mNum'],
                'odds11': self['mOdds11'],
                'odds12': self['mOdds12'],
                'odds13': self['mOdds13'],
                'odds21': self['mOdds21'],
                'odds22': self['mOdds22'],
                'odds23': self['mOdds23'],
                'chance11': self['mChance11'],
                'chance12': self['mChance12'],
                'chance13': self['mChance13'],
                'chance21': self['mChance21'],
                'chance22': self['mChance22'],
                'chance23': self['mChance23'],
                'retratio1': self['mRetRatio1'],
                'retratio2': self['mRetRatio2'],
                'kaili11': self['mKaili11'],
                'kaili12': self['mKaili12'],
                'kaili13': self['mKaili13'],
                'kaili21': self['mKaili21'],
                'kaili22': self['mKaili22'],
                'kaili23': self['mKaili23']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)

    def updOddsItem(self, cur):
        try:
            sql = '''
                    UPDATE rqodds
                    SET `mid`=%(mid)s, `lyid`=%(lyid)s, `num`=%(num)s, `odds11`=%(odds11)s, `odds12`=%(odds12)s, `odds13`=%(odds13)s, 
                        `odds21`=%(odds21)s, `odds22`=%(odds22)s, `odds23`=%(odds23)s, `chance11`=%(chance11)s, `chance12`=%(chance12)s, 
                        `chance13`=%(chance13)s, `chance21`=%(chance21)s, `chance22`=%(chance22)s, `chance23`=%(chance23)s, 
                        `retratio1`=%(retratio1)s, `retratio2`=%(retratio2)s, `kaili11`=%(kaili11)s, `kaili12`=%(kaili12)s, 
                        `kaili13`=%(kaili13)s, `kaili21`=%(kaili21)s, `kaili22`=%(kaili22)s, `kaili23`=%(kaili23)s
                    WHERE `id`=%(id)s 
                    '''
            values = {
                'id': self['mId'],
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'num': self['mNum'],
                'odds11': self['mOdds11'],
                'odds12': self['mOdds12'],
                'odds13': self['mOdds13'],
                'odds21': self['mOdds21'],
                'odds22': self['mOdds22'],
                'odds23': self['mOdds23'],
                'chance11': self['mChance11'],
                'chance12': self['mChance12'],
                'chance13': self['mChance13'],
                'chance21': self['mChance21'],
                'chance22': self['mChance22'],
                'chance23': self['mChance23'],
                'retratio1': self['mRetRatio1'],
                'retratio2': self['mRetRatio2'],
                'kaili11': self['mKaili11'],
                'kaili12': self['mKaili12'],
                'kaili13': self['mKaili13'],
                'kaili21': self['mKaili21'],
                'kaili22': self['mKaili22'],
                'kaili23': self['mKaili23']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)


# 比分指数Item
class BfOddsItem(scrapy.Item):
    mId = scrapy.Field()
    # 比赛场次编号
    mMid = scrapy.Field()
    # 博彩公司名称
    mlyName = scrapy.Field()
    # 博彩公司编号
    mlyId = scrapy.Field()
    # 主胜
    mMw10 = scrapy.Field()
    mMw20 = scrapy.Field()
    mMw21 = scrapy.Field()
    mMw30 = scrapy.Field()
    mMw31 = scrapy.Field()
    mMw32 = scrapy.Field()
    mMw40 = scrapy.Field()
    mMw41 = scrapy.Field()
    mMw42 = scrapy.Field()
    mMw43 = scrapy.Field()
    # 客胜
    mDw10 = scrapy.Field()
    mDw20 = scrapy.Field()
    mDw21 = scrapy.Field()
    mDw30 = scrapy.Field()
    mDw31 = scrapy.Field()
    mDw32 = scrapy.Field()
    mDw40 = scrapy.Field()
    mDw41 = scrapy.Field()
    mDw42 = scrapy.Field()
    mDw43 = scrapy.Field()
    # 平
    mD00 = scrapy.Field()
    mD11 = scrapy.Field()
    mD22 = scrapy.Field()
    mD33 = scrapy.Field()
    mD44 = scrapy.Field()

    def getLyId(self, cur):
        try:
            sql = 'SELECT id FROM b_lottery WHERE name=%(name)s'
            values = {
                'name': self['mlyName']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def getOddsId(self, cur):
        try:
            sql = '''
                SELECT id FROM bfodds WHERE mid=%(mid)s and lyid=%(lyid)s
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def addOddsItem(self, cur):
        try:
            sql = '''
                INSERT INTO bfodds(`mid`, `lyid`, `mw10`, `mw20`, `mw21`, `mw30`, `mw31`, `mw32`, `mw40`, `mw41`, `mw42`, `mw43`, 
                    `dw10`, `dw20`, `dw21`, `dw30`, `dw31`, `dw32`, `dw40`, `dw41`, `dw42`, `dw43`,
                    `d00`, `d11`, `d22`, `d33`, `d44`)
                VALUES(%(mid)s, %(lyid)s, %(mw10)s, %(mw20)s, %(mw21)s, %(mw30)s, %(mw31)s, %(mw32)s, %(mw40)s, %(mw41)s, %(mw42)s, %(mw43)s, 
                    %(dw10)s, %(dw20)s, %(dw21)s, %(dw30)s, %(dw31)s, %(dw32)s, %(dw40)s, %(dw41)s, %(dw42)s, %(dw43)s, 
                    %(d00)s, %(d11)s, %(d22)s, %(d33)s, %(d44)s)
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'mw10': self['mMw10'],
                'mw20': self['mMw20'],
                'mw21': self['mMw21'],
                'mw30': self['mMw30'],
                'mw31': self['mMw31'],
                'mw32': self['mMw32'],
                'mw40': self['mMw40'],
                'mw41': self['mMw41'],
                'mw42': self['mMw42'],
                'mw43': self['mMw43'],
                'dw10': self['mDw10'],
                'dw20': self['mDw20'],
                'dw21': self['mDw21'],
                'dw30': self['mDw30'],
                'dw31': self['mDw31'],
                'dw32': self['mDw32'],
                'dw40': self['mDw40'],
                'dw41': self['mDw41'],
                'dw42': self['mDw42'],
                'dw43': self['mDw43'],
                'd00': self['mD00'],
                'd11': self['mD11'],
                'd22': self['mD22'],
                'd33': self['mD33'],
                'd44': self['mD44']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)

    def updOddsItem(self, cur):
        try:
            sql = '''
                    UPDATE bfodds
                    SET `mid`=%(mid)s, `lyid`=%(lyid)s, 
                        `mw10`=%(mw10)s, `mw20`=%(mw20)s, `mw21`=%(mw21)s, `mw30`=%(mw30)s, `mw31`=%(mw31)s, `mw32`=%(mw32)s, 
                        `mw40`=%(mw40)s, `mw41`=%(mw41)s, `mw42`=%(mw42)s, `mw43`=%(mw43)s, 
                        `dw10`=%(dw10)s, `dw20`=%(dw20)s, `dw21`=%(dw21)s, `dw30`=%(dw30)s, `dw31`=%(dw31)s, `dw32`=%(dw32)s, 
                        `dw40`=%(dw40)s, `dw41`=%(dw41)s, `dw42`=%(dw41)s, `dw43`=%(dw42)s,
                        `d00`=%(d00)s, `d11`=%(d11)s, `d22`=%(d22)s, `d33`=%(d33)s, `d44`=%(d44)s
                    WHERE `id`=%(id)s 
                    '''
            values = {
                'id': self['mId'],
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'mw10': self['mMw10'],
                'mw20': self['mMw20'],
                'mw21': self['mMw21'],
                'mw30': self['mMw30'],
                'mw31': self['mMw31'],
                'mw32': self['mMw32'],
                'mw40': self['mMw40'],
                'mw41': self['mMw41'],
                'mw42': self['mMw42'],
                'mw43': self['mMw43'],
                'dw10': self['mDw10'],
                'dw20': self['mDw20'],
                'dw21': self['mDw21'],
                'dw30': self['mDw30'],
                'dw31': self['mDw31'],
                'dw32': self['mDw32'],
                'dw40': self['mDw40'],
                'dw41': self['mDw41'],
                'dw42': self['mDw42'],
                'dw43': self['mDw43'],
                'd00': self['mD00'],
                'd11': self['mD11'],
                'd22': self['mD22'],
                'd33': self['mD33'],
                'd44': self['mD44']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)


# 亚赔明细
class YaOddsDetailItem(scrapy.Item):
    mMid = scrapy.Field()
    mlyName = scrapy.Field()
    # mlyId = scrapy.Field()
    myoid = scrapy.Field()
    mOdds1 = scrapy.Field()
    mDisc = scrapy.Field()
    mOdds2 = scrapy.Field()


# 亚赔Item
class YaOddsItem(scrapy.Item):
    mId = scrapy.Field()
    # 比赛场次编号
    mMid = scrapy.Field()
    # 一场比赛中的一个赔率编号(对应赔率公司)
    mmyId = scrapy.Field()
    #
    mDtDate = scrapy.Field()
    # 博彩公司名称
    mlyName = scrapy.Field()
    # 博彩公司编号
    mlyId = scrapy.Field()
    # 即时盘口
    mImmOdds1 = scrapy.Field()
    mImmDisc = scrapy.Field()
    mImmOdds2 = scrapy.Field()
    mImmDate = scrapy.Field()
    mImmStatus = scrapy.Field()
    # 初始盘口
    mInitOdds1 = scrapy.Field()
    mInitDisc = scrapy.Field()
    mInitOdds2 = scrapy.Field()
    mInitDate = scrapy.Field()
    # 明细数据(500彩票中的更多)
    mDetailData = scrapy.Field()

    def getLyId(self, cur):
        try:
            sql = 'SELECT id FROM b_lottery WHERE name=%(name)s'
            values = {
                'name': self['mlyName']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def getOddsId(self, cur):
        try:
            sql = '''
                SELECT id FROM yaodds WHERE mid=%(mid)s and lyid=%(lyid)s
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def addOddsItem(self, cur):
        try:
            sql = '''
                INSERT INTO yaodds(`mid`, `lyid`, `immodds1`, `immdisc`, `immodds2`, `immdate`, `immstatus`, 
                    `initodds1`, `initdisc`, `initodds2`, `initdate`, `myid`, `dtdate`) 
                VALUES(%(mid)s, %(lyid)s, %(immodds1)s, %(immdisc)s, %(immodds2)s, %(immdate)s, %(immstatus)s, 
                    %(initodds1)s, %(initdisc)s, %(initodds2)s, %(initdate)s, %(myid)s, %(dtdate)s)                
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'immodds1': self['mImmOdds1'],
                'immdisc': self['mImmDisc'],
                'immodds2': self['mImmOdds2'],
                'immdate': self['mImmDate'],
                'immstatus': self['mImmStatus'],
                'initodds1': self['mInitOdds1'],
                'initdisc': self['mInitDisc'],
                'initodds2': self['mInitOdds2'],
                'initdate': self['mInitDate'],
                'myid': self['mmyId'],
                'dtdate': self['mDtDate']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)

    def updOddsItem(self, cur):
        try:
            sql = '''
                UPDATE yaodds
                SET `mid`=%(mid)s, `lyid`=%(lyid)s, `immodds1`=%(immodds1)s, `immdisc`=%(immdisc)s, `immodds2`=%(immodds2)s, 
                    `immdate`=%(immdate)s, `immstatus`=%(immstatus)s, `initodds1`=%(initodds1)s, `initdisc`=%(initdisc)s, 
                    `initodds2`=%(initodds2)s, `initdate`=%(initdate)s, `myid`=%(myid)s, `dtdate`=%(dtdate)s 
                WHERE `id`=%(id)s
                '''
            values = {
                'id': self['mId'],
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'immodds1': self['mImmOdds1'],
                'immdisc': self['mImmDisc'],
                'immodds2': self['mImmOdds2'],
                'immdate': self['mImmDate'],
                'immstatus': self['mImmStatus'],
                'initodds1': self['mInitOdds1'],
                'initdisc': self['mInitDisc'],
                'initodds2': self['mInitOdds2'],
                'initdate': self['mInitDate'],
                'myid': self['mmyId'],
                'dtdate': self['mDtDate']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)


# 大小指数明细
class SizeOddsDetailItem(scrapy.Item):
    mMid = scrapy.Field()
    mlyName = scrapy.Field()
    # mlyId = scrapy.Field()
    msoid = scrapy.Field()
    mOdds1 = scrapy.Field()
    mDisc = scrapy.Field()
    mOdds2 = scrapy.Field()


# 大小指数Item
class SizeOddsItem(scrapy.Item):
    mId = scrapy.Field()
    # 比赛场次编号
    mMid = scrapy.Field()
    # 一场比赛中的一个赔率编号(对应赔率公司)
    mmyId = scrapy.Field()
    #
    mDtDate = scrapy.Field()
    # 博彩公司名称
    mlyName = scrapy.Field()
    # 博彩公司编号
    mlyId = scrapy.Field()
    # 即时盘口
    mImmOdds1 = scrapy.Field()
    mImmDisc = scrapy.Field()
    mImmOdds2 = scrapy.Field()
    mImmDate = scrapy.Field()
    mImmStatus = scrapy.Field()
    # 初始盘口
    mInitOdds1 = scrapy.Field()
    mInitDisc = scrapy.Field()
    mInitOdds2 = scrapy.Field()
    mInitDate = scrapy.Field()
    # 明细数据(500彩票中的更多)
    mDetailData = scrapy.Field()

    def getLyId(self, cur):
        try:
            sql = 'SELECT id FROM b_lottery WHERE name=%(name)s'
            values = {
                'name': self['mlyName']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def getOddsId(self, cur):
        try:
            sql = '''
                SELECT id FROM sizeodds WHERE mid=%(mid)s and lyid=%(lyid)s
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId']
            }
            cur.execute(sql, values)
            datas = cur.fetchall()
            if len(datas) > 0:
                return datas[0]['id']
            else:
                return -1
        except Exception as e:
            print(e)

    def addOddsItem(self, cur):
        try:
            sql = '''
                INSERT INTO sizeodds(`mid`, `lyid`, `immodds1`, `immdisc`, `immodds2`, `immdate`, `immstatus`, 
                    `initodds1`, `initdisc`, `initodds2`, `initdate`, `myid`, `dtdate`) 
                VALUES(%(mid)s, %(lyid)s, %(immodds1)s, %(immdisc)s, %(immodds2)s, %(immdate)s, %(immstatus)s, 
                    %(initodds1)s, %(initdisc)s, %(initodds2)s, %(initdate)s, %(myid)s, %(dtdate)s)             
                '''
            values = {
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'immodds1': self['mImmOdds1'],
                'immdisc': self['mImmDisc'],
                'immodds2': self['mImmOdds2'],
                'immdate': self['mImmDate'],
                'immstatus': self['mImmStatus'],
                'initodds1': self['mInitOdds1'],
                'initdisc': self['mInitDisc'],
                'initodds2': self['mInitOdds2'],
                'initdate': self['mInitDate'],
                'myid': self['mmyId'],
                'dtdate': self['mDtDate']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)

    def updOddsItem(self, cur):
        try:
            sql = '''
                UPDATE sizeodds
                SET `mid`=%(mid)s, `lyid`=%(lyid)s, `immodds1`=%(immodds1)s, `immdisc`=%(immdisc)s, `immodds2`=%(immodds2)s, 
                    `immdate`=%(immdate)s, `immstatus`=%(immstatus)s, `initodds1`=%(initodds1)s, `initdisc`=%(initdisc)s, 
                    `initodds2`=%(initodds2)s, `initdate`=%(initdate)s, `myid`=%(myid)s, `dtdate`=%(dtdate)s 
                WHERE `id`=%(id)s
                '''
            values = {
                'id': self['mId'],
                'mid': self['mMid'],
                'lyid': self['mlyId'],
                'immodds1': self['mImmOdds1'],
                'immdisc': self['mImmDisc'],
                'immodds2': self['mImmOdds2'],
                'immdate': self['mImmDate'],
                'immstatus': self['mImmStatus'],
                'initodds1': self['mInitOdds1'],
                'initdisc': self['mInitDisc'],
                'initodds2': self['mInitOdds2'],
                'initdate': self['mInitDate'],
                'myid': self['mmyId'],
                'dtdate': self['mDtDate']
            }
            cur.execute(sql, values)
            return True
        except Exception as e:
            print(e)
