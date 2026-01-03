FROM ubuntu@sha256:104ae83764a5119017b8e8d6218fa0832b09df65aae7d5a6de29a85d813da2fb

RUN apt-get update && \
    apt-get install -y --no-install-recommends socat ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 ctf

WORKDIR /app
COPY echo-back /app/echo-back
COPY flag.txt /app/flag.txt

RUN chmod 555 /app/echo-back && chmod 444 /app/flag.txt

USER ctf
EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/app/echo-back,stderr"]
