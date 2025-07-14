FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Copy the necessary files into the Docker image
RUN mkdir /data
COPY users.csv /data/users.csv
COPY data/students.csv /data/students.csv
COPY data/distributions.csv /data/distributions.csv

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

CMD ["gunicorn", "-b", ":8080", "run:app"]