FROM python:3.10-alpine

WORKDIR /srv

COPY Q_Q/requirements.txt /srv/requirements.txt
RUN pip install -r requirements.txt

COPY Q_Q/main.py /srv/main.py

CMD ["sleep 5000"]
