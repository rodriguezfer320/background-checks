FROM python:3.10.0-slim

WORKDIR /home/fsu-bc-backend

COPY app ./app
COPY ./.env .
COPY requirements.txt .
COPY run.py .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]