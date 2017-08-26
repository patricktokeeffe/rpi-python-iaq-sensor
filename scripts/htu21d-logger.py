#!/usr/bin/python2
#
# Acquire temperature/pressure data from HTU21D and do stuff
#
# Patrick O'Keeffe <pokeeffe@wsu.edu>
# Laboratory for Atmospheric Research at Washington State University

from __future__ import print_function

import os, os.path as osp
import time
import logging
from logging.handlers import TimedRotatingFileHandler

import sys
sys.path.append('/home/pi/weather-station')
from HTU21D import HTU21D
htu = HTU21D()

import socket
import paho.mqtt.client as paho

#### read config file
import ConfigParser as configparser
c = configparser.ConfigParser()
c.read('/etc/wsn/htu21d-logger.conf')

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
#tzstr = '{:+03d}00'.format(-time.timezone/3600)
tsfmt = '%Y-%m-%dT%H:%M:%S'#+tzstr

log_fmt = logging.Formatter('%(asctime)s\t%(message)s',
                            datefmt=tsfmt)
log_file = TimedRotatingFileHandler(osp.join(log_dir, log_file),
                                    when='D', interval=30)
log_file.setFormatter(log_fmt)
log_file.suffix = '%Y-%m-%d.tsv'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(log_file)

log.addHandler(logging.StreamHandler()) # for journalctl output


#### MQTT integration
client = paho.Client()
client.connect_async(broker_addr, broker_port)
client.loop_start()
report = '{{"tstamp": {ts:0.2f}, "T": {t:0.2f}, "RH": {rh:0.1f}}'

## for urbanova
#rundir = '/run/aqnet/htu21d'
#run_T = os.path.join(rundir, 'T')
#run_RH = os.path.join(rundir, 'RH')
#try:
#    os.makedirs(rundir)
#except OSError:
#    if not osp.isdir(rundir):
#        raise


while True:
    try:
        T = htu.read_temperature()
        RH = htu.read_humidity()
        now = time.time()

        # rotating TSV files
        log.info('\t'.join(['{:0.2f}'.format(T),
                            '{:0.1f}'.format(RH)]))

        # for journalctl logs
        #### FIXME - better to have JSON in journalctl
        #### see above `logging.StreamHandler()`
        #print('{{"T": {0:0.2f}, "RH": {1:0.1f}}}'.format(T, RH))

        ## for Itron Riva
        #with open(run_T, 'w') as f:
        #    f.write('{:0.2f}'.format(T))
        #with open(run_RH, 'w') as f:
        #    f.write('{:0.2f}'.format(RH))

        client.publish(report_topic,
                       report.format(ts=now, t=T, rh=RH),
                       qos=1, retain=False)

        time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        client.loop_stop()
        raise
    except:
        time.sleep(15)
        pass
