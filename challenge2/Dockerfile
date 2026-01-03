FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m pwn
WORKDIR /home/pwn

COPY chall /home/pwn/chall

# 로컬 재현용 더미 플래그 (원격 진짜 플래그는 서버 Dockerfile이 따로 관리)
ARG FLAG="DH{test_flag}"
RUN echo -n "$FLAG" > /home/pwn/flag

RUN chown -R pwn:pwn /home/pwn && \
    chmod 755 /home /home/pwn && \
    chmod 755 /home/pwn/chall && \
    chmod 444 /home/pwn/flag

EXPOSE 1337

USER pwn
CMD ["socat","TCP-LISTEN:1337,reuseaddr,fork","EXEC:/home/pwn/chall,pty,stderr,setsid,sigint,sane"]
