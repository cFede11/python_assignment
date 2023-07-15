FROM python:3.9

WORKDIR /app

ENV AV_API_KEY="128S2A8V57C2W8UP"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
