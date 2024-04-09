FROM python:3.10-alpine
#FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR .

COPY . .


EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
