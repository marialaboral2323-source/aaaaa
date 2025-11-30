#!/bin/bash
cd /workspace/challenge
echo "1" | timeout 10s nc dyn06.heroctf.fr 13683
