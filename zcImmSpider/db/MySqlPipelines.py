import logging
import pymysql
from twisted.enterprise import adbapi
from .MySqlItems import MatchDataItem
from .MySqlItems import OuOddsItem
from .MySqlItems import ImmOuOddsItem
from .MySqlItems import YaOddsItem
from .MySqlItems import RqOddsItem
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
            if isinstance(item, MatchDataItem):
                self.db_pool.runInteraction(self.process_md_item, item)
            elif isinstance(item, LSItem):
                self.db_pool.runInteraction(self.process_ls_item, item)
            elif isinstance(item, OuOddsItem) or isinstance(item, ImmOuOddsItem) or isinstance(item, YaOddsItem) or isinstance(item, SizeOddsItem) or isinstance(item, RqOddsItem) or isinstance(item, BfOddsItem):
                self.db_pool.runInteraction(self.process_odds_item, item)
                # t = threading.Thread(target=self.process_odds_item, args=(item,))
                # t.start()
        except Exception as e:
            print(e)

    # 处理联赛数据
    def process_ls_item(self, cursor, item):
        try:
            aid = item.getAreaId(cursor)
            if aid == -1:
                item.addAreaItem(cursor)
                aid = item.getAreaId(cursor)
            if aid == -1:
                return False
            item['mAid'] = aid
            cid = item.getCountryId(cursor)
            if cid == -1:
                item.addCountryItem(cursor)
                cid = item.getCountryId(cursor)
            if cid == -1:
                return False
            item['mCid'] = cid
            lmid = item.getLsid(cursor)
            if lmid == -1:
                if item.addLsItem(cursor):
                    return True
            else:
                item['mLsid'] = lmid
                item.updLsItem(cursor)
                return True
            return False
        except Exception as e:
            print(e)
            return False

    def process_md_item(self, cursor, item):
        try:
            lsid = item.getLsid(cursor)
            if lsid == -1:
                item.addLsItem(cursor)
                lsid = item.getLsid(cursor)
            if lsid == -1:
                return
            item['mlsId'] = lsid
            ssid = item.getSsid(cursor)
            if ssid == -1:
                item.addSsItem(cursor)
                ssid = item.getSsid(cursor)
            if ssid == -1:
                return
            item['mSsId'] = ssid
            mtid = item.getTeamId(cursor, item['mMtName'], item['mMtFName'])
            if mtid == -1:
                item.addTeamItem(cursor, item['mMtName'], item['mMtFName'])
                mtid = item.getTeamId(cursor, item['mMtName'], item['mMtFName'])
            else:
                item['mMtId'] = mtid
                item.updTeamItem(cursor, mtid, item['mMtName'], item['mMtFName'])
            if mtid == -1:
                return
            item['mMtId'] = mtid

            dtid = item.getTeamId(cursor, item['mDtName'], item['mDtFName'])
            if dtid == -1:
                item.addTeamItem(cursor, item['mDtName'], item['mDtFName'])
                dtid = item.getTeamId(cursor, item['mDtName'], item['mMtFName'])
            else:
                item['mDtId'] = dtid
                item.updTeamItem(cursor, dtid, item['mDtName'], item['mDtFName'])
            if dtid == -1:
                return
            item['mDtId'] = dtid

            imid = item.getMdid(cursor)
            if imid == -1:
                item.addMdItem(cursor)
            else:
                item['mid'] = imid
                return item.updMdItem(cursor)
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
