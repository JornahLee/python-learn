from kafka import KafkaProducer, KafkaConsumer, TopicPartition, KafkaAdminClient
from kafka.admin import NewPartitions, NewTopic
from kafka.errors import kafka_errors
import traceback
import json

topic = 'user-log'
topic2 = 'user-log'
group_id = 'user-log-group'
kwargs = {'bootstrap_servers': ['192.168.10.128:9092'], 'group_id': group_id}
dev_host = '192.168.10.128:9092'
test_host = 'test.rsth.plus:9092'
cli = KafkaAdminClient(bootstrap_servers=[test_host])
# cli = KafkaAdminClient(bootstrap_servers=[dev_host])


def get_partitions(p_topic: str):
    #     host_port = '192.168.10.128:9092'
    # topic = 'vivo_ad_group_save_topic'

    # pro = KafkaProducer(bootstrap_servers=['192.168.1.107:9092'],
    #                     key_serializer=lambda k: json.dumps(k).encode(),
    #                     value_serializer=lambda v: json.dumps(v).encode())
    # top = TopicPartition(topic, partition=[0, 1, 2, 3, 4])
    # pro.send(topic=topic2, value='woshishei')
    # con = KafkaConsumer(bootstrap_servers=['192.168.1.107:9092'])
    #  list_consumer_groups() 元组由消费者组名称和消费者组协议类型组成。
    l_group = cli.list_consumer_groups()
    for g_id in l_group:
        for par in cli.list_consumer_group_offsets(g_id[0]):
            # print(par)
            if par.topic == p_topic:
                print(g_id[0], ':', par)
    pass


def consume_rate(p_topic: str, consumer: KafkaConsumer):
    partitions = [TopicPartition(p_topic, p) for p in consumer.partitions_for_topic(p_topic)]
    print("start to cal offset:")
    # total
    toff = consumer.end_offsets(partitions)
    toff = [(key.partition, toff[key]) for key in toff.keys()]
    toff.sort()
    print("total offset: {}".format(str(toff)))
    # current
    coff = [(x.partition, consumer.committed(x)) for x in partitions]
    print('coff:', coff)
    coff.sort()
    print("current offset: {}".format(str(coff)))
    # cal sum and left
    toff_sum = sum([x[1] for x in toff])
    cur_sum = sum([x[1] for x in coff if x[1] is not None])
    left_sum = toff_sum - cur_sum
    print("kafka left: {}".format(left_sum))


# 扩展topic的分区数
def create_partition(t: str, partition_count):
    cli.create_partitions({t: NewPartitions(partition_count)})


def list_all_topics():
    print('list_topics:', cli.list_topics())


if __name__ == '__main__':
    # pro = KafkaProducer(bootstrap_servers=[dev_host],
    #                     key_serializer=lambda k: json.dumps(k).encode(),
    #                     value_serializer=lambda v: json.dumps(v).encode())
    # # top = TopicPartition('vivo_ad_report_es_topic', partition=[0, 1, 2, 3, 4])
    # pro.send(topic='vivo_ad_report_es_topic', value='')


    # cli.create_topics(NewTopic('vivo_ad_report_es_topic', 5,-1))
    # create_partition('vivo_ad_report_es_topic', 5)
    get_partitions('vivo_ad_report_es_topic')
    # consume_rate('vivo_ad_group_save_topic')
    # consumer = KafkaConsumer(bootstrap_servers=['192.168.10.128:9092'], group_id='advert_new')
    # consume_rate('vivo_ads_report_topic', consumer)
    pass
