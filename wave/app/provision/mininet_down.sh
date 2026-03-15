#!/bin/bash

set -e

sudo mn -c &> /dev/null

sudo pkill -f net-linear.py

sudo pkill -f net-tree.py

sudo rm -f /tmp/ultimo_switch.txt

sleep 3

echo "[WAVE 🌊] Mininet stopped"
