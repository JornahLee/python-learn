import pymysql
# $ pip3 install PyMySQL
# pymysql安装
# 使用的python版本为3.5
# Flask-MySQL使用了peewee；Flask-MySQL 会安装PyMySQL的最新版
# peewee使用 MySQLdb 或 pymysql 来连接MySQL数据库
# PyMySQL的最新版，不支持Python 2.7 和 3.5版本了（而我使用的是3.5版本），所以peewee报错
# 解决
# 不使用 Flask-MySQL 安装的PyMySQL最新版，指定PyMySQL版本为0.10.1，sudo pip3 install pymysql==0.10.1


# pymysql 默认不提交

def xxxx():
    global cur, conn, file
    try:
        conn = pymysql.connect(host='xx',
                               user="xx", passwd="xx", db="xxx")
        # 获取游标
        cur = conn.cursor()
        row_count = cur.execute("""
        select o.id,tca.id from orders o 
        inner join xxxx oap on o.id=oap.order_id 
        inner join xxxx tca on o.id=tca.order_id
        where o.order_status = 'TRIAL' and o.updated_at > '2020-11-01 00:29:27'
        """)
        rows = cur.fetchall()
        file = open("xxx.txt", "w+")
        for i in rows:
            order_id = i[0]
            time_change_audits_id = i[1]
            process(cur, file, order_id, time_change_audits_id)
        # 需要commit更新才会生效
        conn.commit()
    finally:
        if file is not None:
            file.close()
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def process(cur_param, file_order_id, order_id, time_change_audits_id):
    # 导出所有订单id
    file_order_id.write(str(order_id) + ',')
    cur_param.execute("""
    update xxx set change_type='AWARD' , order_id=null
    where change_type='BUY' and order_id=%s
    """, order_id)
    cur.execute("""
    delete from xxxx where order_id=%s
    """, order_id)



global log_file
if __name__ == '__main__':
    log_file = open("xxx.log", "w+")
    xxxx()
