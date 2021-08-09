FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir pipenv
RUN pipenv install --system --ignore-pipfile --deploy --clear
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=zen
CMD ["python3", "zen.py", "runserver", "0.0.0.0:8000"]
