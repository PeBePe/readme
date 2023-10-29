FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=readme.settings \
    PORT=8000 \
    WEB_CONCURRENCY=2

# Install system packages required Django.
RUN apt-get update --yes --quiet \
&& apt-get install --yes --quiet --no-install-recommends \
&& apt-get install -y build-essential curl \
&& curl -sL https://deb.nodesource.com/setup_16.x | bash - \ 
&& apt-get install -y nodejs --no-install-recommends \
&& rm -rf /var/lib/apt/lists/* \ 
&& apt-get clean 

RUN addgroup --system django \
    && adduser --system --ingroup django django

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy project code
COPY . .

RUN SECRET_KEY=nothing python manage.py tailwind install --no-input;
RUN SECRET_KEY=nothing python manage.py tailwind build --no-input;
RUN SECRET_KEY=nothing python manage.py collectstatic --no-input;

# Run as non-root user
RUN chown -R django:django /app
USER django

# Run application
# CMD gunicorn readme.wsgi:application