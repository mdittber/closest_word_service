FROM python:3.7.2-slim

RUN mkdir /service
ADD . /service
WORKDIR /service
RUN  tar -xzvf glove.tar.gz
RUN  pip install -r requirements.txt
CMD  python api.py
