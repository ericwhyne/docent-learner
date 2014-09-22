#!/bin/bash

#TODO: make apache restart optional

# Make directories, copy files, and check permissions
sudo cp sites-enabled/docent-learner-apache.conf /etc/apache2/sites-enabled/

sudo mkdir /var/www/html/images
sudo cp images/* /var/www/html/images
sudo chmod a+rw /var/www/html/images

sudo mkdir /var/www/html/textselect
sudo cp textselect/* /var/www/html/textselect
sudo chmod a+rw /var/www/html/textselect

# Copy python source
sudo mkdir /var/www/docent-learner
sudo cp src/* /var/www/docent-learner

# Set up Admin directories
sudo mkdir /var/www/html/uploads
sudo chmod a+rw /var/www/html/uploads

# Copy var files (stuff that changes during runtime)
sudo mkdir /var/www/html/var/
sudo cp -r var/* /var/www/html/var

# Copy static files (stuff that should never change)
sudo mkdir /var/www/html/static/
sudo cp -r static/* /var/www/html/static

# Copy html
sudo rm /var/www/html/index.html
sudo cp html/index.html /var/www/html/

# Restart apache after deploying .conf file
#sudo service apache2 restart
