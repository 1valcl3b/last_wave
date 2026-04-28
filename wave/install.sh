#!/usr/bin/env bash

set -Eeuo pipefail

LOG_FILE="install.log"
FORCE=false

for arg in "$@"; do
    case $arg in
        --force)
            FORCE=true
            shift
            ;;
    esac
done

exec > >(tee -i "$LOG_FILE")
exec 2>&1

export DEBIAN_FRONTEND=noninteractive

echo "===> WAVE Installer (README-aligned)"
echo "===> Log: $LOG_FILE"

fail() {
    echo "ERROR: $1"
    exit 1
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

version_ge() {
    printf '%s\n%s' "$2" "$1" | sort -C -V
}

require_sudo() {
    if ! sudo -n true 2>/dev/null; then
        echo "Sudo required"
        sudo true
    fi
}


# verificar OS


echo "===> Checking OS"

if ! grep -qi ubuntu /etc/os-release; then
    fail "Only Ubuntu is supported"
fi

UBUNTU_VERSION=$(lsb_release -rs)
echo "Ubuntu: $UBUNTU_VERSION"

if ! version_ge "$UBUNTU_VERSION" "22.04"; then
    fail "Ubuntu 22.04+ required"
fi

require_sudo


# Base update

echo "===> Updating system"
sudo apt update -y

# Python

echo "===> Checking Python3"

if command_exists python3 && ! $FORCE; then
    PY_VERSION=$(python3 --version | awk '{print $2}')
    echo "Python detected: $PY_VERSION"
else
    echo "Installing Python3..."
    sudo apt install -y python3
fi

# python3-venv

echo "===> Checking python3-venv"

if dpkg -l | grep -q python3-venv && ! $FORCE; then
    echo "python3-venv OK"
else
    echo "Installing python3-venv..."
    sudo apt install -y python3-venv
fi


# curl (required for Docker)

echo "===> Checking curl"

if ! command_exists curl; then
    sudo apt install -y curl
fi

# Docker

echo "===> Checking Docker"

if command_exists docker && ! $FORCE; then
    echo "Docker already installed"
else
    echo "Installing Docker (README method)..."

    curl -fsSL https://get.docker.com -o get-docker.sh
    chmod +x get-docker.sh
    sudo sh ./get-docker.sh
    sudo chmod 777 /var/run/docker.sock
fi

# Docker Compose

echo "===> Checking Docker Compose"

if docker compose version >/dev/null 2>&1; then
    echo "Docker Compose available"
else
    echo "Docker Compose not detected explicitly (may be bundled)"
fi

# Docker group

echo "===> Configuring Docker permissions"

if groups "$USER" | grep -q docker; then
    echo "User already in docker group"
else
    sudo usermod -aG docker "$USER"
    #echo "Logout/login required"
fi

# VirtualBox

echo "===> Checking VirtualBox"

if command_exists vboxmanage && ! $FORCE; then
    echo "VirtualBox OK"
else
    echo "Installing VirtualBox..."
    sudo apt install -y virtualbox || {
        echo "Install manually: https://www.virtualbox.org/wiki/Linux_Downloads"
    }
fi

# Vagrant (README METHOD)

echo "===> Checking Vagrant"

if command_exists vagrant && ! $FORCE; then
    echo "Vagrant OK"
else
    echo "Installing Vagrant..."

    wget -O - https://apt.releases.hashicorp.com/gpg | \
        sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list

    sudo apt update -y
    sudo apt install -y vagrant
fi

# Mininet

echo "===> Checking Mininet"

if command_exists mn && ! $FORCE; then
    echo "Mininet OK"
else
    echo "Installing Mininet..."
    sudo apt install -y mininet
    echo "Recommended: https://mininet.org/download/"
fi

# Final validation

echo "===> Validating installation"

python3 --version || fail "Python not working"
docker --version || fail "Docker not working"
docker compose version || echo "Docker Compose check skipped"
vagrant --version || fail "Vagrant not working"
mn --version || fail "Mininet not working"

echo "Installation completed successfully"
echo "Next: ./app-compose.sh --start"
