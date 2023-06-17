FROM python:3.10-alpine

COPY Q_Q/ .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]


