#!/usr/bin/env bash

INFO='\033[0;36m'
WARNING='\033[0;33m'
DANGER='\033[0;31m'
SUCCESS='\033[0;32m'
NORMAL='\033[0;37m'
SUBDUED='\033[1;30m'
vagrant='\033[0;35m'

clear
echo -e "${INFO}Updating repositories...${SUBDUED}"
# Python 3.8
sudo add-apt-repository -y ppa:deadsnakes/ppa
# Postgres
sudo apt-get install wget ca-certificates -y
# wget -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
# sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RELEASE=$(lsb_release -cs)
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list

sudo apt-get update -y
sudo apt-get upgrade -y

echo -e "${INFO}Installing userspace tools...${SUBDUED}"
sudo apt install -y git 
sudo apt install -y curl 
sudo apt install -y zsh 
sudo apt install -y tmux 
sudo apt install -y figlet
sudo apt install -y dos2unix
clear
echo -e "${vagrant}"
figlet -ctf banner {{ cookiecutter.project }}

echo -e "${INFO}Installing build tools...${SUBDUED}"
sudo apt install -y software-properties-common
sudo apt install -y build-essential

echo -e "${INFO}Installing libraries...${SUBDUED}"
sudo apt install -y libssl-dev
sudo apt install -y zlib1g-dev
sudo apt install -y libbz2-dev
sudo apt install -y libreadline-dev
sudo apt install -y llvm
sudo apt install -y libpq-dev
sudo apt install -y libjpeg-dev
sudo apt install -y libxslt1-dev 
sudo apt install -y zlib1g-dev 
sudo apt install -y libffi-dev
sudo apt install -y libssl-dev
sudo apt install -y libxslt1-dev 
sudo apt install -y libevent-dev 
sudo apt install -y libsasl2-dev 
sudo apt install -y libldap2-dev 
sudo apt install -y pkg-config 
sudo apt install -y libtiff5-dev 
sudo apt install -y libjpeg8-dev 
sudo apt install -y libjpeg-dev 
sudo apt install -y zlib1g-dev 
sudo apt install -y libfreetype6-dev 
sudo apt install -y liblcms2-dev 
sudo apt install -y liblcms2-utils 
sudo apt install -y libwebp-dev 
sudo apt install -y tcl8.6-dev 
sudo apt install -y tk8.6-dev 
sudo apt install -y python-tk 
sudo apt install -y libyaml-dev

echo -e "${INFO}Installing Python...${SUBDUED}"
sudo apt install -y python3.8 python3.8-dev python3.8-distutils python3-pip

echo -e "${INFO}Installing Web Server...${SUBDUED}"
sudo apt install -y nginx nginx-extras

echo -e "${INFO}Installing RabbitMQ...${SUBDUED}"
sudo apt install -y rabbitmq-server
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
sudo rabbitmq-plugins enable rabbitmq_management

echo -e "${INFO}Installing PostgreSQL...${SUBDUED}"
sudo apt install -y postgresql-11 postgresql-server-dev-11 postgresql-contrib

echo -e "${INFO}Finsihing up...${SUBDUED}"
sudo apt-get clean -y
sudo chown -R vagrant:vagrant /var/www/html
sudo chown -R vagrant:vagrant /{{ cookiecutter.app_folder }}

echo -e "${SUCCESS}"
figlet -ctf banner Done!
