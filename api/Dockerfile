FROM python:3.6

RUN mkdir /service
ADD . /service
WORKDIR /service
RUN  tar -xzvf glove.tar.gz
RUN  pip install -r requirements.txt
CMD  python api.py
