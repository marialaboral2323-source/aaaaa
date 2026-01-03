FROM python:3.11-slim

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app.py /app/
COPY flag.txt /app/

RUN chmod 444 /app/flag.txt && \
    chmod 555 /app/app.py

RUN useradd -m -s /bin/bash pyjail
USER pyjail

EXPOSE 8000

CMD ["socat", "TCP-LISTEN:8000,reuseaddr,fork", "EXEC:'python3 /app/app.py'"]