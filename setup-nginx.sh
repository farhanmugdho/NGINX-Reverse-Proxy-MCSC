#!/bin/bash
# Install NGINX and deploy configuration

apt-get update
apt-get install -y nginx

# Copy NGINX config
cp nginx/reverse-proxy.conf /etc/nginx/sites-available/default

# Test and restart NGINX
nginx -t
systemctl restart nginx