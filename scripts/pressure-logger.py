#!/usr/bin/python2
#
# Acquire temperature/pressure data from BMP180 and do stuff
#
# Patrick O'Keeffe <pokeeffe@wsu.edu>
# Laboratory for Atmospheric Research at Washington State University

from __future__ import print_function

import os, os.path as osp
import time
import logging
from logging.handlers import TimedRotatingFileHandler

import paho.mqtt.client as paho
import RPi.GPIO as GPIO

import Adafruit_BMP.BMP085 as BMP


##########    CONFIG    ###############
log_dir = '/var/log/wsn/bmp180'
log_file = 'pressure'

interval = 10 # sec
#######################################


#### logging setup
try:
    os.makedirs(log_dir)
except OSError:
    if not osp.isdir(log_dir):
        raise

log_path = osp.join(log_dir, log_file)
log_fmt = logging.Formatter('%(asctime)s\t%(message)s',
                            datefmt='%Y-%m-%dT%H:%M:%S%z')
log_fmt.converter = time.gmtime
    # HINT force timestamp to include a (correct) UTC offset
    # http://stackoveflow.com/a/27858760
log_file = TimedRotatingFileHandler(log_path)
log_file.setFormatter(log_fmt)
log_file.suffix = '%Y-%m-%d.tsv'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(log_file)

log.addHandler(logging.StreamHandler()) # for debugging


sensor = BMP.BMP085()

while True:
    try:
        tmpr = sensor.read_temperature()
        press = sensor.read_pressure()/100.0
        log.info('\t'.join(['{:0.2f}'.format(tmpr),
                            '{:0.2f}'.format(press)]))
        time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pass
