#!/bin/bash

echo $'\n\x1b[1;31mDO NOT RUN THIS SCRIPT ON YOUR OWN MACHINE\x1b[0m'
echo $'\x1b[1;33mIT WILL BREAK THINGS\x1b[0m  \x1b[1;35mYOU HAVE BEEN WARNED\x1b[0m'
read -p $'\x1b[32mto continue anyway, type "YES":\x1b[0m ' yesno
if [ "$yesno" != "YES" ]; then exit; fi

grep -q 'Debian GNU/Linux 13' /etc/issue || { echo expecting trixie; exit 1; }

set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive
apt update
apt upgrade -y

YNETD=ynetd-2024.02.17
apt install -y build-essential
wget https://yx7.cc/code/ynetd/$YNETD.tar.xz
tar -xvf $YNETD.tar.xz
make -C$YNETD -j$(nproc)
ln -s $YNETD/ynetd .

LINUX=linux-6.18.2
apt install -y bc bison flex libssl-dev libelf-dev libdw-dev debhelper
wget https://cdn.kernel.org/pub/linux/kernel/v6.x/$LINUX.tar.xz
tar -xvf $LINUX.tar.xz
cd $LINUX
sed -Ei 's/(#define MAX_SYNCOOKIE_AGE\s+)2/\11111/' include/net/tcp.h
cp /boot/config-$(uname -r) .config
make olddefconfig
make -j$(nproc) bindeb-pkg
cd -
dpkg -i linux-image-*.deb

apt install -y iptables-persistent
cat >/etc/iptables/rules.v4 <<EOF
*filter
-A INPUT -p tcp --dport 1996 --tcp-flags SYN SYN ! -s 127.0.0.1 -j DROP
COMMIT
EOF
echo 'net.ipv4.tcp_syncookies=2' >/etc/sysctl.d/cookies.conf
cat >/etc/iptables/rules.v6 <<EOF
*filter
-A INPUT -p tcp --dport 1996 --tcp-flags SYN SYN ! -s       ::1 -j DROP
COMMIT
EOF

cat >/etc/systemd/system/unbefleckt.service <<EOF
[Unit]
After=network.target
[Install]
WantedBy=multi-user.target
[Service]
WorkingDirectory=/root/
ExecStart=/root/run.sh
EOF
systemctl enable unbefleckt

reboot

