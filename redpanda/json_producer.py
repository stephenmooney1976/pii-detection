#!/usr/bin/env python

from dotenv import load_dotenv
import json
from kafka import KafkaProducer
import os
import time

""" read in information about started redpanda environment """
load_dotenv('redpanda.env')

""" create producer """
producer = KafkaProducer(
    bootstrap_servers = os.environ.get('RPK_BROKERS'),
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

topic = "orders"

def on_success(metadata):
  print(f"Message produced to topic '{metadata.topic}' at offset {metadata.offset}")

def on_error(e):
  print(f"Error sending message: {e}")

""" read in OpenAI generated PII """
with open('../data/pii_records.json') as f:
  l_json_data = json.load(f)

""" push messages to toic from OpenAI """
for ii in range(len(l_json_data)):
  msg = dict(id=ii, inputs=l_json_data[ii]['inputs'])
  future = producer.send(topic, msg)
  future.add_callback(on_success)
  future.add_errback(on_error)
  time.sleep(0.100) #

""" flush and close producer """
producer.flush()
producer.close()