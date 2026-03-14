#!/bin/bash

CONTAINERS_UP="/home/vlc/logs/container_up.txt"

echo "containers up" > "$CONTAINERS_UP"

sleep 30

STATUS_FILE="/home/vlc/logs/ready.txt"

sleep 2

echo "container ready" > "$STATUS_FILE"

tail -f /dev/null

