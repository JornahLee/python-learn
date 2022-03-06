import bson
from pymongo import MongoClient
import atexit
from sshtunnel import SSHTunnelForwarder
import json
import pymysql
import datetime

# // 啥是bson
from bson import json_util

global server, client


def p_type(obj):
    print(type(obj))


def get_mongo_conn():
    global server, client
    server = SSHTunnelForwarder(('132.232.81.70', 6000),
                                ssh_password='mimacs614',
                                ssh_username='root',
                                remote_bind_address=('localhost', 27017))
    server.start()
    atexit.register(shutdown)
    client = MongoClient('127.0.0.1', server.local_bind_port)


def shutdown():
    server.stop()


# class Article(dict):
#     def __init__(self):
#         self.id = 1
#
#     def __str__(self):
#         return str(self.__dict__)


def get_from_mongo(obj):
    db = client.get_database('iBlog_v2')
    post = {}
    # obj[]
    cate_name = obj['categories']
    post['isDraft'] = obj['status'] == 'draft'
    post['isLocal'] = True
    post['isActive'] = True
    post['commentsFlag'] = 0
    post['viewCount'] = obj['hits']
    post['labels'] = []
    post['alias'] = obj['title']
    post['title'] = obj['title']
    post['createTime'] = obj['created']
    post['modifyTime'] = obj['modified']
    post['publishTime'] = obj['modified']
    post['content'] = obj['content']
    post['__v'] = 0

    cate_collection = db.get_collection("category")
    cat_from_db = cate_collection.find_one({'cateName': cate_name})
    print(cat_from_db)
    if cat_from_db is None:
        cate = {'createTime': datetime.datetime.now(), 'modifyTime': datetime.datetime.now(), 'cateName': cate_name,
                'alias': cate_name, 'sequence': 0, '__v': 0}
        ret = cate_collection.insert_one(cate)
        # print('ret:',ret.inserted_id)
        # p_type(ret.inserted_id)
        cate_id = ret.inserted_id
        # print(ret.__dict__)
        pass
    else:
        cate_id = cat_from_db['_id']
        pass
    # post.name = 1
    # print(post)

    post['category'] = cate_id
    post_collection = db.get_collection("post")
    post_collection.insert_one(post)
    # post_collection.insert(
    #     {'labels': [], 'viewCount': 3, 'isLocal': True, 'isDraft': False, 'isActive': True, 'commentsFlag': 0,
    #      'createTime': datetime.datetime.now(), 'modifyTime': datetime.datetime.now(),
    #      'content': 'python',
    #      'title': 'python', 'category': bson.ObjectId('5bd27e95abb45c7371f36ed3'), 'alias': 'python',
    #      'publishTime': datetime.datetime.now(), '__v': 0}
    # )
    # res = post_collection.find().limit(10)
    # for r in res:
    #     param_obj = json.loads(json_util.dumps(r))
    #     print(param_obj)
    # # print(param_obj['_id'])


def data_from_mysql():
    conn = pymysql.connect(host='132.232.81.70',
                           user="root", passwd="mimaMysql614.", db="blog_jl")
    # 获取游标
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    row_count = cur.execute("""select * from t_contents
    """)
    rows = cur.fetchall()
    # for row in rows:
    #     print(row)
    #     p_type(row['modified'])
    cur.close()
    return rows


if __name__ == '__main__':
    get_mongo_conn()
    # p_type(bson.ObjectId('5bd27e95abb45c7371f36ed3'))
    # print(bson.ObjectId('5bd27e95abb45c7371f36ed3'))
    for row in data_from_mysql():
        print(row)
        p_type(row)
        get_from_mongo(row)
    pass
