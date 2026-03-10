#!/bin/bash

set +e

CLIENT="client"
SERVER="server"

CLIENT_IP="$1/24"
SERVER_IP="$2/24"

SWITCH_CLIENT="s1"

SWITCH_FILE="/tmp/ultimo_switch.txt"
SWITCH_SERVER=$(tr -d '\n' < "$SWITCH_FILE")

DNS_IP=$2

# Pegando PID de cada container
CLIENT_PID=$(docker inspect -f '{{.State.Pid}}' $CLIENT)
SERVER_PID=$(docker inspect -f '{{.State.Pid}}' $SERVER)

sudo mkdir -p /var/run/netns
sudo ln -sf /proc/$CLIENT_PID/ns/net /var/run/netns/$CLIENT
sudo ln -sf /proc/$SERVER_PID/ns/net /var/run/netns/$SERVER

# Criando os veth pairs
sudo ip link delete client 2>/dev/null || true
sudo ip link delete server 2>/dev/null || true

sudo ip link add veth-client type veth peer name client
sudo ip link add veth-server type veth peer name server

# Movendo uma ponta para os containers
sudo ip link set veth-client netns $CLIENT
sudo ip link set veth-server netns $SERVER

# Conectando aos SWitchs do Mininet
sudo ovs-vsctl add-port $SWITCH_CLIENT client
sudo ovs-vsctl add-port $SWITCH_SERVER server

# Subindo as interfaces client e server
sudo ip link set client up
sudo ip link set server up

# Configurando IPs dentro dos containers

sudo ip netns exec $CLIENT ip link set lo up
sudo ip netns exec $CLIENT ip addr add $CLIENT_IP dev veth-client
sudo ip netns exec $CLIENT ip link set veth-client up

sudo ip netns exec $SERVER ip link set lo up
sudo ip netns exec $SERVER ip addr add $SERVER_IP dev veth-server
sudo ip netns exec $SERVER ip link set veth-server up

docker exec -it client bash -c 'echo "'$DNS_IP' server" | sudo tee -a /etc/hosts'