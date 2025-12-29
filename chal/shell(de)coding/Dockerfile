# see compose.yml

FROM debian:trixie

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 python3-pip \
    && rm -rf /var/lib/apt/lists/
RUN pip3 install --break-system-packages unicorn

RUN useradd --create-home --shell /bin/bash ctf

COPY ynetd /sbin/
COPY emu.py flag.txt /home/ctf/
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chown root /home/ctf/flag.txt && \
    chmod 505 /home/ctf/emu.py && \
    chmod 444 /home/ctf/flag.txt && \
    chmod 500 /sbin/ynetd

RUN find / -ignore_readdir_race -path /sys -prune -o -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -exec rm {} \;
USER ctf
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'

USER root

RUN ynetd -v

WORKDIR /home/ctf
EXPOSE 1024
CMD ynetd -t 600 -lt 300 -lm -1 /home/ctf/emu.py
