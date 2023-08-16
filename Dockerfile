ARG FUNCTION_DIR /service_root
FROM python:3.11.4-slim

USER root
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install git curl -y
RUN pip install -U pip

RUN mkdir /service_root
WORKDIR /service_root
COPY . .

RUN pip install -U -r requirements.txt -q
RUN pip install -U git+https://github.com/huggingface/transformers.git -q
RUN python install-nlp-dependencies.py

ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["lambda_handler.handler"]
