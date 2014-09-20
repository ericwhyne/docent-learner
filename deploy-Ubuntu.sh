#!/bin/bash

# Make directories, copy files, and check permissions
sudo cp sites-enabled/docent-learner-apache.conf /etc/apache2/sites-enabled/

sudo mkdir /var/www/html/images
sudo cp images/* /var/www/html/images
sudo chmod a+rw /var/www/html/images

sudo mkdir /var/www/docent-learner
sudo cp src/images.py /var/www/docent-learner

sudo mkdir /var/www/docent-learner/config
sudo cp config/* /var/www/docent-learner/config/

sudo rm /var/www/html/index.html
sudo cp src/index.html /var/www/html/

sudo service apache2 restart
