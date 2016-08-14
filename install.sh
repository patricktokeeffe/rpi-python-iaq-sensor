#!/bin/bash


# pressure-logger
echo "Installing BMP logging service executable..."
cp scripts/bmp180-logger.py /usr/sbin/bmp180-logger
chmod +x /usr/sbin/bmp180-logger
mkdir -p /etc/wsn
cp etc/wsn/bmp180-logger.conf /etc/wsn/

echo "Registering BMP180 logging service..."
cp etc/systemd/system/bmp180-logger.service /etc/systemd/system/

echo "Enabling BMP180 logging service start at boot..."
systemctl enable bmp180-logger.service

echo "Starting BMP logging service..."
systemctl restart bmp180-logger.service

