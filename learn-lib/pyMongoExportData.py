from pymongo import MongoClient

# client = MongoClient('192.168.10.36')
client = MongoClient('test.rsth.plus')
db = client.admin.authenticate('admin', '123456')
db = client.get_database('smartad')
calculate_column = db.get_collection(name="calculate_column")


def mongo():
    # mongodb://admin:123456@test.rsth.plus:27017/basic?authSource=admin
    # client = MongoClient('admin:123456@test.rsth.plus:27017/basic?authSource=admin')
    # client = MongoClient('test.rsth.plus')

    # smartad = client.smartad
    # print(smartad.get_collection('kpi').find_one())
    docs = []
    index = 0
    with open('data-mongo.txt', encoding='utf-8') as f:
        source = f.readline()
        while source:
            print(source)
            split = source.split()
            doc = {
                "customColumnName": split[0],
                "calcRule": split[1],
                "resultInterceptorCode": split[2],
                "calcParamCols": split[3],
                "order": index
            }
            index += 1
            docs.append(doc)
            source = f.readline()
    # db.calculate_column.insert({
    #     customColumnName:"123",calcRule:"123",calcParamCols:"123",resultInterceptorCode:"123"
    # })
    calculate_column.insert_many(docs)


def mongo2():
    docs = []
    index = 0
    fields = ["actualIncome", "ltv60", "ltv45", "ltv30", "ltv15", "ltv7", "retain7d", "retain3d", "retain2d"]
    for field in fields:
        doc = {
            "customColumnName": field,
            "calcRule": field,
            "resultInterceptorCode": "none",
            "calcParamCols": field,
            "order": index
        }
        index += 1
        docs.append(doc)
    # db.calculate_column.insert({
    #     customColumnName:"123",calcRule:"123",calcParamCols:"123",resultInterceptorCode:"123"
    # })
    calculate_column.insert_many(docs)
    pass


def plus_all():
    li = [5.15, 1.69, 7.28, 7.18, 16.37,
          10.65,
          3.12, 14.79,
          14.32,3.14,12.95,8.98,
          6.24,
          6.16,27.2,
          24.37,
          21.08
        ,12312313,12312313,12312313,12312313,12312313,12312313,12312313,12312313,12312313,12312313,12312313]
    pass


if __name__ == '__main__':
    # print('222   111 333'.split())
    mongo2()
