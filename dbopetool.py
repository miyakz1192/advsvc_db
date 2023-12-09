#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import dbinitializer


def init_db():
    dbinitializer.init_db()


def main():
    descstr = 'DB Operation Tool for advsvc'
    parser = argparse.ArgumentParser(description=descstr)

    # ロングオプション
    parser.add_argument('--initdb', action='store_true', help='Initialize db')

    # 位置引数（オプションではない引数）
    # parser.add_argument('positional_arg', type=int, help='位置引数のサンプル')

    args = parser.parse_args()

    # 取得した引数の利用
    # if args.short:
    #    print('ショートオプションが指定されました')
    #
    # if args.long:
    #    print('ロングオプションが指定されました')

    if args.initdb:
        init_db()


main()
