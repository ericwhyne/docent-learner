docent-learner
==============
![schoolmaster](https://raw.githubusercontent.com/ericwhyne/docent-learner/master/static/AdriaenVanOstade-TheSchoolMaster.png)

Docent-learner is a web interface which statelessly and randomly traverses digital collections of images, text, or other content and asks users to answer questions or tag the content. This software was designed for quickly creating domain specific training sets for machine learning tasks. It was written in a few hours during a DARPA hackathon and has been iteratively improved as it's applied to different problem sets. The goal of this project is to make deploying functionality for creating training data sets simple, scalable, and provide a clutter-free interface that allows for fast tagging of big data by many users.

* Docent - _A person who acts as a guide, typically on a voluntary basis, in a museum, art gallery, or zoo._
* Learner - _A person who is learning a subject or skill._

Capabilities (mostly integrated):
- Supports arbitrarily large numbers of tagging users simultaneously
- Cookies to track tagger's user agent (aka browser) and session
- Mechanical Turk integration
- Image tagging
- Tweet tagging
- Text selection

Roadmap:
- The ability to refine and train machine learning models to make suggesions that might help taggers (allow the docent to learn as it goes). This is partially working and uses Vowpal Wabbit. 
- Gamification of tagging by setting up points system or rewards to emotionally and competitively involve taggers.

The easiest way to get started with Docent Learner is to use Vagrant. For more information on Vagrant go to https://www.vagrantup.com/

Entering these commands into a machine with Vagrant will result in a fully functional Docent-Learner install:
```
git clone https://github.com/ericwhyne/docent-learner.git
cd docent-learner
vagrant up
```
Then point your browser here: http://127.0.0.1:8081/docent-learner/

To add your own images and tags, ssh into the running Vagrant machine:
```
vagrant ssh
```
Then delete all files in /var/www/html/docent-learner/images and replace them with your own images.

Update your questions via the administration interface. Upon provisioning the password to the admin interface is randomized and available in the following file. Each time you provision, the new password will be appended to the file. This password file is in the .gitignore and will never be committed to the github repository through normal pushes or pull requests.
```
In the vagrant VM:
vagrant@docent-learner:~$ cat /vagrant/admin-password.txt
or on the host machine:
eric@glamdring:~/workspace/docent-learner$ cat admin-password.txt 
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
After deploying to the ubuntu system, the root interface will be at http://host-ip/docent-learner/ on the standard http port 80.


### Deploy with Docker
```
docker run -d -p 80:80 mbartoli/docent-learner
```
