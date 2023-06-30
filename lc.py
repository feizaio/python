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


@app.route('/userid-week')
def calculate_retention_ids_week():
    # 调用API获取数据
    response = requests.get('http://10.16.30.200:1001/operation')  # 将API_URL替换为实际的API地址
    data = response.json()  # 假设API返回的数据是JSON格式

    # 将API返回的数据转换为DataFrame对象
    df = pd.DataFrame(data)

    # 将操作时间createTime转换为日期时间格式
    df['operationTime'] = pd.to_datetime(df['operationTime'], errors='coerce')

    # 获取用户的首次操作时间
    first_operation_time = df.groupby('userId')['operationTime'].min().reset_index().rename(columns={'operationTime': 'first_operationTime'})

    # 合并DataFrame并筛选出符合条件的用户ID
    df_merged = pd.merge(df, first_operation_time, on='userId')
    retention_ids = df_merged[df_merged['operationTime'] >= df_merged['first_operationTime'] + pd.DateOffset(weeks=1)]['userId'].unique().tolist()

    # 创建结果列表，每个元素是一个字典包含用户ID和最后一次记录时间
    result = [{'用户ID': user_id, '最后一次记录时间': df[df['userId'] == user_id]['operationTime'].max().strftime("%Y-%m-%d %H:%M:%S")} for user_id in retention_ids]

    return jsonify(result)



@app.route('/userid-month')
def calculate_retention_ids_month():
    # 调用API获取数据
    response = requests.get('http://10.16.30.200:1001/operation')  # 将API_URL替换为实际的API地址
    data = response.json()  # 假设API返回的数据是JSON格式

    # 将API返回的数据转换为DataFrame对象
    df = pd.DataFrame(data)

    # 将操作时间createTime转换为日期时间格式
    df['operationTime'] = pd.to_datetime(df['operationTime'], errors='coerce')

    # 获取用户的首次操作时间
    first_operation_time = df.groupby('userId')['operationTime'].min()

    # 获取一个月后仍然有记录的用户ID
    retention_ids = []
    for user_id, first_time in first_operation_time.items():
        one_month_after = first_time + pd.DateOffset(months=1)
        if df[(df['userId'] == user_id) & (df['operationTime'] >= one_month_after)].shape[0] > 0:
            retention_ids.append(user_id)

    # 创建结果列表，每个元素是一个字典包含序号、用户ID和最后一次记录时间
    result = []
    for i, user_id in enumerate(retention_ids):
        user_df = df[df['userId'] == user_id]
        last_record_time = user_df['operationTime'].max()
        if pd.notnull(last_record_time):
            last_record_time = last_record_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            last_record_time = "缺失"
        result.append({'序号': i+1, '用户ID': user_id, '最后一次记录时间': last_record_time})

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1003)
