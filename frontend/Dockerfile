FROM python:3.10.2-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - 

RUN apt-get update -y && \
    apt-get install -y netcat && \
    apt-get install -y nodejs && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

RUN echo "NODE Version:" && node --version
RUN echo "NPM Version:" && npm --version

COPY ./entrypoint.sh .

RUN chmod +x /code/entrypoint.sh

COPY . .

ENTRYPOINT ["/code/entrypoint.sh"]
