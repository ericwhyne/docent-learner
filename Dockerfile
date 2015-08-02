FROM ubuntu:14.04
MAINTAINER Michael Bartoli <michael.bartoli@pomona.edu>

RUN apt-get update
RUN apt-get -y install \
	python \
	build-essential \
	python-dev \
	python-pip \
	git \
	vowpal-wabbit \
	apache2 \
	libapache2-mod-wsgi \
	apache2-utils
RUN pip install nltk

# create admin account
ENV adminpass='admin'
ENV adminuname='admin'
RUN htpasswd -cb /etc/apache2/docent-learner-admin-pwfile ${adminuname} ${adminpass} 
RUN echo "$adminuname $adminpass" && echo "$adminuname $adminpass" >> /home/admin-password.txt

# server setup
ENV basedir="/var/www/html/docent-learner"
ENV imagesdir="images"
ENV tweetsdir="tweets"
ENV textselectdir="textselect"
ENV pydir="/var/www/docent-learner/"

#RUN mkdir -p ${basedir}
WORKDIR /var/www/html/

RUN git clone https://github.com/mbartoli/docent-learner

RUN mkdir "${basedir}/boldtext"
RUN chmod a+rw "${basedir}/boldtext"

WORKDIR /var/www/html/docent-learner

#RUN mkdir -p "${basedir}/${imagesdir}"
#RUN cp images/* "${basedir}/${imagesdir}"
RUN chmod a+rw "${basedir}/${imagesdir}"

#RUN mkdir -p "${basedir}/${tweetsdir}"
#RUN cp tweets/* "${basedir}/${tweetsdir}"
RUN chmod a+rw "${basedir}/${tweetsdir}"

#RUN mkdir -p "${basedir}/${textselectdir}"
#RUN cp textselect/* "${basedir}/${textselectdir}"
RUN chmod a+rw "${basedir}/${textselectdir}"

# Copy python source
RUN mkdir -p "${pydir}"
RUN cp -r src/* "${pydir}"

RUN chmod a+rw "/var/www/html/docent-learner/var/config/config.json"
RUN chmod a+rw "/var/www/html/docent-learner/var/textselect-modelbuild.lock"
RUN chmod a+rw "/var/www/html/docent-learner/var/textselect-model-build-status.txt"

RUN cp sites-enabled/docent-learner-apache.conf /etc/apache2/sites-enabled/
RUN service apache2 restart

