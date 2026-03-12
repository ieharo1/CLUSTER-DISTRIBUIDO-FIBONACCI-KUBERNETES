FROM python:3.11

WORKDIR /worker

COPY worker /worker

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "worker.py"]

