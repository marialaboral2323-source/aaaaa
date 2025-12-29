
FROM archlinux

RUN pacman -Sy --noconfirm sagemath
RUN pacman -S  --noconfirm python-pycryptodome

RUN useradd --create-home --shell /bin/bash ctf
WORKDIR /home/ctf

COPY ynetd /sbin/

COPY vuln.sage public.py flag.txt /home/ctf/

# sane defaults
RUN chmod 555 /home/ctf && \
    chown -R root:root /home/ctf && \
    chmod -R 000 /home/ctf/* && \
    chmod 500 /sbin/ynetd

RUN chmod 555 vuln.sage && \
    chmod 444 public.py && \
    chmod 444 flag.txt

# check whitelist of writable files/folders
RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/mail|/var/spool/mail)'
USER root

RUN ynetd -v

EXPOSE 1024
CMD ynetd -u ctf -lt 30 -t 630 -lm 4294967296 -sh y "PATH=/bin/ DOT_SAGE=/tmp/.sage/ sage /home/ctf/vuln.sage"
