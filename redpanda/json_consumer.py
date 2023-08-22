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
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

from presidio_analyzer import AnalyzerEngine

from entity_recognizers import TransformerRecognizer

operators = {
    "DEFAULT": OperatorConfig("replace", {"new_value": "<ANONYMIZED>"}),
    "PHONE_NUMBER": OperatorConfig(
        "mask",
        {
            "type": "mask",
            "masking_char": "*",
            "chars_to_mask": 12,
            "from_end": True,
        },
    ),
    "US_SSN": OperatorConfig(
        "mask",
        {
            "type": "mask",
            "masking_char": "#",
            "chars_to_mask": 11,
            "from_end": False
        }
    ),
    "TITLE": OperatorConfig("redact", {}),
}

model_dir = '../bert-base-NER' # directory that we downloaded HuggingFace to above

xfmr_recognizer = TransformerRecognizer(model_dir)
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(xfmr_recognizer)
anonymizer_engine = AnonymizerEngine()

load_dotenv('redpanda.env', override=True)

consumer = KafkaConsumer(
  bootstrap_servers=os.environ.get('RPK_BROKERS'),
  group_id="demo-group",
  auto_offset_reset="earliest",
  enable_auto_commit=False,
  consumer_timeout_ms=1000,
  value_deserializer=lambda m: json.loads(m.decode('ascii'))
)

topic = "random-pii-text"
consumer.subscribe(topic)

anonymized_json = list()

try:
    for message in consumer:
        topic_info = f"topic: {message.partition}|{message.offset})"
        message_info = f"key: {message.key}, {message.value}"

        original_json = message.value

        analyzer_results = analyzer.analyze(text=original_json['inputText'],
                                                            language="en")

        anonymized_text = anonymizer_engine.anonymize(text=original_json['inputText'],
                                                      analyzer_results=analyzer_results,
                                                      operators=operators)

        original_json['outputText'] = anonymized_text.text


        anonymized_json.append(original_json)

except Exception as e:
    print(f"Error occurred while consuming messages: {e}")
    print(type(e).__name__)
finally:
    consumer.close()

aj = anonymized_json[:5]

for ii in aj:
  print(str(ii))