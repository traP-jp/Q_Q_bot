FROM python:3.10-alpine

COPY Q_Q/ .

RUN pip install -r requirements.txt

WORKDIR /Q_Q

CMD ["python", "main.py"]


