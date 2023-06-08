from flask import Flask, jsonify
import pandas as pd
from datetime import datetime, timedelta
import requests

app = Flask(__name__)

@app.route('/Retained-1')
def calculate_retention():
    # 调用API获取数据
    response = requests.get('http://10.16.30.200:1001/operation')  # 将API_URL替换为实际的API地址
    data = response.json()  # 假设API返回的数据是JSON格式

    # 将API返回的数据转换为DataFrame对象
    df = pd.DataFrame(data)
    # 将操作时间createTime转换为日期格式
    df['operationTime'] = pd.to_datetime(df['operationTime'], errors='coerce').dt.date
    df = df.dropna(subset=['operationTime'])
    df = df.drop_duplicates()

    # 计算每天的次日留存率
    day_retention = []
    for date in df['operationTime'].unique():
        today_users = set(df[df['operationTime'] == date]['userId'])
        tomorrow_users = set(df[df['operationTime'] == date + timedelta(days=1)]['userId'])
        
        # 检查当天用户集合是否为空
        if len(today_users) == 0:
            retention_rate = 0  # 给留存率一个默认值，可以根据需求进行调整
        else:
            retention_rate = len(today_users & tomorrow_users) / len(today_users)
        #retention_rate_formatted = "{:.2%}".format(retention_rate * 100)
        day_retention.append({'date': date.strftime("%Y-%m-%d"), 'retention_rate': retention_rate})

    # 将每天的次日留存率转换为DataFrame格式
    day_retention_df = pd.DataFrame(day_retention)

    # 按照日期进行排序
    day_retention_df = day_retention_df.sort_values(by='date')

    result = {'day_retention': [{'date': str(record['date']), 'retention_rate': f"{record['retention_rate']:.2%}"} for record in day_retention] }
    return jsonify(result)

@app.route('/Retained-7')
def calculate_retention2():
    # 调用API获取数据
    response = requests.get('http://10.16.30.200:1001/operation')  # 将API_URL替换为实际的API地址
    data = response.json()  # 假设API返回的数据是JSON格式

    # 将API返回的数据转换为DataFrame对象
    df = pd.DataFrame(data)
    # 将操作时间createTime转换为日期格式
    df['operationTime'] = pd.to_datetime(df['operationTime'], errors='coerce').dt.date
    df = df.dropna(subset=['operationTime'])
    df = df.drop_duplicates()
    # 计算每周的7天内留存
    week_retention = []
    processed_weeks = set()  # 用于跟踪已处理的周

    for date in df['operationTime'].unique():
        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=6)
        
        if (week_start, week_end) in processed_weeks:
            continue  # 如果该周已经处理过，则跳过
        
        processed_weeks.add((week_start, week_end))
        
        week_users = set(df[(df['operationTime'] >= week_start) & (df['operationTime'] <= week_end)]['userId'].unique())
        next_week_users = set(df[(df['operationTime'] >= week_end + timedelta(days=1)) & (df['operationTime'] <= week_end + timedelta(days=7))]['userId'].unique())
        
        if len(week_users) == 0:
            retention_rate = 0
        else:
            retention_rate = len(week_users & next_week_users) / len(week_users)
        #retention_rate_formatted = "{:.2%}".format(retention_rate * 100)
        week_retention.append({'week_start': week_start.strftime("%Y-%m-%d"), 'week_end': week_end.strftime("%Y-%m-%d"), 'retention_rate': retention_rate})

    week_retention_df = pd.DataFrame(week_retention)
    
    # 返回结果
    result = {'week_retention': [{'week_start': str(record['week_start']), 'week_end': str(record['week_end']), 'retention_rate': f"{record['retention_rate']:.2%}"} for record in week_retention]}
    
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1003)
