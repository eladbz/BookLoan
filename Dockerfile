FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["exec gunicorn --bind :${PORT:-8000} app:app"]