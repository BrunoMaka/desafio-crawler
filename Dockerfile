# NÂO UTILIZAR

FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python django_crawler/manage.py makemigrations
RUN python django_crawler/manage.py migrate

EXPOSE 8000

CMD ["python", "django_crawler/manage.py", "runserver", "0.0.0.0:8000"]
