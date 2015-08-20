FROM python:3.5

ENV https_proxy http://172.17.42.1:3128/

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD [ "python", "./app.py" ]
