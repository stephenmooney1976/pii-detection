#!/usr/bin/env python

from huggingface_hub import snapshot_download

repo_id = 'dslim/bert-base-NER'
model_id = repo_id.split('/')[-1]
 
snapshot_download(repo_id=repo_id, local_dir=model_id)

import spacy
spacy.cli.download(model="en_core_web_lg")
