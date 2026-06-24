FROM python:3.11

WORKDIR /app

COPY code/requirements.txt .
RUN pip install -r requirements.txt

# Install flower for Celery monitoring
RUN pip install flower

COPY code/ .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]