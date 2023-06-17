FROM python:3.10-alpine

WORKDIR /srv

COPY Q_Q/ /srv/

RUN pip install -r requirements.txt

COPY Q_Q/main.py /srv/main.py

CMD ["python", "main.py"]


