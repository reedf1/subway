FROM python:3.8-slim
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY app/subway.py /usr/local/bin/subway
RUN chmod +rx /usr/local/bin/subway
ENTRYPOINT ["/usr/local/bin/subway"]
CMD ["--help"]