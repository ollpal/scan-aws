FROM python:3.5

ENV http_proxy http://172.17.42.1:3128/
ENV https_proxy http://172.17.42.1:3128/

RUN apt-get update && apt-get install -y python3-setuptools graphviz

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "python", "./app.py" ]
