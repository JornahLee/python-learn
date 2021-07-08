# pip3 install kafka-python


from kafka import KafkaConsumer
from kafka import KafkaClient

from kafka import KafkaProducer
from kafka import TopicPartition
from kafka import KafkaProducer
from kafka import KafkaAdminClient
from kafka.errors import KafkaError

host_port = '192.168.10.128:9092'
topic = 'vivo_ads_report_topic'

global top, producer, consumer


# 获取Lan值
def get_lan():
    partitions = producer.partitions_for(top)
    # sum = 0
    # for pt in partitions:
    #     p = TopicPartition(topic=top, partition=pt)
    #     beginning_offsets = consumer.committed(p)
    #     end_offsets = consumer.end_offsets([p])
    #     print(beginning_offsets, end_offsets)
    #
    #     sum = sum + end_offsets[p] - beginning_offsets
    #
    # return sum
    return partitions


def method_name():
    global top, producer, consumer
    cli = KafkaAdminClient(bootstrap_servers=host_port)
    print(cli.list_topics())


if __name__ == '__main__':
    method_name()
