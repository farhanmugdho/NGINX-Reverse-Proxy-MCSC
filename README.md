# NGINX Reverse Proxy Assignment

This project demonstrates a reverse proxy setup using NGINX forwarding requests to two backend Flask application servers.

## Project Structure

```
nginx-reverse-proxy-assignment/
├── backend1/              # Backend 1 (port 5001)
│   └── server.py
├── backend2/              # Backend 2 (port 5002)
│   └── server.py
├── nginx/                 # NGINX reverse proxy configuration
│   └── reverse-proxy.conf
├── frontend/              # Frontend application
│   ├── app.py
│   └── templates/
│       └── index.html
├── screenshots/           # Proof screenshots
│   ├── ip-address.png
│   ├── backend1-running.png
│   ├── backend2-running.png
│   ├── nginx-config.png
│   └── nginx-test.png
├── README.md              # This file
└── report/                # Optional report
    └── report.md
```
## Architecture
Client -> NGINX :8080
             |-- /     -> frontend 127.0.0.1:3000
             |-- /api  -> backend  127.0.0.1:5000 -> MySQL 127.0.0.1:3306

            
## Backend Servers

### Backend 1 (port 5001)
- `backend1/server.py` - Flask application
- Returns: Hello from Backend 1
- Access via: http://YOUR-IP/app1

### Backend 2 (port 5002)
- `backend2/server.py` - Flask application
- Returns: Hello from Backend 2
- Access via: http://YOUR-IP/api

## NGINX Reverse Proxy Configuration

The NGINX configuration (`nginx/reverse-proxy.conf`) forwards:
- http://YOUR-IP/app1 → localhost:5001 (Backend 1)
- http://YOUR-IP/api → localhost:5002 (Backend 2)

## Setup & Running

### 1. Run setup-nginx.sh
```bash
cd nginx-reverse-proxy-assignment
./setup-nginx.sh      # installs NGINX, deploys the frontend and config
```

### 2. Start backends
```bash
./start.sh            # starts both backends
# Backend 1: http://localhost:5001/app1
# Backend 2: http://localhost:5002/api
```

### 3. Test the Setup
- Open browser and visit: http://YOUR-IP/app1
- Should display: Hello from Backend 1
- Open browser and visit: http://YOUR-IP/api
- Should display: Hello from Backend 2

## API Endpoints

- `/api/users` - Reads from MySQL if setup-mysql.sh is run (otherwise returns sample data)
- `/api/check-backend/<1|2>` - AJAX endpoint to check backend status

## Screenshots

For assignment submission, include these screenshots in screenshots/:
- ip-address.png - Your VM/IP address
- backend1-running.png - Backend 1 server running
- backend2-running.png - Backend 2 server running
- nginx-config.png - NGINX configuration file
- nginx-test.png - Browser showing app1 and api working
- nginx-status.png - NGINX status/running

## Report Sections (Option 2)

If submitting a report, include these sections:
1. Introduction
2. Environment
3. Backend Setup
4. NGINX Installation
5. Reverse Proxy Configuration
6. IP Address Explanation
7. VMware NAT Explanation
8. Request Flow
9. Testing
10. Screenshots
11. Conclusion
