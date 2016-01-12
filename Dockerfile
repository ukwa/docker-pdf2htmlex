FROM bwits/pdf2htmlex

# Idea is to wrap pdf2htmlex in a simple web service


RUN \
  apt-get update && \
  apt-get install -y python-flask gunicorn

ADD config.py /config.py
ADD service.py /service.py

CMD python /service.py