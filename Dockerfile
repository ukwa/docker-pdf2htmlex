# Based on bwits/pdf2htmlex
# Idea is to wrap pdf2htmlex in a simple web service
#
# Dockerfile to build a pdf2htmlEx image
FROM debian:jessie

ENV REFRESHED_AT 20170418

# update debian source list
RUN \
    apt-get -qqy update && \
    apt-get -qqy install pdf2htmlex && \
    apt-get -qqy install python-dev python-flask gunicorn python-pip && \
    rm -rf /var/lib/apt/lists/*

RUN \
  pip install gevent

VOLUME /pdf/tmp
WORKDIR /pdf

ADD config.py /pdf/config.py
ADD service.py /pdf/service.py
ADD gunicorn.ini /pdf/gunicorn.ini.py

CMD gunicorn -c gunicorn.ini.py service:app

