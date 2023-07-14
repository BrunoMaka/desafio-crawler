FROM python:3.9

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "django_crawler/manage.py", "runserver", "0.0.0.0:8000"]
