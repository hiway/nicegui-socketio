FROM python:3.11.3-slim

LABEL maintainer="Harshad Sharma <harshad@sharma.io>"

RUN apt update && apt install curl -y

# Poetry for Python dependency management
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    cd /usr/local/bin && \
    ln -s ~/.local/bin/poetry && \
    poetry config virtualenvs.create false

WORKDIR /app

COPY main.py \
    client.py \
    Procfile \
    pyproject.toml \
    README.md \
    LICENSE \
    ./ 

RUN poetry install --no-root

EXPOSE 8080

CMD fallocate -l 1024M /_swapfile && \
    mkswap /_swapfile && \
    chmod 0600 /_swapfile && \
    swapon /_swapfile && \
    honcho start
