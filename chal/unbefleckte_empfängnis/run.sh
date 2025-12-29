#!/bin/bash
set -euxo pipefail

./ynetd -p 1996 'cat flag.txt' &
PID=$!

handler() { kill $PID; }
trap handler SIGINT

sleep 1

nc -4 localhost 1996 </dev/null >/dev/null
nc -6 localhost 1996 </dev/null >/dev/null

wait $PID

