FROM python:3.8-slim
LABEL maintainer 'Juracy Filho <juracy at gmail.com>'
ENV PYTHONUNBUFFERED 1

RUN pip install redis==2.10.5

WORKDIR /worker
COPY . /worker

ENTRYPOINT ["/usr/local/bin/python"]
