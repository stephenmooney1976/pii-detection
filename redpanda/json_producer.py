#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 9 13:21:29 2023

@author: Stephen Mooney
"""

from dotenv import load_dotenv
import json
from kafka import KafkaProducer
import os

""" read in information about started redpanda environment """
load_dotenv('redpanda.env', override=True)

print( os.environ.get('RPK_BROKERS'))
""" create producer """
producer = KafkaProducer(
    bootstrap_servers = os.environ.get('RPK_BROKERS'),
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

topic = "random-pii-text"

def on_success(metadata):
  print(f"Message produced to topic '{metadata.topic}' at offset {metadata.offset}")

def on_error(e):
  print(f"Error sending message: {e}")

""" read in OpenAI generated PII """
with open('../data/pii_records.json') as f:
  l_json_data = json.load(f)

""" push messages to topic from OpenAI """
for ii in range(len(l_json_data)):
  msg = {'recordId': f"{ii}", 'inputText': l_json_data[ii]['inputs']}
  future = producer.send(topic, msg)
  future.add_callback(on_success)
  future.add_errback(on_error)

""" flush and close producer """
producer.flush()
producer.close()
