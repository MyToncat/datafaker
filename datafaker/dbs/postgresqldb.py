#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from datafaker.dbs.basedb import BaseDB
# from drivers import load_sqlalchemy
from datafaker.dbs.rdbdb import RdbDB
from datafaker.drivers import load_sqlalchemy
from datafaker.utils import save2db


class PostgresqlDB(RdbDB):

    def construct_self_rows(self):
        session = load_sqlalchemy(self.args.connect)
        # 处理schema.table格式的表名
        table_name = self.args.table
        if '.' in table_name:
            # 如果表名包含点号，说明是schema.table格式
            schema, table = table_name.split('.', 1)
            sql = '''SELECT 
    a.attname AS "字段名",
    pg_catalog.format_type(a.atttypid, a.atttypmod) AS "数据类型",
    col_description(a.attrelid, a.attnum) AS "字段注释"
FROM 
    pg_catalog.pg_attribute a
WHERE 
    a.attrelid = ('%s.%s')::regclass  -- 替换为你的表名
    AND a.attnum > 0  -- 排除系统列
    AND NOT a.attisdropped;  -- 排除已删除的列''' % (schema, table)
        else:
            # 保持原有的处理方式
            sql = '''SELECT 
    a.attname AS "字段名",
    pg_catalog.format_type(a.atttypid, a.atttypmod) AS "数据类型",
    col_description(a.attrelid, a.attnum) AS "字段注释"
FROM 
    pg_catalog.pg_attribute a
WHERE 
    a.attrelid = '%s'::regclass  -- 替换为你的表名
    AND a.attnum > 0  -- 排除系统列
    AND NOT a.attisdropped;  -- 排除已删除的列''' % self.args.table
        rows = session.execute(sql)
        return rows