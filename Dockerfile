FROM ubuntu:14.04
MAINTAINER Michael Bartoli <michael.bartoli@pomona.edu>

RUN apt-get update
RUN apt-get -y install \
	python \
	build-essential \
	python-dev \
	python-pip \
	git \
	vowpal-wabbit

RUN pip install nltk


