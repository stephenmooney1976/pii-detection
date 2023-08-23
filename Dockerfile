FROM python:3.11.4-slim-bullseye AS os_updates

USER root
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install --no-install-recommends build-essential curl git -y \
    && apt-get clean \
    && apt-get autoclean \
    && apt-get autoremove -y \ 
    && rm -rf /var/lib/apt/lists/*

from os_updates AS rust_install

# Get Rust
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH /root/.cargo/bin:$PATH

RUN pip install --no-cache-dir -U pip

from rust_install 

RUN mkdir service_root
WORKDIR service_root
COPY . .

RUN pip install --no-cache-dir -U -r requirements.txt -q \
    && pip install --no-cache-dir -U git+https://github.com/huggingface/transformers.git -q \
    && python install-nlp-dependencies.py    

CMD ["python3", "-u", "rest_service.py"]
