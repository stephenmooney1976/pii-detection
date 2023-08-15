# Personally Identifiable Information (PII) detection using Presidio, BERT NER, and Kafka (Redpanda)

## Summary
Provided here are a few python artifacts to demonstrate the ability to extend Presidio with a Named Entity Recogntion model.
This also integrates with a Kafka consumer at this point. Soon there will be examples of how to integrate this as in-stream
transformation and integration with real-time databases.

Technologies used in this repository are:
- Python
- Jupyter Lab
- Presidio
- BERT / LLM NER
- Docker
- Redpanda
- Shell Scripting

`blog-part1-pii-kafka.ipynb` is a Jupyter notebook associated with a blog post that discusses PII and how to replace it in 
unstructured text. This notebook has a full implementation of the blog post and has almost every artifact of this repository
integrated therewithin.

`generate-random-pii-json.py` is a program that I used to generate records with random PII within them. Using OpenAI, it
requires that you set up an OpenAI API key. These go in a file named .env and get pulled in with dotenv. The format of 
.env is as follows:

```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

`sagemaker-check.py` is a program that I used to check IAM roles for SageMaker. I am not using SageMaker at the moment for this
blog/demo, but may come back to it.

`redpanda/entity_recognizers.py` is a python implementation of the EntityRecognizer for NER transformers. This is exactly the
same as the code in the Jupyter notebook mentioned above.

`redpnada/json_consumer.py` is a Kafka consumer built to apply PII detection and anonymization at runtime. This code is the
same as the code in the Jupyter notebook metoned above.

`redpanda/json_producer.py` is a Kafka JSON producer that reads in the randomly generated PII file under `data` and publishes
these records as messages to a Kafka topic.

`redpanda/start_container.bash` is a bash script that starts Redpanda and creates a file named `redpanda.env` which is then used
by `json_consumer.py` and `json_producer.py` to locate the cluster broker(s). Redpanda requires Docker to be installed, and I am
making use of the `rpk` command. Documentation on `rpk` can be found [here](https://docs.redpanda.com/docs/get-started/rpk-install/).

`redpanda/stop_container.bash` is a bash script that stops Redpanda and cleans up Docker resources.

## Getting started

Clone the repository, set up the virtual environment, and install the required packages

```
git clone git@github.com:stephenmooney1976/pii-detection.git
cd pii-detection
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

_Install rpk. Follow the instructions here to get rpk up and running: https://docs.redpanda.com/docs/get-started/rpk-install/_

_Install Docker: https://docs.docker.com/engine/install/_

Now copy your OpenAI API key into the `.env` file, and save the file. It should send up looking something like

`OPENAI_API_KEY=sk-`

Install Jupyter Lab if you haven't already. [here](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html) is
the link to the Jupyter installation documentation.

```
pip install -U jupyterlab
#or
conda install -c conda-forge jupyterlab
```

## Test it out

This can all be executed by running the jupyter notebook by opening jupyter lab from the command line:

```
jupyter-lab
```

Then by opening the notebook `blog-part1-pii-kafka.ipynb` and running the code within.

This can also be done by using the commmand line:

```
# start Redpanda
cd redpanda
./start_container.bash
python3 json_producer.py
python3 json_consumer.py
./stop_container.bash
```