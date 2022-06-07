FROM python:3.7

EXPOSE 7200

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip setuptools wheel nltk

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

RUN chmod 777 /app/wait-for-it.sh

CMD [ "python", "manage.py", "run" ]