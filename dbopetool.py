#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import dbinitializer
import dbquery
from dbmodels import *
from datetime import datetime


engine = dbinitializer.create_engine()
dbquery.init_and_connect(engine)


def init_db():
    print("INFO: Initializing DB")
    dbinitializer.init_db()
    print("INFO: End")


def drop_all():
    dbinitializer.drop_all()


def listrec():
    print("INFO: List All records in DB")
    session = dbquery.create_session()
    all_records = session.query(DialogRecord).all()
    # 結果の表示
    for r in all_records:
        # print(f"RECORD={r.id}")
        print(f"ID={r.id},STATUS={r.status},A2T={r.audio2text},T2AF={r.text2advice_full},T2A={r.text2advice},Time={r.timestamp}")
    session.close()
    print("INFO: End")


def listsumnone():
    print("INFO: List Summary is none or insufficient")
    session = dbquery.create_session()
    all_records = session.query(DialogRecord).all()
    
    res = {}
    # TODO: FIXME: this code is low performance maybe. improve...
    # 結果の表示
    for r in all_records:
        # print(f"RECORD={r.id}")
        if r.text2advice is None:
            continue
        year = r.timestamp.year
        month = r.timestamp.month
        day = r.timestamp.day

        summaries = dbquery.find_by_day(SummaryRecord, year, month, day) 
        if summaries is not None:
            for s in summaries:
                if s.advice2summary is not None:
                    continue
                res[(year,month,day)] = s.id

    session.close()

    for _, v in res.items():
        print(f"ID={v}")

    print("INFO: End")


def listrecsum():
    print("INFO: List All records in DB")
    session = dbquery.create_session()
    all_records = session.query(SummaryRecord).all()
    # 結果の表示
    for r in all_records:
        print(f"ID={r.id},SUMMARY={r.advice2summary},Time={r.timestamp}")
    session.close()
    print("INFO: End")


def listt2anone():
    session = dbquery.create_session()
    all_records = session.query(DialogRecord).all()
    # 結果の表示
    for r in all_records:
        if r.text2advice is None:
            print(f"ID={r.id}")
    session.close()


def savewav(id):
    print("INFO: save wav file as id.wav")
    session = dbquery.create_session()
    r = dbquery.find_one_by_id(DialogRecord, id)

    if r is None:
        print(f"INFO: record is not found {id}")
        return

    # 結果の表示
    print(r.id, r.status, r.audio2text, r.text2advice)
    with open(f"{id}.wav", 'wb') as file:
        file.write(r.raw_audio)

    session.close()
    print("INFO: End")
# メモ：ちなみに、session作ったら自動的にトランザクションが開始
# される。commitとかrollbackを明示的に指定しないと、rollbackになる
# 以下、ChatGPTに聞いてみた時のメモ。
# はい、その通りです。session.commit() を呼び出さない限り、トランザクションは
# 自動的にロールバックされます。これは SQLAlchemy の挙動です。
# トランザクションを明示的にコミットする必要は、データベースへの変更（INSERT、
# UPDATE、DELETEなど）を行った場合に発生します。
# ただし、SELECT 文などの読み取り専用操作の場合は通常コミットが不要です。


def savea2t(id):
    print("INFO: save audio2text culumn as id.txt")
    session = dbquery.create_session()
    r = dbquery.find_one_by_id(DialogRecord, id)

    if r is None:
        print(f"INFO: record is not found {id}")
        return

    # 結果の表示
    print(r.id, r.status, r.audio2text, r.text2advice)
    with open(f"{id}.txt", 'w') as file:
        file.write(r.audio2text)

    session.close()
    print("INFO: End")


def main():
    descstr = 'DB Operation Tool for advsvc'
    parser = argparse.ArgumentParser(description=descstr)

    # ロングオプション
    parser.add_argument('--initdb', action='store_true', help='Initialize db')
    parser.add_argument('--listrec', action='store_true', help='list records')
    parser.add_argument('--listrecsum', action='store_true', help='list records(summary)')
    parser.add_argument('--listt2anone', action='store_true', help='list text to advice is none')
    parser.add_argument('--listsumnone', action='store_true', help='list summary is not none or insufficient')
    parser.add_argument('--savewav', type=int, help='save wav by id')
    parser.add_argument('--savea2t', type=int, help='save audio2text by id')
    parser.add_argument('--dropall', action='store_true', help='drop table all')

    args = parser.parse_args()

    # 取得した引数の利用
    # if args.short:
    #    print('ショートオプションが指定されました')
    #
    # if args.long:
    #    print('ロングオプションが指定されました')

    if args.initdb:
        init_db()
        return

    if args.listrec:
        listrec()
        return

    if args.listrecsum:
        listrecsum()
        return

    if args.listt2anone:
        listt2anone()
        return

    if args.listsumnone:
        listsumnone()
        return

    if args.savewav is not None:
        savewav(args.savewav)
        return

    if args.dropall is not None:
        drop_all()

    # saving audio2text column of id(record==args.savea2t)
    if args.savea2t is not None:
        savea2t(args.savea2t)
        return


main()
