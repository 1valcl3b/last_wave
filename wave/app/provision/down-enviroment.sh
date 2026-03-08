#!/bin/bash

set +e  # não parar se der erro

CLIENT="client"
SERVER="server"

SWITCH_CLIENT="s1"
SWITCH_FILE="/tmp/ultimo_switch.txt"
SWITCH_SERVER=$(tr -d '\n' < "$SWITCH_FILE")

# Removendo portas dos switches
sudo ovs-vsctl --if-exists del-port $SWITCH_CLIENT veth-client-sw
sudo ovs-vsctl --if-exists del-port $SWITCH_SERVER veth-server-sw

# apagando as interfaces 
sudo ip link delete client 2>/dev/null
sudo ip link delete server 2>/dev/null

# Removendo links de namespace
sudo rm -f /var/run/netns/$CLIENT
sudo rm -f /var/run/netns/$SERVER

