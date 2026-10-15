
# NGINX Reverse Proxy Implementation on Linux

## 1. Project Overview

This project demonstrates how to implement an **NGINX Reverse Proxy** on a Linux operating system using two Python Flask backend services.

NGINX acts as the main entry point for incoming HTTP requests. Based on the requested URL path, NGINX forwards each request to the appropriate backend application.

The implementation covers:
- Linux environment setup
- NGINX installation and configuration
- Two Flask backend applications
- MySQL database integration
- Reverse proxy routing
- HTTP request and response flow
- Linux IP addressing and networking
- Testing and verification

### Technologies Used

| Technology | Purpose |
|---|---|
| Ubuntu Linux | Operating system |
| NGINX | Reverse proxy server |
| Python 3 | Backend programming |
| Flask | Web application framework |
| MySQL | Database for Backend 1 |
| PyMySQL | Python-MySQL connectivity |
| Git | Source code management |
| curl | HTTP request testing |

This implementation uses NGINX directly on Linux without requiring Docker, Kubernetes, AWS, or an additional reverse proxy.

---

## 2. Project Objectives

The main objectives are:

1. Install and run NGINX on Linux.
2. Run two independent backend applications.
3. Configure different ports for each backend.
4. Configure NGINX as a reverse proxy.
5. Forward incoming requests based on URL paths.
6. Verify communication between NGINX and Flask.
7. Identify the Linux IP address and network interface.
8. Explain private IP addressing and virtual networking.
9. Test the complete HTTP request-response cycle.

---

## 3. Project Structure

The relevant project files are:

```text
NGINX-Reverse-Proxy-MCSC/
│
├── backend1/
│   └── server.py
│
│
├── database/
│
├── nginx/
│   └── reverse-proxy.conf
│
├── frontend/
│
├── docker/
│
├── kubernetes/
│
├── docker-compose.yaml
│
├── setup-nginx.sh
│
├── start.sh
│
├── README.md
│
├── architecture-diagram.txt
│
└── DESIGN-EXPLANATION.txt
```

The repository contains additional Docker and Kubernetes resources, but these are not required for the standalone Linux NGINX implementation described here.

---

## 4. System Architecture

```text
                  CLIENT / BROWSER
                         |
                         |
                  HTTP Request
                         |
                         v
                NGINX REVERSE PROXY
                     Port 8080
                         |
                         |                     
                         |            
                       /app1         
                         |                     
                         v             
                   FLASK BACKEND 1 
                      Port 5001
                         |                     
                         v          
                   MySQL Database       
                         |                
                         |
                    HTTP Response
                         |
                         v
                  CLIENT / BROWSER
```

### Architecture Explanation

The browser sends HTTP requests to NGINX on port `8080`.

NGINX examines the requested URL path and forwards the request to the corresponding backend.

| Request Path | Backend | Backend Port |
|---|---|---|
| `/app1` | Flask Backend | 5001 |

Backend 1 connects to the MySQL database.

Both applications can be accessed using the same NGINX port.

---

## 5. Linux Environment Setup

The demonstrated environment uses Ubuntu on Windows Subsystem for Linux (WSL).

### Step 1 — Open Ubuntu

From Windows PowerShell:

```powershell
wsl -d Ubuntu
```

The following Linux commands are executed inside the Ubuntu terminal.

### Step 2 — Update Packages

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 3 — Install Required Packages

```bash
sudo apt install -y nginx python3 python3-pip python3-venv git curl mysql-server
```

### Step 4 — Start NGINX

```bash
sudo systemctl start nginx
```

Check its status:

```bash
sudo systemctl status nginx
```

Expected status:

```text
Active: active (running)
```

Press `q` to exit the status screen.

### Step 5 — Start MySQL

```bash
sudo systemctl start mysql
```

Verify:

```bash
sudo systemctl status mysql
```

Expected status:

```text
Active: active (running)
```

---

## 6. Clone the GitHub Repository

Navigate to the home directory:

```bash
cd ~
```

Clone the repository:

```bash
git clone https://github.com/farhanmugdho/NGINX-Reverse-Proxy-MCSC.git
```

If the repository has already been cloned, skip the clone command.

Enter the project directory:

```bash
cd ~/NGINX-Reverse-Proxy-MCSC
```

Check the files:

```bash
ls
```

---

## 7. Python Virtual Environment

Create a virtual environment inside the project directory:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install Flask and PyMySQL:

```bash
python3 -m pip install flask pymysql
```

Verify PyMySQL installation:

```bash
python3 -m pip show pymysql
```

The terminal prompt should indicate the active environment:

```text
(.venv) ubuntu@hostname:~/NGINX-Reverse-Proxy-MCSC$
```

---

## 8. MySQL Database Configuration

Backend 1 requires a MySQL database.

Open MySQL with administrative privileges:

```bash
sudo mysql
```

Create the database:

```sql
CREATE DATABASE IF NOT EXISTS samples;
```

Create the local database user:

```sql
CREATE USER IF NOT EXISTS 'user'@'localhost'
IDENTIFIED BY 'password';
```

Configure its password:

```sql
ALTER USER 'user'@'localhost'
IDENTIFIED BY 'password';
```

Grant database permissions:

```sql
GRANT ALL PRIVILEGES ON samples.* TO 'user'@'localhost';
```

Select the database:

```sql
USE samples;
```

Create the visits table:

```sql
CREATE TABLE IF NOT EXISTS visits (
    id INT PRIMARY KEY,
    counter INT NOT NULL DEFAULT 0
);
```

Insert the initial record:

```sql
INSERT INTO visits (id, counter)
VALUES (1, 0)
ON DUPLICATE KEY UPDATE id = id;
```

Exit MySQL:

```sql
EXIT;
```

### Verify MySQL Connection

Run:

```bash
mysql -h 127.0.0.1 -u user -p samples
```

Enter the configured password when prompted.

A successful connection displays the MySQL prompt:

```text
mysql>
```

Exit using:

```sql
EXIT;
```

**Security Note:** The sample credentials are intended only for a local coursework demonstration. Production applications should use stronger credentials and environment-based configuration.

---

## 9. Configure Backend 1

Backend 1 uses:

```text
python3 backend1/server.py
```

It is configured to run on port `5001`.

Its application defines a Flask route:

```python
@app.route('/app1')
```

Backend 1 connects to MySQL and reads the visits counter.

### Database Host Configuration

The original source uses the hostname:

```python
DB_HOST = 'db'
```

This hostname is intended for Docker networking.

For standalone Linux execution, use:

```python
DB_HOST = '127.0.0.1'
```

The following command updates the original database hostname:

```bash
sed -i "s/DB_HOST = 'db'/DB_HOST = '127.0.0.1'/" backend1/server.py
```

Verify the value:

```bash
grep -n DB_HOST backend1/server.py
```

Expected value:

```python
DB_HOST = '127.0.0.1'
```

### Start Backend 1

From the project directory:

```bash
source .venv/bin/activate
python3 backend1/server.py
```

The Flask server should report that it is listening on port `5001`.

Keep this terminal open.

### Test Backend 1 Directly

Open another terminal and run:

```bash
curl -i http://127.0.0.1:5001/app1
```

Expected successful HTTP status:

```text
HTTP/1.1 200 OK
```

Example response body:

```text
Hello from Backend 1 - Visits: 0
```

The visits value depends on the database record.

---


## 10. NGINX Reverse Proxy Configuration

NGINX receives incoming HTTP requests on port `8080` and routes requests to the Flask applications.

### Configuration File

The project configuration is located at:

```text
nginx/reverse-proxy.conf
```

```bash

sudo nano /etc/nginx/sites-available/reverse-proxy
```

Use the following configuration for the standalone Linux implementation:

```nginx
server {
    listen 8080;
    server_name localhost;

    location /app1 {
        proxy_pass http://127.0.0.1:5001;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api {
        proxy_pass http://127.0.0.1:5002;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
Checking the currently enabled configuration
```bash
sudo cat /etc/nginx/sites-available/reverse-proxy
```
Look for
```bash
listen 8080;
```



### Explanation

| Directive | Purpose |
|---|---|
| `listen 8080` | NGINX accepts HTTP requests on port 8080 |
| `server_name localhost` | Defines the configured server name |
| `location /app1` | Matches Backend 1 requests |
| `proxy_pass` | Forwards requests to a backend |
| `X-Real-IP` | Sends the client IP information |
| `X-Forwarded-For` | Passes the proxy-chain IP information |
| `X-Forwarded-Proto` | Identifies the original request protocol |

The `proxy_pass` directives do not end with a trailing slash, preserving the original request URI for the Flask routes.

---

## 11. Enable the NGINX Configuration

Ensure the repository configuration file contains the configuration shown above.

Copy it to the NGINX configuration directory:

```bash
sudo cp nginx/reverse-proxy.conf /etc/nginx/sites-available/reverse-proxy
```

Enable the configuration:

```bash
sudo ln -sfn /etc/nginx/sites-available/reverse-proxy /etc/nginx/sites-enabled/reverse-proxy
```

### Test the Configuration

```bash
sudo nginx -t
```

Expected output:

```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Restart NGINX

```bash
sudo systemctl restart nginx
```

### Verify Listening Port

```bash
sudo ss -ltnp | grep ':8080'
```

NGINX should be listening on port `8080`.

A successful syntax test alone does not prove that NGINX is listening or forwarding requests.

---

## 12. Test the NGINX Reverse Proxy

Both Flask applications must be running during these tests.

### Test Backend 1 Through NGINX

```bash
curl -i http://127.0.0.1:8080/app1
```

Expected successful HTTP status:

```text
HTTP/1.1 200 OK
```

Example response:

```text
Hello from Backend 1 - Visits: 0
```


### Browser Testing

Open:

**Backend 1 through NGINX**

```text
http://localhost:8080/app1
```

Both requests should be served through NGINX rather than accessing the Flask ports directly.

---

## 13. Verify Listening Ports

Run:

```bash
sudo ss -ltnp
```

Check that the following services are listening:

| Service | Port |
|---|---|
| NGINX | 8080 |
| Flask Backend 1 | 5001 |
| MySQL | 3306, if using its default TCP configuration |

A more focused command is:

```bash
sudo ss -ltnp | grep -E ':8080|:5001|:5002'
```

### Check NGINX Access Logs

Run:

```bash
sudo tail -f /var/log/nginx/access.log
```

Send a request to:

```text
http://localhost:8080/app1
```

The NGINX access log should record the incoming request.

Repeat with:

```text
http://localhost:8080/api
```

These logs, together with the active proxy configuration and successful HTTP responses, provide evidence of request forwarding.

---

## 14. Complete HTTP Request Flow

### Request to Backend 1

**Step 1:** The browser sends an HTTP request to:

```text
http://localhost:8080/app1
```

**Step 2:** NGINX receives the request on port `8080`.

**Step 3:** NGINX examines the URL path `/app1`.

**Step 4:** The reverse proxy forwards the request to:

```text
http://127.0.0.1:5001/app1
```

**Step 5:** Flask Backend 1 processes the request.

**Step 6:** Backend 1 reads the visits counter from MySQL.

**Step 7:** Backend 1 sends an HTTP response back to NGINX.

**Step 8:** NGINX forwards the response to the browser.

Example response:

```text
Hello from Backend 1 - Visits: 0
```



**Step 6:** NGINX forwards the response to the browser.

This demonstrates path-based routing through a single reverse proxy.

---

## 15. Linux IP Address and Networking

Linux provides commands to inspect IP addresses, interfaces, and routing information.

### Check IP Address

```bash
ip -4 addr
```

### Check Routing Table

```bash
ip route
```

### Check Assigned IPv4 Addresses

```bash
hostname -I
```

### Inspect the Default Route

```bash
ip -4 route get 1.1.1.1
```

### Network Information

Record the actual values from the Linux environment:

| Network Property | Observed Value |
|---|---|
| Linux IPv4 Address | Verify using `ip -4 addr` |
| Network Interface | Verify from interface output |
| Subnet/Prefix | Verify from interface output |
| Default Gateway | Verify using `ip route` |
| IP Address Type | Private or public |
| IP Assignment | Verify from system network configuration |
| Virtual Networking Mode | Verify WSL/VM configuration |

### Private vs. Public IP Address

Private IPv4 ranges include:

```text
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
```

Private IPv4 addresses are not directly routable on the public internet.

Public IPv4 addresses can be globally routable when permitted by network configuration.

The address `127.0.0.1` is a loopback address used for communication within the local system.

### Virtual Networking in WSL

This implementation was demonstrated using Ubuntu on WSL.

In the common WSL 2 NAT configuration, Linux uses a virtual network interface connected through the Windows host networking system.

The WSL instance typically receives a private IPv4 address within a virtual subnet managed by the host networking environment.

Outbound traffic can pass through the host's network connection using NAT.

The exact interface, subnet, IP address, and gateway must be confirmed from the running environment.

WSL may also support other networking configurations, so NAT should not be assumed without verification.

### VMware NAT Networking

If the implementation is reproduced inside a VMware Linux virtual machine using NAT:

1. VMware creates a private virtual network.
2. The VM normally receives a private IP address.
3. VMware's virtual DHCP service may assign the IP.
4. Outbound VM traffic passes through the NAT service.
5. NAT allows the VM to access external networks through the host.

### VMware Bridged Networking

In bridged mode:

1. The VM connects to the same network as the host.
2. The VM appears as a separate network device.
3. The network's DHCP server may assign the IP address.
4. The VM can communicate with other devices, subject to firewall and network configuration.

**Environment note:** WSL and VMware are different virtualization environments. If VMware is mandatory for the assignment, the implementation must be demonstrated in the required VMware environment.

---

## 16. Troubleshooting

### Error 1 — ModuleNotFoundError: pymysql

Cause: The Python environment cannot find PyMySQL.

Solution:

```bash
python3 -m pip install pymysql
```

### Error 2 — MySQL Hostname Cannot Be Resolved

Example:

```text
socket.gaierror: [Errno -2] Name or service not known
```

Cause: The backend uses Docker hostname `db` outside Docker.

Solution:

```bash
sed -i "s/DB_HOST = 'db'/DB_HOST = '127.0.0.1'/" backend1/server.py
```

### Error 3 — MySQL Access Denied

Example:

```text
ERROR 1045 (28000): Access denied
```

Cause: Invalid database credentials or missing permissions.

Solution: Verify the database user, password, and grants.

### Error 4 — 404 Not Found

Cause: The requested Flask route does not exist.

Correct endpoints:

```text
Backend 1: /app1
```

### Error 5 — 500 Internal Server Error

Cause: An application-side failure, such as a database connection or query error.

Solution: Inspect the traceback in the Flask terminal.

### Error 6 — Connection Refused

Example:

```text
curl: (7) Failed to connect
```

Cause: The destination service may not be running or listening on the requested port.

Check:

```bash
sudo ss -ltnp
```

Restart the corresponding service if necessary.

### Error 7 — NGINX Not Listening on Port 8080

Check the enabled configuration:

```bash
ls -l /etc/nginx/sites-enabled/
```

Verify the active configuration:

```bash
sudo nginx -T
```

Test and restart NGINX:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

---

## 17. Screenshots and Evidence

Capture screenshots after successfully testing the implementation.

### Screenshot 1 — Linux Environment

```bash
cat /etc/os-release
```

### Screenshot 2 — NGINX Status

```bash
sudo systemctl status nginx
```

### Screenshot 3 — Backend Services

Show both Flask applications listening on their respective ports.

### Screenshot 4 — NGINX Configuration

```bash
sudo cat /etc/nginx/sites-available/reverse-proxy
```

### Screenshot 5 — IP Address

```bash
ip -4 addr
ip route
```

### Screenshot 6 — Direct Backend Testing

```bash
curl -i http://127.0.0.1:5001/app1
curl -i http://127.0.0.1:5002/api
```

### Screenshot 7 — Reverse Proxy Testing

```bash
curl -i http://127.0.0.1:8080/app1
curl -i http://127.0.0.1:8080/api
```

### Screenshot 8 — NGINX Request Logs

```bash
sudo tail -n 20 /var/log/nginx/access.log
```

Only include screenshots showing the actual executed setup and observed results.

---

## 18. Assignment Requirements Checklist

- [ ] Linux environment confirmed
- [ ] NGINX installed and running
- [ ] Backend 1 running on port 5001
- [ ] Backend 2 running on port 5002
- [ ] NGINX configured as a reverse proxy
- [ ] NGINX listening on port 8080
- [ ] Direct backend requests tested
- [ ] Reverse proxy requests tested
- [ ] Linux IP address identified
- [ ] Network interface and subnet explained
- [ ] Virtual networking mode explained
- [ ] Screenshots or demonstration video prepared

---

## 19. Conclusion

This project illustrates how NGINX can act as a reverse proxy between a client and multiple backend applications.

The intended implementation uses two Flask services running on separate ports, with NGINX receiving HTTP requests on port `8080` and routing them based on URL paths.

Backend 1 integrates with MySQL

The reverse proxy implementation is verified when both requests return successful responses through NGINX and the active configuration and logs confirm the routing behavior.

The project also provides practical experience with Linux services, virtual networking, private IP addressing, HTTP communication, and backend integration.

---
