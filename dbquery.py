from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import StaleDataError
import time
from dbmodels import *
from sqlalchemy import and_


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
