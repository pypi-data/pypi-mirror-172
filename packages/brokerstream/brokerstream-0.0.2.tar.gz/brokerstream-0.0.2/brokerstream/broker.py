import json
from typing import TYPE_CHECKING
from kafka import KafkaProducer, KafkaConsumer
import traceback
import sys
from json import dumps, loads
from dataclasses import dataclass
from enum import Enum

class BrokerStreams():

    def __init__(self, consume_topic_name, producer_topic_name, broker_url):
        self.___producer = None
        self.___consumer = None
        self.___consume_topic_name = consume_topic_name
        self.___producer_topic_name = producer_topic_name
        self.___broker_url = broker_url
        self.__initiliaze()

    def __initiliaze(self):
        try:
            self.___consumer = KafkaConsumer(
                self.___consume_topic_name,
                bootstrap_servers=[self.___broker_url],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: loads(x.decode('utf-8'))
            )
            self.___producer = KafkaProducer(
                bootstrap_servers=[self.___broker_url],
                value_serializer=lambda x: dumps(x).encode('utf-8'),
                api_version=(0, 10, 1),
            )
        except Exception as e:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            print('\n')


    def send_message(self, data, topic_name=None):
        try:
            if not None:
                self.___producer.send(topic_name, data)
            else:
                self.___producer.send(self.___producer_topic_name, data)
        except Exception as e:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            print('\n')

    def consume_topic(self):
        try:
            return self.___consumer
        except Exception as e:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            print('\n') 


class Connectors(Enum):
    INSTA = 'INSTA'
    LINKEDIN = 'LINKEDIN'
    FACEBOOK = 'FACEBOOK'

class SearchType(Enum):
    FLN = 'FIRST_LAST_NAME'
    EMAIL = 'EMAIL'
    LINK = 'LINK'

@dataclass
class DtoBk:
    user_id: str
    search_type: list  
    connectors: list
    data: json