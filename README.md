docent-learner
==============

Docent-learner is a web interface which statelessly and randomly traverses digital collections of images or text and asks users to answer questions or tag the content. This was built and designed for quickly creating domain specific training sets for machine learning tasks. It was written in a few hours during a DARPA hackathon when it was discovered that there was no good free software that did this. The goal of this project is to make deploying functionality for creating training data sets simple, scalable, and provide a clutter-free interface that allows for fast tagging by many users.

   Docent - A person who acts as a guide, typically on a voluntary basis, in a museum, art gallery, or zoo.
   Learner - A person who is learning a subject or skill.

Capabilities and road map:
- Image tagging is currently supported. 
- A text selection interface is under development and mostly complete.
- Integration with HBase, Impala, and S3 is planned.
- The ability to refine and train machine learning models (rather than just tag data) is also potentially a part of this project, however will be avoided if it adds too much complexity. 

The easiest way to get started with Docent Learner is to use Vagrant. For more information on Vagrant go to https://www.vagrantup.com/

Entering these commands into a machine with Vagrant will result in a fully functional Docent-Learner install:
```
git clone https://github.com/ericwhyne/docent-learner.git
cd docent-learner
vagrant up
```
Then point your browser at your computer: http://127.0.0.1/docent-learner/dl/images.py

To add your own images and tags, ssh into the running Vagrant machine:
```
vagrant ssh
```
Then delete all files in /var/www/html/docent-learner/images and replace them with your own images.
Modify this file and enter your own form questions:
```
sudo vim /var/www/html/docent-learner/var/config/image_questions.form
```

As your images become tagged, a json file will be written to disk for each image. To aggregate these results into a single json file, run these commands.
```
cat *.json | while read a; do echo $a, >> aggregate.json; done
sed -i '1s/^/[\n /' aggregate.json
sed -i '$s/,$/]/' aggregate.json
```

As currently configured, Docent Learner will only allow an image to be tagged once however if a user clicks the back button on their browser to re-tag an image it will result in two records in the file's json file. How these redundant tags are deconflicted is up to the developer using them during the creation of their machine learning model.

