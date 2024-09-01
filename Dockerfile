FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl inetutils-ping

COPY requirements.prod.txt gunicorn_config.py wsgi.py ./
RUN pip install -r requirements.prod.txt

COPY . .

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
CMD ["gunicorn", "--config", "gunicorn_config.py", "wsgi:app"]
