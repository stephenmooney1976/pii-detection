#!/usr/bin/env python

from dotenv import load_dotenv
import json
import openai

load_dotenv('.env')

model_engine = "text-davinci-003"
num_samples = 10

prompt = "Generate text with a bunch of random PII. Please do not use name John Smith. or Jane Doe. Please use a random name."

output_results = list()

for ii in range (num_samples):
  completion = openai.Completion.create(
          engine=model_engine,
         prompt=prompt,
         max_tokens=2048,
         n=1,
         stop=None,
         temperature=0.5
   )

  response_text = completion.choices[0].text.strip()
  output_results.append(dict(inputs=response_text))

with open('data/pii_records.json', 'w', encoding='utf-8') as f:
  json.dump(output_results, f, ensure_ascii=True, indent=2)
