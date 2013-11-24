itc-archive
===========

Python tool to archive reports from Apple's iTunes Connect service.

Installation
------------

This is roughly what needs to happen to get itc-archive working.

* Download the source

    $ git clone https://github.com/passerinelabs/itc-archive.git

* Change directory into the itc-archive root dir

    $ cd itc-archive

* Run the setup script. This will download the java Autoingestion.class file from Apple.

    $ ./bin/setup.sh

* Set your iTunes Connect password in the properties file
 
   $ vim conf/autoingestion.properties

* Set your Apple vendor id and start date for your App

    $ vim bin/itc.py
