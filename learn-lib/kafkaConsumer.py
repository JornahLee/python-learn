# pip3 install kafka-python


from kafka import KafkaConsumer

from kafka import KafkaProducer
from kafka import TopicPartition
from kafka import KafkaProducer
from kafka.errors import KafkaError

host_port = '192.168.10.128:9092'
topic = 'vivo_ads_report_topic'


# 获取Lan值
def get_lan():
    partitions = producer.partitions_for(top)
    sum = 0
    for pt in partitions:
        p = TopicPartition(topic=top, partition=pt)
        beginning_offsets = consumer.committed(p)
        end_offsets = consumer.end_offsets([p])
        print(beginning_offsets, end_offsets)

        sum = sum + end_offsets[p] - beginning_offsets

    return sum


def method_name():
    global top, producer, consumer
    # https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html
    bootstrap_server = [host_port]
    top = topic
    producer = KafkaProducer(bootstrap_servers=bootstrap_server)
    consumer = KafkaConsumer(top,
                             group_id='my-groups',
                             bootstrap_servers=bootstrap_server)
    print("123123")
    # test
    for message in consumer:
        # message value and key are raw bytes -- decode if necessary!
        # e.g., for unicode: `message.value.decode('utf-8')`
        print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                             message.offset, message.key,
                                             message.value))
        print("======")
        print(get_lan())


def send():
    producer = KafkaProducer(
        bootstrap_servers=[host_port]
    )
    future = producer.send("test", b"this is a python to kafka")
    try:
        record = future.get(timeout=10)
        print(record)
    except KafkaError as e:
        print(e)


def comsu():
    consumer = KafkaConsumer(
        "test",
        bootstrap_servers=[
            host_port
        ]
    )
    for each in consumer:
        print("%s:%d:%d: key=%s value=%s" % (
            each.topic, each.partition,
            each.offset, each.key, each.value
        ))


if __name__ == '__main__':
    comsu()
