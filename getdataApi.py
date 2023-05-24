from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB连接配置
MONGO_HOST = 'xx.xx.xx.xx'
MONGO_PORT = 27018
MONGO_DB = 'userCenter'
COLLECTION_NAME = 'userOperationLog'

@app.route('/Usage')
def aggregate_query1():
    # 连接到MongoDB
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]

    # 执行第一个聚合查询
    pipeline = [
        {"$match": {"productType": 5,
                     "userId": {"$regex": "^((?!_).)*$"},
            "userId": {"$ne": None}}},
        {
            "$group": {
                "_id": {"userId": "$userId", "loginTimeStamp": "$loginTimeStamp"},
                "maxOperationTime": {"$max": {"$add": ["$operationTime", 8 * 60 * 60 * 1000]}},
                "minOperationTime": {"$min": {"$add": ["$operationTime", 8 * 60 * 60 * 1000]}}
            }
        },
        {
            "$project": {
                "_id": 0,
                "userId": "$_id.userId",
                "maxOperationTime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d %H:%M:%S",
                        "date": {"$add": ["$maxOperationTime", 8 * 60 * 60 * 1000]}
                    }
                },
                "minOperationTime": {
                    "$dateToString": {
                        "format": "%Y-%m-%d %H:%M:%S",
                        "date": {"$add": ["$minOperationTime", 8 * 60 * 60 * 1000]}
                    }
                },
                "loginTimeStamp": "$_id.loginTimeStamp"
            }
        }
    ]

    result = db[COLLECTION_NAME].aggregate(pipeline)

    # 处理查询结果
    documents = []
    for document in result:
        documents.append(document)

    # 关闭连接
    client.close()

    return jsonify(documents)


@app.route('/operation')
def aggregate_query2():
    # 连接到MongoDB
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB]

    # 执行第二个聚合查询
    pipeline = [
        {"$match": {
            "productType": 5,
            "userId": {"$regex": "^((?!_).)*$"},
            "userId": {"$ne": None}
        }},
        {
            "$group": {
                "_id": {"userId": "$userId", "operationTime": "$operationTime", "menuCode": "$menuCode"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "userId": "$_id.userId",
                "operationTime": "$_id.operationTime",
                "menuCode": "$_id.menuCode",
            }
        }
    ]

    result = db[COLLECTION_NAME].aggregate(pipeline)

    # 处理查询结果
    documents = []
    for document in result:
        documents.append(document)

    # 关闭连接
    client.close()

    return jsonify(documents)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1001)
