FROM python:3.11
LABEL authors="vitaliy_vorobyev"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .