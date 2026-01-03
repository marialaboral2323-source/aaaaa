#!/bin/bash

IP_ADDR=$(ip addr show eth0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)

IFS='.' read -ra ADDR <<< "$IP_ADDR"
let "ADDR[3]-=1"
if [ ${ADDR[3]} -lt 0 ]; then
    ADDR[3]=255
fi
NEIGHBOR_IP="${ADDR[0]}.${ADDR[1]}.${ADDR[2]}.${ADDR[3]}"

cat > /etc/bird/bird.conf <<EOF
log syslog all;

router id $IP_ADDR;

protocol bgp dreamhack {
    local as 65002;
    source address $IP_ADDR;
    graceful restart on;
    neighbor $NEIGHBOR_IP as 65001;
    import all;
    export all;
}

protocol kernel {
        scan time 60;
        import none;
#       export all;   # Actually insert routes into the kernel routing table
}

protocol device {
        scan time 60;
}

EOF

bird -c /etc/bird/bird.conf -d &

exec /usr/sbin/sshd -D
