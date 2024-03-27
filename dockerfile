FROM python:3.11.7-slim

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /app/fee_calculator

CMD flask run --host 0.0.0.0 --port 5000

EXPOSE 5000