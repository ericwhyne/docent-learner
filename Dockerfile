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

WORKDIR /home
RUN git clone https://github.com/mbartoli/docent-learner
WORKDIR /home/docent-learner

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

RUN mkdir -p ${basedir}

RUN mkdir "${basedir}/boldtext"
RUN chmod a+rw "${basedir}/boldtext"

RUN mkdir -p "${basedir}/${imagesdir}"
RUN cp images/* "${basedir}/${imagesdir}"
RUN chmod a+rw "${basedir}/${imagesdir}"

RUN mkdir -p "${basedir}/${tweetsdir}"
RUN cp tweets/* "${basedir}/${tweetsdir}"
RUN chmod a+rw "${basedir}/${tweetsdir}"

RUN mkdir -p "${basedir}/${textselectdir}"
RUN cp textselect/* "${basedir}/${textselectdir}"
RUN chmod a+rw "${basedir}/${textselectdir}"

# Copy python source
RUN mkdir -p "${pydir}"
RUN cp -r src/* "${pydir}"

RUN mkdir -p "${basedir}/var/"
RUN cp -r var/* "${basedir}/var/"
RUN chmod a+rw "/var/www/html/docent-learner/var/config/config.json"
RUN chmod a+rw "/var/www/html/docent-learner/var/textselect-modelbuild.lock"
RUN chmod a+rw "/var/www/html/docent-learner/var/textselect-model-build-status.txt"

RUN mkdir -p "${basedir}/static/"
RUN cp -r static/* "${basedir}/static/"

RUN cp -r html/* "${basedir}"


RUN echo 'ServerName localhost' >> /etc/apache2/conf.d

RUN cp sites-enabled/docent-learner-apache.conf /etc/apache2/sites-enabled/
EXPOSE 80
