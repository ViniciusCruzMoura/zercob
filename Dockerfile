FROM python:3.13

WORKDIR /usr/src

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", " \
    echo 'Iniciando a Aplicação... Aguarde 10 Segundos...'; sleep 10; \
    python manage.py migrate ; \
    python manage.py collectstatic --noinput ; \
    celery -A core worker --beat --scheduler django --loglevel=info --concurrency=2 & \
    gunicorn --config gunicorn-cfg.py core.wsgi \
"]
