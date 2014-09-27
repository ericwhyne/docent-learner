docent-learner
==============

Docent-learner is a web interface which statelessly and randomly traverses digital collections of images or text and asks users to answer questions or tag the content. This software was designed for quickly creating domain specific training sets for machine learning tasks. It was written in a few hours during a DARPA hackathon when it was discovered that there was no simple and easy free software that did this. The goal of this project is to make deploying functionality for creating training data sets simple, scalable, and provide a clutter-free interface that allows for fast tagging by many users.

* Docent - _A person who acts as a guide, typically on a voluntary basis, in a museum, art gallery, or zoo._
* Learner - _A person who is learning a subject or skill._

Capabilities and road map/TODO:
- Image tagging is currently supported. 
- A text selection interface is under development and mostly complete.
- Integration with AWS S3 and HBase/Accumulo is planned.
- The ability to refine and train machine learning models (rather than just tag data) is also potentially a part of this project.
- Eventually all capabilities should be controlled through the web interface. Rudimentary data binding for configuration modification is mostly implemented.
- At this time there is no authentication or security safety features since during the hackathon we deployed it on an internal network.   

The easiest way to get started with Docent Learner is to use Vagrant. For more information on Vagrant go to https://www.vagrantup.com/

Entering these commands into a machine with Vagrant will result in a fully functional Docent-Learner install:
```
git clone https://github.com/ericwhyne/docent-learner.git
cd docent-learner
vagrant up
```
Then point your browser at your computer: http://127.0.0.1:8080/docent-learner/dl/images.py

To add your own images and tags, ssh into the running Vagrant machine:
```
vagrant ssh
```
Then delete all files in /var/www/html/docent-learner/images and replace them with your own images.
Modify this file and enter your own form questions:
```
sudo vim /var/www/html/docent-learner/var/config/image_questions.form
```

As your images become tagged, a json file will be written to disk for each image. To aggregate these results into a single json file, use the aggregate tool in the utils directory.
```
vagrant@docent-learner:/vagrant/utils$ ./aggregate-images-json.sh 
Filename: 2014-09-27-image-tags.json
vagrant@docent-learner:/vagrant/utils$ cat 2014-09-27-image-tags.json 
[
/var/www/html/docent-learner/images/{ "has_labrador":"true","tagged_image":"dog-with-stick.jpg"},
/var/www/html/docent-learner/images/{ "is_dog":"true","tagged_image":"doxen-race.jpeg"},
/var/www/html/docent-learner/images/{ "has_labrador":"true","tagged_image":"puppies-in-grass.jpeg"}
]
vagrant@docent-learner:/vagrant/utils$ 
```
As currently configured, the docent Learner interface will only allow an image to be tagged once however if a user clicks the back button on their browser to re-tag an image it will result in two records in the file's json file. How these redundant tags are deconflicted is up to the developer using them during the creation of their machine learning model.

To deploy this software directly on an Ubuntu system:
```
sudo apt-get -y install apache2
sudo apt-get -y install libapache2-mod-wsgi
./deploy-Ubuntu.sh
```
