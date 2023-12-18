#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import dbinitializer
import dbquery
from dbmodels import *


engine = dbinitializer.create_engine()
dbquery.init_and_connect(engine)


def init_db():
    print("INFO: Initializing DB")
    dbinitializer.init_db()
    print("INFO: End")


def listrec():
    print("INFO: List All records in DB")
    session = dbquery.create_session()
    all_records = session.query(DialogRecord).all()
    # 結果の表示
    for r in all_records:
        print(f"RECORD={r.id}")
        print(r.id, r.status, r.audio2text, r.text2advice)
    session.close()
    print("INFO: End")


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


def main():
    descstr = 'DB Operation Tool for advsvc'
    parser = argparse.ArgumentParser(description=descstr)

    # ロングオプション
    parser.add_argument('--initdb', action='store_true', help='Initialize db')
    parser.add_argument('--listrec', action='store_true', help='list records')
    parser.add_argument('--savewav', type=int, help='save wav by id')

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

    if args.savewav is not None:
        savewav(args.savewav)
        return


main()
