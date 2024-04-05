#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 9 13:21:29 2023

@author: Stephen Mooney
"""

from dotenv import load_dotenv
import json
from kafka import KafkaConsumer
import os

load_dotenv('redpanda.env', override=True)

consumer = KafkaConsumer(
  bootstrap_servers=os.environ.get('RPK_BROKERS'),
  group_id="demo-group",
  auto_offset_reset="earliest",
  enable_auto_commit=False,
  consumer_timeout_ms=1000,
  value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

topic = "random-pii-text-anon"
consumer.subscribe(topic)

try:
    for message in consumer:
        topic_info = f"topic: {message.partition}|{message.offset})"
        message_info = f"key: {message.key}, {message.value}"

        original_json = message.value
        original_text = original_json['inputText']
        print(f"{message.value}")

except Exception as e:
    print(f"Error occurred while consuming messages: {e}")
finally:
    consumer.close()
