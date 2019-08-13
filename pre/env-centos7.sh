#!/bin/bash

yum -y install epel-release
yum -y install python36
python3 -m ensurepip
pip3 install --upgrade pip
pip3 install requests
pip3 install beautifulsoup4
pip3 install lxml
