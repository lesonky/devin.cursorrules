#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import json
import csv
import argparse
import sys
from pathlib import Path
from typing import Union, List, Dict, Any, Optional
from contextlib import contextmanager

class SQLiteTools:
    def __init__(self, db_path: str):
        """初始化SQLite工具类
        
        Args:
            db_path: 数据库文件路径
        """
        self.db_path = db_path
        self._ensure_db_directory()

    def _ensure_db_directory(self):
        """确保数据库目录存在"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)

    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行SQL查询
        
        Args:
            query: SQL查询语句
            params: 查询参数

        Returns:
            查询结果列表
        """
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                if query.strip().upper().startswith(('SELECT', 'PRAGMA')):
                    rows = cursor.fetchall()
                    return [dict(row) for row in rows]
                else:
                    conn.commit()
                    return [{"affected_rows": cursor.rowcount}]
            except sqlite3.Error as e:
                print(f"SQL执行错误: {str(e)}", file=sys.stderr)
                raise

    def execute_script(self, script: str):
        """执行SQL脚本
        
        Args:
            script: SQL脚本内容
        """
        with self.get_connection() as conn:
            try:
                conn.executescript(script)
                conn.commit()
            except sqlite3.Error as e:
                print(f"SQL脚本执行错误: {str(e)}", file=sys.stderr)
                raise

    def import_csv(self, table_name: str, csv_file: str, delimiter: str = ','):
        """从CSV文件导入数据
        
        Args:
            table_name: 目标表名
            csv_file: CSV文件路径
            delimiter: CSV分隔符
        """
        with open(csv_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f, delimiter=delimiter)
            
            if not csv_reader.fieldnames:
                raise ValueError("CSV文件为空或格式错误")

            # 创建表
            columns = [f"{name} TEXT" for name in csv_reader.fieldnames]
            create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(columns)}
            )
            """
            
            with self.get_connection() as conn:
                conn.execute(create_table_sql)
                
                # 插入数据
                placeholders = ','.join(['?' for _ in csv_reader.fieldnames])
                insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                
                for row in csv_reader:
                    values = [row[field] for field in csv_reader.fieldnames]
                    conn.execute(insert_sql, values)
                
                conn.commit()

    def export_csv(self, query: str, output_file: str, delimiter: str = ','):
        """将查询结果导出到CSV文件
        
        Args:
            query: SQL查询语句
            output_file: 输出文件路径
            delimiter: CSV分隔符
        """
        results = self.execute_query(query)
        
        if not results:
            print("查询结果为空", file=sys.stderr)
            return

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys(), delimiter=delimiter)
            writer.writeheader()
            writer.writerows(results)

def main():
    parser = argparse.ArgumentParser(description='SQLite数据库操作工具')
    parser.add_argument('--db', required=True, help='数据库文件路径')
    parser.add_argument('--query', help='执行SQL查询')
    parser.add_argument('--script', help='执行SQL脚本文件')
    parser.add_argument('--import-csv', help='导入CSV文件')
    parser.add_argument('--table', help='导入CSV时的目标表名')
    parser.add_argument('--export-csv', help='导出查询结果到CSV文件')
    parser.add_argument('--delimiter', default=',', help='CSV分隔符')

    args = parser.parse_args()
    
    try:
        sqlite_tools = SQLiteTools(args.db)
        
        if args.query and not args.export_csv:
            # 只在不导出CSV时打印JSON结果
            results = sqlite_tools.execute_query(args.query)
            print(json.dumps(results, ensure_ascii=False, indent=2))
            
        elif args.script:
            with open(args.script, 'r', encoding='utf-8') as f:
                script_content = f.read()
            sqlite_tools.execute_script(script_content)
            print("SQL脚本执行成功")
            
        elif args.import_csv:
            if not args.table:
                raise ValueError("导入CSV时需要指定目标表名 (--table)")
            sqlite_tools.import_csv(args.table, args.import_csv, args.delimiter)
            print(f"数据已成功导入到表 {args.table}")
            
        elif args.export_csv:
            if not args.query:
                raise ValueError("导出CSV时需要指定查询语句 (--query)")
            sqlite_tools.export_csv(args.query, args.export_csv, args.delimiter)
            print(f"数据已成功导出到 {args.export_csv}")
            
    except Exception as e:
        print(f"错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 