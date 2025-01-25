import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 连接数据库
conn = sqlite3.connect('events.db')

# 查询数据
df = pd.read_sql_query("""
    SELECT 
        strftime('%Y-%m-%d', time) as date,
        category,
        COUNT(*) as count
    FROM events 
    GROUP BY date, category
    ORDER BY date
""", conn)

# 创建图表目录
os.makedirs('images', exist_ok=True)

# 1. 按类别统计异常总数的饼图
plt.figure(figsize=(10, 6))
category_counts = df.groupby('category')['count'].sum()
plt.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')
plt.title('异常事件类型分布')
plt.savefig('images/event_distribution_pie.png')
plt.close()

# 2. 每日异常数量趋势图
plt.figure(figsize=(12, 6))
daily_counts = df.groupby(['date', 'category'])['count'].sum().unstack()
daily_counts.plot(kind='line', marker='o')
plt.title('每日异常事件趋势')
plt.xlabel('日期')
plt.ylabel('异常数量')
plt.xticks(rotation=45)
plt.legend(title='异常类型', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('images/daily_trend.png')
plt.close()

conn.close() 