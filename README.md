PingdomResponder
================

A light weight responder to Pingdom Probe server requests  
Runs as a daemon taking up very little resources and will only respond to valid Pingdom Probe server IP addresses or custom ones you have added.

# Running PingdomResponder
There are 3 parameters start | restart | stop
```
python PingdomResponder/server.py PARAM
python PingdomResponder/server.py start
```

#Installation
Only 1 external Python module is required: FeedParser (http://pypi.python.org/pypi/feedparser/)  

## Install Python SetupTools
Install python setuptools if you don't already have them installed  
Go to http://pypi.python.org/pypi/setuptools#files and download the setuptools .egg file for your Python version  
For Python 2.7 you can use the following:
```
wget -O setuptools-0.6c11-py2.7.egg "http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg"
sudo sh setuptools-0.6c11-py2.7.egg
```

## Install FeedParser
Go to http://pypi.python.org/pypi/feedparser/#downloads and select the latest version (At this time 5.1.3
```
wget -O feedparser-5.1.3.tar.gz "http://pypi.python.org/packages/source/f/feedparser/feedparser-5.1.3.tar.gz"
tar xvf feedparser-5.1.3.tar.gz
cd feedparser-5.1.3
sudo python setup.py install
```

## Firewall
Open port 8143 on your firewall to allow incoming requests to Pingdom Responder

## Customise Pingdom Responder
1. By default PingdomResponder listens on port 8143 - you can change this by modifying the 'port' variable in server.py  
2. PingdomResponder will only respond with a 200 OK when the request comes from IP addresses published by Pingdom on their Probe RSS Feed.  
You can add your own static IP addresses to the 'customProbeIPs' list eg: ['127.0.0.1', '123.123.123.123']  
This will allow your requests to be responded to.
