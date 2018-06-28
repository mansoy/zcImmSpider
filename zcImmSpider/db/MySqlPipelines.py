import logging
import pymysql
from twisted.enterprise import adbapi
from .MySqlItems import InterMatchItem
from .MySqlItems import OuOddsItem
from .MySqlItems import YaOddsItem
from .MySqlItems import RqOddsItem
from .MySqlItems import TeamScoreItem
from .MySqlItems import SizeOddsItem
from .MySqlItems import BfOddsItem
from .MySqlItems import LSItem


class MySqlPipelines(object):

    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        # db_params = dict(
        #     host=settings['MYMySql_HOST'],
        #     user=settings['MYMySql_USER'],
        #     password=settings['MYMySql_PASSWORD'],
        #     port=settings['MYMySql_PORT'],
        #     db=settings['MYMySql_DB'],
        #     charset="utf-8",
        #     use_unicode=True,
        #     cursorclass=cursors.Cursor
        # )
        # db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        db_pool = adbapi.ConnectionPool('pymysql',
                                        host=settings["MYSQL_HOST"],
                                        db=settings["MYSQL_DB"],
                                        user=settings["MYSQL_USER"],
                                        password=settings["MYSQL_PASSWORD"],
                                        charset="utf8",
                                        cursorclass=pymysql.cursors.DictCursor,
                                        use_unicode=True)
        return cls(db_pool)

    def process_item(self, item, spider):
        try:
            if isinstance(item, TeamScoreItem):
                self.db_pool.runInteraction(self.process_teamscorc_item, item)
            elif isinstance(item, LSItem):
                self.db_pool.runInteraction(self.process_ls_item, item)
            elif isinstance(item, InterMatchItem):
                self.db_pool.runInteraction(self.process_im_item, item)
            elif isinstance(item, OuOddsItem) or isinstance(item, YaOddsItem) or isinstance(item, SizeOddsItem) or isinstance(item, RqOddsItem) or isinstance(item, BfOddsItem):
                self.db_pool.runInteraction(self.process_odds_item, item)
                # t = threading.Thread(target=self.process_odds_item, args=(item,))
                # t.start()
        except Exception as e:
            print(e)

    # 球队排名Item处理
    def process_teamscorc_item(self, cursor, item):
        try:
            lsid = item.getLMatchId(cursor, item['mLsName'])
            if lsid == -1:
                return
            item['mLsid'] = lsid
            tid = item.getTeamId(cursor)
            if tid == -1:
                item.addTeamItem(cursor)
                tid = item.getTeamId(cursor)
            else:
                item['mTeamId'] = tid
                item.updTeamItem(cursor)
            if tid == -1:
                return
            item['mTeamId'] = tid
            id = item.getLsScoreId(lsid, tid, item['mSeason'])
            if id == -1:
                item.addLsScoreItem(cursor)
            else:
                item['mid'] = id
                item.updLsScoreItem(cursor)
            return True
        except Exception as e:
            print(e)
            return False

    # 处理联赛数据
    def process_ls_item(self, item):
        try:
            # aid = MsDBModel.getAreaId(item['mAName'])
            # if aid == -1:
            #     MsDBModel.addAreaItem(item)
            #     aid = MsDBModel.getAreaId(item['mAName'])
            # if aid == -1:
            #     return False
            # item['mAid'] = aid
            # cid = MsDBModel.getCountryId(item['mCName'])
            # if cid == -1:
            #     MsDBModel.addCountryItem(item)
            #     cid = MsDBModel.getCountryId(item['mCName'])
            # if cid == -1:
            #     return False
            # item['mCid'] = cid
            # lmid = MsDBModel.getLMatchId(item['mLsName'])
            # if lmid == -1:
            #     if MsDBModel.addLMatchItem(item):
            #         return True
            # else:
            #     item['mLsid'] = lmid
            #     MsDBModel.updLMatchItem(item)
            #     return True
            return False
        except Exception as e:
            print(e)
            return False

    def process_im_item(self, cursor, item):
        try:
            lsid = item.getLsid(cursor)
            if lsid == -1:
                item.addLsItem(cursor)
                lsid = item.getLsid(cursor)
            if lsid == -1:
                return

            item['mLsid'] = lsid
            mtid = item.getTeamId(cursor, item['mMtName'])
            if mtid == -1:
                item.addTeamItem(cursor, item['mMtName'])
                mtid = item.getTeamId(cursor, item['mMtName'])
            if mtid == -1:
                return
            item['mMtid'] = mtid

            dtid = item.getTeamId(cursor, item['mDtName'])
            if dtid == -1:
                item.addTeamItem(cursor, item['mDtName'])
                dtid = item.getTeamId(cursor, item['mDtName'])
            if dtid == -1:
                return
            item['mDtid'] = dtid

            imid = item.getImId(cursor)
            if imid == -1:
                item.addImItem(cursor)
            else:
                item['mId'] = imid
                return item.updImItem(cursor)
            return True
        except Exception as e:
            print(e)
            return False

    def process_odds_item(self, cursor, item):
        try:
            # with self.LOCK:
            lyid = item.getLyId(cursor)
            if lyid == -1:
                return False
            item['mlyId'] = lyid
            id = item.getOddsId(cursor)
            if id == -1:
                return item.addOddsItem(cursor)
            else:
                item['mId'] = id
                return item.updOddsItem(cursor)
        except Exception as e:
            print(e)
            return False
