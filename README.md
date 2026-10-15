# NGINX Reverse Proxy Implementation on Linux

## Project Overview

This project demonstrates how NGINX works as a reverse proxy on a Linux system, forwarding incoming HTTP requests to different backend application services running on separate ports.

The project uses:
- Linux (Ubuntu/Debian)
- NGINX
- Python
- Flask
- Git and GitHub

The main objective is to understand how client requests travel through a web server, how different application components communicate, and how IP addressing works in a Linux networking environment.

---

## Project Objectives

- Install and run NGINX on Linux.
- Create two independent Flask backend services.
- Run the backend services on different ports.
- Configure NGINX as a reverse proxy.
- Route HTTP requests to the appropriate backend.
- Identify the Linux machine's IP address.
- Explain private/public IP addressing and VMware networking.
- Test and verify the complete request flow.

---

## Project Structure

```text
nginx-reverse-proxy/
│
├── README.md
│
├── backend1/
│   └── server.py
│
├── backend2/
│   └── server.py
│
├── nginx/
│   └── reverse-proxy.conf
│
├── screenshots/
│
├── setup-nginx.sh
│
└── start.sh
```

> Note: The repository structure should match the files actually uploaded to GitHub.

---

## System Architecture

```text
                    Client / Browser
                           |
                           | HTTP Request
                           v
                  NGINX Reverse Proxy
                       Port 8080
                           |
                +----------+----------+
                |                     |
                |                     |
             /app1/                 /app2/
                |                     |
                v                     v
          Flask Backend 1       Flask Backend 2
          127.0.0.1:5001        127.0.0.1:5002
                |                     |
                +----------+----------+
                           |
                      HTTP Response
                           |
                           v
                    Client / Browser
```

### Architecture Explanation

NGINX acts as the main entry point for client requests.

When a client sends an HTTP request, NGINX checks the requested URL path and forwards the request to the appropriate backend application.

- `/app1/` routes to Backend 1 on port `5001`.
- `/app2/` routes to Backend 2 on port `5002`.

Each backend processes its request independently and sends the response back through NGINX.

---

## Backend Servers

Two Python Flask applications are used to demonstrate request routing.

### Backend 1 — Port 5001

**File:** `backend1/server.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Backend 1"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
```

**Direct Access:**

```text
http://127.0.0.1:5001/
```

**Through NGINX:**

```text
http://127.0.0.1:8080/app1/
```

**Expected Response:**

```text
Hello from Backend 1
```

### Backend 2 — Port 5002

**File:** `backend2/server.py`

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Backend 2"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)
```

**Direct Access:**

```text
http://127.0.0.1:5002/
```

**Through NGINX:**

```text
http://127.0.0.1:8080/app2/
```

**Expected Response:**

```text
Hello from Backend 2
```

---

## NGINX Reverse Proxy Configuration

**File:** `nginx/reverse-proxy.conf`

```nginx
server {
    listen 8080;
    server_name _;

    location /app1/ {
        proxy_pass http://127.0.0.1:5001/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /app2/ {
        proxy_pass http://127.0.0.1:5002/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Configuration Explanation

- `listen 8080;` — NGINX listens for incoming HTTP requests on port 8080.
- `server_name _;` — Provides a placeholder server name for this server block.
- `location /app1/` — Matches requests beginning with `/app1/`.
- `proxy_pass http://127.0.0.1:5001/;` — Forwards matching requests to Backend 1.
- `location /app2/` — Matches requests beginning with `/app2/`.
- `proxy_pass http://127.0.0.1:5002/;` — Forwards matching requests to Backend 2.
- `proxy_set_header` — Passes relevant request information to the backend server.

The trailing slash in each `proxy_pass` directive replaces the matched location prefix with `/` when forwarding requests.

---

## Installation and Setup

All commands must be executed inside the Linux environment.

### Step 1 

```
wsl -d Ubuntu
```

### Step 2 — Update Linux Packages

```bash
sudo apt update
```

### Step 3 — Install NGINX and Python

```bash
sudo apt install -y nginx python3 python3-pip python3-venv
```

### Step 4 — Check NGINX Status

```bash
sudo systemctl status nginx
```

NGINX should report:

```text
active (running)
```

If NGINX is not running:

```bash
sudo systemctl start nginx
```

If NGINX is running
then
```bash
cd ~
git clone https://github.com/farhanmugdho/NGINX-Reverse-Proxy-MCSC.git
```

### Step 5 — Install Flask

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask
```

```bash
cd ~/NGINX-Reverse-Proxy-MCSC
ls
```

### Step 6 — Start Backend 1

Check if pymysql is installed or not, if not installed then
```bash
python3 -m pip install pymysql
```

Open a Linux terminal and run:

```bash
source .venv/bin/activate
python3 backend1/server.py
```

If it fails to run then
```bash
grep -n DB_HOST backend1/server.py
```

Backend 1 will listen on:

```text
127.0.0.1:5001
```

### Step 7 — Start Backend 2

Open another Linux terminal and run:

```bash
source .venv/bin/activate
python3 backend2/server.py
```

Backend 2 will listen on:

```text
127.0.0.1:5002
```

### Step 8 — Configure NGINX

Copy the reverse proxy configuration:

```bash
sudo cp nginx/reverse-proxy.conf /etc/nginx/sites-available/reverse-proxy
```

Enable the configuration:

```bash
sudo ln -s /etc/nginx/sites-available/reverse-proxy /etc/nginx/sites-enabled/reverse-proxy
```

If the symbolic link already exists, do not create it again.

### Step 9 — Test NGINX Configuration

```bash
sudo nginx -t
```

Expected successful result:

```text
nginx: configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Step 10 — Reload NGINX

```bash
sudo systemctl reload nginx
```

---

## API Endpoints

| Endpoint | Backend | Port | Description |
|----------|---------|------|-------------|
| `/app1/` | Backend 1 | 5001 | Routes requests to Flask Backend 1 |
| `/app2/` | Backend 2 | 5002 | Routes requests to Flask Backend 2 |

NGINX receives requests on port `8080` and forwards them to the corresponding backend.

---

## Testing the Backend Services

### Test Backend 1 Directly

```bash
curl -i http://127.0.0.1:5001/
```

Expected response body:

```text
Hello from Backend 1
```

### Test Backend 2 Directly

```bash
curl -i http://127.0.0.1:5002/
```

Expected response body:

```text
Hello from Backend 2
```

These tests confirm that both Flask applications are running independently.

---

## Testing NGINX Reverse Proxy

### Test Route 1

```bash
curl -i http://127.0.0.1:8080/app1/
```

Expected response body:

```text
Hello from Backend 1
```

### Test Route 2

```bash
curl -i http://127.0.0.1:8080/app2/
```

Expected response body:

```text
Hello from Backend 2
```

A successful HTTP `200 OK` response containing the correct backend message confirms that NGINX is forwarding the request to the intended application.

### Check Listening Ports

```bash
sudo ss -ltnp
```

Verify that:
- NGINX is listening on port `8080`.
- Flask Backend 1 is listening on port `5001`.
- Flask Backend 2 is listening on port `5002`.

---

## IP Address and Network Configuration

Linux provides commands to inspect the machine's IP address and network interfaces.

### Check IP Address

```bash
ip -4 addr
```

### Check Routing Table

```bash
ip route
```

### Network Information

Fill in the following information using the actual output from the Linux machine:

| Network Property | Observed Value |
|------------------|----------------|
| Linux IP Address | To be verified |
| Network Interface | To be verified |
| Subnet/Prefix | To be verified |
| Default Gateway | To be verified |
| IP Address Type | To be verified |
| IP Assignment Method | To be verified |
| VMware Networking Mode | To be verified, if applicable |

### Private vs. Public IP Address

A private IPv4 address belongs to one of these ranges:

```text
10.0.0.0       - 10.255.255.255
172.16.0.0     - 172.31.255.255
192.168.0.0    - 192.168.255.255
```

Private IP addresses are commonly used within local networks and virtual machine networks.

A public IP address is globally routable on the internet.

The address `127.0.0.1` is a loopback address used for internal communication within the same machine. It is not the machine's LAN IP address.

### Why the Machine Receives Its IP Address

If DHCP is enabled, the DHCP server assigns an available IP address from the configured address pool.

The assigned address depends on:
- The network subnet.
- DHCP server configuration.
- Available addresses.
- Existing DHCP leases.
- Address reservations, if configured.

If static addressing is used, the IP address is assigned through the machine's network configuration.

### VMware NAT Networking

When VMware NAT mode is enabled:

1. The virtual machine connects to a private virtual network.
2. VMware normally assigns a private IP address through its virtual DHCP server.
3. The VM sends outbound traffic through the VMware NAT service.
4. NAT translates the VM's private network connection using the host-side network connection.
5. This allows the VM to communicate with external networks without requiring its own directly accessible public IP.

### VMware Bridged Networking

In Bridged mode:

1. The VM connects to the same network as the host.
2. The VM acts as a separate device on that network.
3. It normally receives an IP from the network's DHCP server.
4. Other devices on that network may be able to communicate directly with the VM, subject to firewall and network restrictions.

The actual networking mode and assigned IP must be verified in the Linux/VMware environment.

---

## Complete HTTP Request Flow

The request flow works as follows:

**Step 1:** The client sends an HTTP request to NGINX.

```text
http://127.0.0.1:8080/app1/
```

**Step 2:** NGINX receives the request on port `8080`.

**Step 3:** NGINX examines the URL path `/app1/`.

**Step 4:** Based on its configuration, NGINX forwards the request to:

```text
http://127.0.0.1:5001/
```

**Step 5:** Flask Backend 1 processes the request and generates a response.

**Step 6:** The response returns to NGINX.

**Step 7:** NGINX forwards the HTTP response to the client.

**Step 8:** The client receives the result:

```text
Hello from Backend 1
```

The same process applies to `/app2/`, except that NGINX forwards the request to Backend 2 on port `5002`.

---

## Screenshots

The following screenshots should be captured from the actual Linux environment after successful implementation.

### Screenshot 1 — Linux Environment

Show the Linux distribution and terminal.

```bash
cat /etc/os-release
```

### Screenshot 2 — NGINX Service

Show the NGINX service status.

```bash
sudo systemctl status nginx
```

### Screenshot 3 — Backend Servers

Show both Flask applications running on ports `5001` and `5002`.

### Screenshot 4 — NGINX Configuration

Show the active reverse proxy configuration.

```bash
sudo cat /etc/nginx/sites-available/reverse-proxy
```

### Screenshot 5 — IP Address

Show the assigned IP address and network interface.

```bash
ip -4 addr
ip route
```

### Screenshot 6 — Request Flow Testing

Show successful requests through NGINX.

```bash
curl -i http://127.0.0.1:8080/app1/
curl -i http://127.0.0.1:8080/app2/
```

Add the corresponding image files to the `screenshots/` folder.

---

## Assignment Report Sections

If submitting the report option, include:

1. Introduction
2. Project Objectives
3. Linux Environment
4. Backend Application Setup
5. NGINX Installation
6. Reverse Proxy Configuration
7. IP Address and Network Explanation
8. VMware NAT/Bridged Networking Explanation
9. Complete HTTP Request Flow
10. Testing Results
11. Screenshots
12. Conclusion

---

## Conclusion

This project demonstrates how NGINX can be configured as a reverse proxy in a Linux environment.

Two independent Flask applications run on separate ports, and NGINX routes incoming HTTP requests to the correct backend service based on the requested URL.

The implementation also covers Linux IP addressing, private and public networks, DHCP, VMware networking, and the complete HTTP request-response cycle.

Successful testing of both backend services through NGINX provides evidence that the reverse proxy is functioning correctly.
