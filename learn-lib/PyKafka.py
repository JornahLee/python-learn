from kafka import KafkaProducer, KafkaConsumer, TopicPartition, KafkaAdminClient
from kafka.admin import NewPartitions
from kafka.errors import kafka_errors
import traceback
import json

topic = 'user-log'
topic2 = 'user-log'
group_id = 'user-log-group'
kwargs = {'bootstrap_servers': ['192.168.1.107:9092'], 'group_id': group_id}


def produce():
    cli = KafkaAdminClient(bootstrap_servers=['192.168.1.107:9092'])
    # cli.create_partitions({topic: NewPartitions(10)})
    # pro = KafkaProducer(bootstrap_servers=['192.168.1.107:9092'],
    #                     key_serializer=lambda k: json.dumps(k).encode(),
    #                     value_serializer=lambda v: json.dumps(v).encode())
    # top = TopicPartition(topic, partition=[0, 1, 2, 3, 4])
    # pro.send(topic=topic2, value='woshishei')
    cli.list_topics()
    cli.list_topics()
    print('list_topics:', cli.list_topics())
    # con = KafkaConsumer(bootstrap_servers=['192.168.1.107:9092'])
    #  list_consumer_groups() 元组由消费者组名称和消费者组协议类型组成。
    l_group = cli.list_consumer_groups()
    print('list_consumer_groups:', l_group)
    print('list_consumer_group_offsets:', cli.list_consumer_group_offsets(group_id))
    for g_id in l_group:
        print(' g_id[0]:', g_id[0])
        print(cli.list_consumer_group_offsets(g_id[0]))

        # print(t)
        # consume_rate(con, t)
    pass


def consume_rate(consumer: KafkaConsumer, topic1):
    partitions = [TopicPartition(topic1, p) for p in consumer.partitions_for_topic(topic1)]
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


if __name__ == '__main__':
    produce()
