#!/bin/bash


# pressure-logger
echo "Installing BMP logging service executable..."
cp scripts/pressure-logger.py /usr/sbin/pressure-logger
chmod +x /usr/sbin/pressure-logger

echo "Registering BMP180 logging service..."
cp etc/systemd/system/pressure-logger.service /etc/systemd/system/

echo "Enabling BMP180 logging service start at boot..."
systemctl enable pressure-logger.service

echo "Starting BMP logging service..."
systemctl restart pressure-logger.service

