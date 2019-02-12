FROM python:3.7.2-slim

RUN mkdir /service
ADD . /service
WORKDIR /service
RUN  pip install -r requirements.txt
CMD  python app.py
