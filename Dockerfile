FROM python:3.11.4-bullseye

USER root
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y
RUN pip install -U pip

RUN mkdir service_root
WORKDIR service_root
COPY . .

RUN pip install -U -r requirements.txt -q
RUN pip install -U git+https://github.com/huggingface/transformers.git -q
RUN python install-nlp-dependencies.py

CMD ["python3", "-u", "rest_service.py"]
