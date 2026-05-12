FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    sqlite3

WORKDIR /app
COPY . /app

CMD ["python3", "game.py"]