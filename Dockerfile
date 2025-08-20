FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Copy the necessary files into the Docker image
RUN mkdir /data
COPY users.csv /data/users.csv
COPY data/students.csv /data/students.csv
COPY data/distributions.csv /opt/defaults/distributions.csv

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Entrypoint that seeds /data/distributions.csv only if missing
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

ENV PORT=8080

CMD ["gunicorn", "-b", ":8080", "run:app"]