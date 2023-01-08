FROM python:3.11.1-alpine3.17
LABEL maintainer="Sheharyar Ahmad"

# Set Environment Variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYCODE 1

# Set Working Directory
WORKDIR /code

# Copy Requirementss
COPY ./requirements.txt /tmp/requirements.txt

# Install Requirements
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Dependencies for Psycopg2
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

# Copy Project
COPY . /code/

# Expose the port 8000 for usage
EXPOSE 8000