import pymysql


def get_object_from_row(current_row, description):
    entity = {}
    for index, col in enumerate(description):
        entity[col[0]] = current_row[index]
    return entity


class DbHelper:
    def __init__(self, host, user, passwd, db):
        self.conn = pymysql.connect(host='132.232.81.70',
                                    user="root", passwd="mimaMysql614.", db="game_hub")

    def query(self, sql: str):
        ret = []
        with self.conn.cursor() as cur:
            cur.execute(sql)
            for row in cur.fetchall():
                ret.append(get_object_from_row(row, cur.description))
        return ret

    def update(self, sql: str):
        with self.conn.cursor() as cur:
            cur.execute(sql)
        pass

    def insert(self, sql: str):
        with self.conn.cursor() as cur:
            cur.execute(sql)
        pass

    def commit(self):
        self.conn.commit()
