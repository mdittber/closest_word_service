FROM python:3.6

RUN mkdir /service
ADD . /service
WORKDIR /service
RUN  pip install -r requirements.txt
CMD  python app.py
