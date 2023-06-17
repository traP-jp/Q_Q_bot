FROM python:3.10-alpine

WORKDIR /srv

COPY Q_Q/ /srv/

RUN pip install -r requirements.txt

WORKDIR /srv/Q_Q

CMD ["python", "main.py"]


