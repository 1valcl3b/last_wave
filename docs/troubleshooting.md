# Troubleshooting Guide

This document lists common issues that may occur when installing or running WAVE, along with their causes and solutions.

---

## 1. Error: Cannot expose privileged port 80

### Error message


cannot expose privileged port 80


### Cause

Docker (especially in rootless mode) cannot bind to ports below 1024.

### Solution (temporary)

```
sudo sysctl net.ipv4.ip_unprivileged_port_start=80
```

Then restart the environment:

```
./app-compose.sh --start
```

---

## 2. Error: Permission denied (Docker daemon)

### Error message


permission denied while trying to connect to the Docker daemon socket


### Cause

User is not in the `docker` group.

### Solution

```
sudo usermod -aG docker $USER
```

Then log out and log back in.

---

## 3. Docker command works only with sudo

### Cause

Docker group permissions not applied yet.

### Solution

```
newgrp docker
```

Or log out and log back in.

---

## 4. Error: Port already in use

### Error message


bind: address already in use


### Cause

Another service is using the required port (e.g., 80 or 8181).

### Solution

Check which process is using the port:

```
sudo lsof -i :80
```

Stop the conflicting service or change the port configuration.

---

## 5. Cannot access web interface

### Cause

- Using `localhost` in a remote environment
- Firewall blocking access
- Incorrect IP

### Solution

- Replace `localhost` with the machine IP:

- Check open ports:

```
sudo ufw status
```

- If using cloud/VM, ensure security groups allow the port.

---

## 6. Containers are not running

### Symptom

```
docker ps
```

does not show expected containers.

### Solution

Check all containers:

```
docker ps -a
```

Check logs:

```
docker logs wave_app
```

Restart environment:

```
./app-compose.sh --destroy
```
```
./app-compose.sh --start
```

---

## 7. Mininet requires sudo password

### Cause

Mininet requires root privileges.

### Solution

Enter your password when prompted.

### Optional (automation)

Configure passwordless sudo:

```
sudo visudo
```

Add:
```
youruser ALL=(ALL) NOPASSWD: ALL
```

---

## 8. Mininet fails to start

### Possible causes

- Missing kernel modules
- Network conflicts
- Insufficient privileges

### Solution

Run Mininet test:

```
sudo mn --test pingall
```

If it fails, reinstall it from the official website or via apt.

---

## 9. Vagrant not working

### Error message


vagrant: command not found


### Cause

Vagrant not installed correctly.

### Solution

Reinstall using official repository (as described in README).

---

## 10. VirtualBox errors

### Common issue


VT-x/AMD-V not available


### Cause

Hardware virtualization disabled.

### Solution

Enable virtualization in BIOS/UEFI.

---

## 11. Vagrant VM provisioning is slow

### Cause

First execution downloads large VM images.

### Solution

This is expected behavior. Wait for completion.

---

## 12. Network conflicts (IP overlap)

### Cause

Experiment IP range conflicts with the host network or with virtualization network interfaces.

### Solution

- Use a different subnet (e.g., `10.x.x.x` or `172.16.x.x`)
- Avoid using the same IP range as your local network

> [!WARNING]
> If the researcher configures an IP range that is already used by a virtualization platform (e.g., VirtualBox commonly uses `192.168.56.0/24` for host-only networks), the traffic may not traverse the Mininet topology as expected.  
> In such cases, packets can be routed through the host's virtual network interface instead of the emulated network, leading to invalid or inconsistent experimental results.

---

## 13. install.sh script fails

### Possible causes

- No sudo permissions
- No internet connection
- Package repository issues

### Solution

Check log file:

```
cat install.log
```

Then:

- Verify internet connection
- Run script again with force:

```
./install.sh --force
```

---

## 14. Docker installation issues

### Symptom

Docker installed but not working.

### Solution

Restart Docker:

```
sudo systemctl restart docker
```

Check status:

```
sudo systemctl status docker
```

---

## 15. Low performance or long execution time

### Cause

Insufficient hardware resources.

### Solution

Ensure minimum requirements:

- 4 CPU cores
- 8 GB RAM

Close other applications if necessary.

---

## 16. Browser interface not loading correctly

### Cause

- Cache issues
- Browser incompatibility

### Solution

- Try another browser
- Clear cache
- Use incognito mode

---

## 17. No internet connection during setup

### Cause

Dependencies require downloads.

### Solution

Ensure internet connectivity before running:

- install.sh
- Docker setup
- Vagrant provisioning

---

