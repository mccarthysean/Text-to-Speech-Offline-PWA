FROM python:3.12-slim

WORKDIR /app

COPY requirements.prod.txt requirements.prod.txt
RUN pip install -r requirements.prod.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
