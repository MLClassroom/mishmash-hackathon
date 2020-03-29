FROM ubuntu:18.04
FROM python:3.6


COPY . /app
WORKDIR /app

RUN apt-get update -y
RUN apt-get install python3-pip python3-dev -y
RUN apt-get install build-essential libpoppler-cpp-dev pkg-config -y
RUN apt-get install poppler-utils -y

RUN pip install -r requirements.txt
EXPOSE 8505


CMD streamlit run streamlit_app.py streamlit --server.port 8505
