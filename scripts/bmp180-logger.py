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

import socket

#### read config file
import ConfigParser as configparser
c = configparser.ConfigParser()
c.read('/etc/wsn/bmp180-logger.conf')

interval = c.getint('main', 'interval')
log_dir = c.get('logging', 'log_dir')
log_file = c.get('logging', 'log_file')

broker_addr = c.get('mqtt', 'broker_addr')
broker_port = c.get('mqtt', 'broker_port')
_template = c.get('mqtt', 'report_topic')
report_topic = _template.format(hostname=socket.gethostname())
#######################################


#### logging setup
try:
    os.makedirs(log_dir)
except OSError:
    if not osp.isdir(log_dir):
        raise

# HINT alt. solution to http://stackoveflow.com/a/27858760
# XXXX does not handle partial-hour UTC offsets
tzstr = '{:+03d}00'.format(-time.timezone/3600)
tsfmt = '%Y-%m-%dT%H:%M:%S'+tzstr

log_fmt = logging.Formatter('%(asctime)s\t%(message)s',
                            datefmt=tsfmt)
log_file = TimedRotatingFileHandler(osp.join(log_dir, log_file),
                                    when='midnight')
log_file.setFormatter(log_fmt)
log_file.suffix = '%Y-%m-%d.tsv'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(log_file)

log.addHandler(logging.StreamHandler()) # for debugging

#### MQTT integration
client = paho.Client()
client.connect_async(broker_addr, broker_port)
client.loop_start()

report = '{{"tstamp": {ts:0.2f}, "P": {p:0.2f}, "T": {t:0.2f}}}'

sensor = BMP.BMP085(busnum=1)

while True:
    try:
        tmpr = sensor.read_temperature() # C
        press = sensor.read_pressure()/100.0 # Pa->mbar

        now = time.time()
        log.info('\t'.join(['{:0.2f}'.format(tmpr),
                            '{:0.2f}'.format(press)]))

        client.publish(report_topic,
                       report.format(ts=now, p=press, t=tmpr),
                       qos=1, retain=True)

        time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        client.loop_stop()
        raise
    except:
        pass
