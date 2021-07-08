from pymongo import MongoClient
import atexit
from sshtunnel import SSHTunnelForwarder

import pymysql


def shutdown():
    server.stop()


def mysql():
    conn = pymysql.connect(host='132.232.81.70',
                           user="root", passwd="mimaMysql614.", db="blog_jl")
    # 获取游标
    cur = conn.cursor()
    row_count = cur.execute("""
        select * from t_contents limit 1;
    """)
    rows = cur.fetchall()
    all = []
    index = 0
    for r in rows:
        # all.append(r[0])
        # print(r[0],'-',index)
        print(r,'-',index)

        # print(type(r))


def mongo():
    global server
    server = SSHTunnelForwarder(('132.232.81.70', 6000),
                                ssh_password='mimacs614',
                                ssh_username='root',
                                remote_bind_address=('localhost', 27017))
    server.start()
    atexit.register(shutdown)
    client = MongoClient('localhost', server.local_bind_port)
    db = client.get_database('iBlog_v2')
    # for i in db.list_collections():
    #     print(i)
    post = db.get_collection(name="post")
    # post.update_one(filter={"title": "123"}, update={"$set": {"title": "666"}})
    # post.update_one()
    print(post.find_one())


if __name__ == '__main__':
    # mongo()
    mysql()
