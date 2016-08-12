Wireless Sensor Network
=======================

Indoor Air & Climate Change (2015-2017)
---------------------------------------

Simple wifi (802.11bgn) sensor node for measuring:

* carbon dioxide (K30; Senseair)
* barometric pressure & temperature (BMP180)
* relative humidity & temperature (HTU21DF)




### Setup

#### Pressure Logger

First, manually install dependencies:

```
$ sudo apt-get update
$ sudo apt-get install git build-essential python-dev python-smbus
$ git clone https://github.com/adafruit/Adafruit_Python_BMP.git
$ cd Adafruit_Python_BMP
$ sudo python setup.py install
```

Then run the installation script:

```
$ sudo ./install.sh
```
