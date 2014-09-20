#!/bin/bash

# Install and configure Apache Web Server
sudo apt-get -y install apache2
sudo apt-get -y install libapache2-mod-wsgi


# Run the deployment scripts
cd /vagrant
./deploy-Ubuntu.sh
