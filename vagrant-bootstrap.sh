#!/bin/bash
# This file contains stuff we only want to do once during provisioning.

sudo apt-get update
sudo apt-get upgrade

# Install and configure Apache Web Server
sudo apt-get -y install apache2
sudo apt-get -y install libapache2-mod-wsgi # needed to run have Apache run Python
sudo apt-get -y install apache2-utils # needed for htpasswd

# Install dependencies
sudo apt-get -y install python-nltk
sudo apt-get -y install vowpal-wabbit

# Create an admin account
adminpass=`tr -dc A-Za-z0-9_ < /dev/urandom | head -c 10`
adminuname='admin'
htpasswd -cb /etc/apache2/docent-learner-admin-pwfile $adminuname $adminpass
echo "$adminuname $adminpass" >> /vagrant/admin-password.txt

# Run the deployment scripts
cd /vagrant
./deploy-Ubuntu.sh
