Wireless Sensor Node
====================

Indoor Air & Climate Change (2015-2017)
---------------------------------------

A Raspberry Pi-based wireless sensor node for measuring:

* carbon dioxide ([K30; Senseair][1])
* barometric pressure & temperature ([BMP180; Bosch][2])

  [1]: http://www.co2meter.com/products/k-30-co2-sensor-module
  [2]: https://www.adafruit.com/products/1603


## Quick Start

After providing power, the system boots immediately and begins logging
measurements to local storage. Sensors are queried for new values twice
per minute and data is logged into tab-separated values files. 

The wireless network is used to update the clock and to report measurements
to an MQTT message broker.


## Usage

### Configuration

> *TODO*


## Setup

### Assembly

*Refer to the excellent resources provided by the vendors linked to above.*

### Installation

First, manually install dependencies:

```
$ sudo apt-get update
$ sudo apt-get install git build-essential python-dev python-smbus samba samba-common
$ git clone https://github.com/adafruit/Adafruit_Python_BMP.git
$ cd Adafruit_Python_BMP
$ sudo python setup.py install
```

Then run the installation script:

```
$ sudo ./install.sh
```
