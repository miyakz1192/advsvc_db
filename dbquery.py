from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import StaleDataError
import time
from dbmodels import *
from sqlalchemy import and_
from datetime import datetime, timedelta
import calendar


connection = None
engine = None


def init_and_connect(engine_):
    global engine
    global connection
    engine = engine_
    connection = engine.connect()


def create_session():
    Session = sessionmaker(autocommit=False, bind=engine)
    session = Session()
    return session


def _find_by_id(tgtcls, ident, method="one"):
    session = create_session()
    tgt = session.query(tgtcls).filter(tgtcls.id == ident)
    if method == "one":
        ret = tgt.one()
    elif method == "all":
        ret = tgt.all()

    session.close()
    return ret


def _find_by(tgtcls, params, method="one"):
    session = create_session()
    cond = [getattr(tgtcls, key) == value for key, value in params.items()]
    tgt = session.query(tgtcls).filter(and_(*cond))
    if method == "one":
        ret = tgt.one()
    elif method == "all":
        ret = tgt.all()

    session.close()
    return ret


def find_all_by_id(target_cls, ident):
    return _find_by_id(target_cls, ident, "all")


def find_one_by_id(target_cls, ident):
    return _find_by_id(target_cls, ident, "one")


def find_all_by(target_cls, params):
    return _find_by(target_cls, params, "all")


def find_one_by(target_cls, params):
    return _find_by(target_cls, params, "one")


def update_one_by_id(tgtcls, ident, params):
    session = create_session()
    tgt = session.query(tgtcls).filter(tgtcls.id == ident).one()
    if tgt is None:
        print(f"WARN: nothing to update {target_cls},{ident}")
        return

    for key, value in params.items():
        setattr(tgt, key, value)

    tgt.version += 1

    try:
        session.commit()
    except StaleDataError:
        # ロールバック
        session.rollback()
        print(f"Error: Another tran has modified data. retry.")
    finally:
        session.close()

"""
Time based query
"""
def last_day_of_month(year, month):
    _, last_day = calendar.monthrange(year, month)
    return last_day


def get_week_range_sunday(start_date):
    # 指定された日付を含む週の初め（日曜日）を計算
    start_of_week = start_date - timedelta(days=(start_date.weekday() + 1) % 7)

    # 1週間後の日付を計算
    end_of_week = start_of_week + timedelta(days=6)

    return start_of_week, end_of_week


def find_all_by_datetime(target_cls, start, end=None):
    session = create_session()
    tgt = session.query(target_cls).filter(start <= target_cls.timestamp,
                                           target_cls.timestamp <= end)
    ret = tgt.all()
    session.close()
    return ret


def find_by_datetime(tgt_cls, start, end):
    end = end + timedelta(days=1)
    return find_all_by_datetime(tgt_cls, start, end)


def find_by_day(tgt_cls, year, month, day):
    specified_date = datetime(year, month, day)
    return find_by_datetime(tgt_cls, specified_date, specified_date)


def find_by_week_in_day(tgt_cls, year, month, day):
    specified_date = datetime(year, month, day)
    week_range = get_week_range_sunday(specified_date)
    return find_by_datetime(tgt_cls, start=week_range[0], end=week_range[1])


def find_by_month(tgt_cls, year, month):
    start = datetime(year, month, 1)
    end = datetime(year, month, last_day_of_month(year, month))
    return find_by_datetime(tgt_cls, start, end)
