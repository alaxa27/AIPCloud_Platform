#!/usr/bin/env sh

cd /opt
apt-get -y update && apt-get -y upgrade
apt-get -y install vim docker.io

curl -o /usr/local/bin/docker-compose -L "https://github.com/docker/compose/releases/download/1.15.0/docker-compose-$(uname -s)-$(uname -m)"
chmod +x /usr/local/bin/docker-compose

git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt
cd /opt/letsencrypt
./letsencrypt-auto certonly --standalone -d api.aipcloud.io

cd /opt/AIPCloud_Platform
docker-compose build
