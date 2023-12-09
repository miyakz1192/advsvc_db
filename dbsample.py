import dbinitializer
import dbquery
from dbmodels import *

engine = dbinitializer.create_engine()
dbquery.init_and_connect(engine)

# mode = "find_test1"
mode = "find_test2"
# mode = "create_sample1"
# mode = "update_sample1"

if mode == "find_test1":
    print("find_test1")
    print(f"DEBUG: {dbquery.engine}")
    res = dbquery.find_one_by_id(DialogRecord, 1)
    print(res)
    res = dbquery.find_all_by_id(DialogRecord, 1)
    print(res)

if mode == "find_test2":
    print("S ********find_test2")
    print("=============")
    res = dbquery.find_one_by(DialogRecord, {"uuid": "uuid_mod", "version": 1})
    print(res)
    print("=============")
    res = dbquery.find_all_by(DialogRecord, {"uuid": "uuid_mod", "version": 1})
    print(res)
    print("E ********find_test2")

if mode == "create_sample1":
    print("create_sample1")
    session = dbquery.create_session()
    dr1 = DialogRecord(uuid="uuid1")
    session.add_all([dr1])
    session.commit()

if mode == "update_sample1":
    print("update_sample1")
    dbquery.update_one_by_id(tgtcls=DialogRecord, ident=2,
                             params={"uuid": "uuid_mod"})
