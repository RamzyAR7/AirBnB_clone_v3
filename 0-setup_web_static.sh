#!/usr/bin/env bash
# Checks and makes dirs and configure nginx
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx
if [ ! -d "/data/" ];
then sudo mkdir -p "/data/"
fi
if [ ! -d "/data/web_static/" ];
then sudo mkdir -p "/data/web_static/"
fi
if [ ! -d "/data/web_static/releases/" ];
then sudo mkdir -p "/data/web_static/releases/"
fi
if [ ! -d "/data/web_static/shared/" ];
then sudo mkdir -p "/data/web_static/shared/"
fi
if [ ! -d "/data/web_static/releases/test/" ];
then sudo mkdir -p "/data/web_static/releases/test/"
fi
sudo bash -c " echo 'this is a test' > '/data/web_static/releases/test/index.html'"
sudo ln -sf "/data/web_static/releases/test/" "/data/web_static/current"
sudo chown -hR "ubuntu:ubuntu" "/data/"
FIND=$(grep "/hbnb_static/" /etc/nginx/sites-enabled/default)
if [[ -z $FIND ]]; then
sudo sed -i "40i\	location /hbnb_static/ {\n\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-enabled/default
fi
sudo service nginx start
