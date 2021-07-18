FROM python:3.9.5-alpine3.12

WORKDIR /app

COPY requirements.txt requirements.txt

COPY pecheck.py pelib.py ./

RUN pip3 install -r requirements.txt --no-cache-dir

ENTRYPOINT ["python", "sentinel.py"]
