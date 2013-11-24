itc-archive
===========

Python tool to archive reports from Apple's iTunes Connect service.

Installation
------------

This is roughly what needs to happen to get itc-archive working.

Download the source

```
git clone https://github.com/passerinelabs/itc-archive.git
```

Change directory into the itc-archive root directory

```
cd itc-archive
```

Run the setup script. This will download the java Autoingestion.class file from Apple.

```
./bin/setup.sh
```

Set your iTunes Connect password in the properties file

``` 
vim conf/autoingestion.properties
```

Set your Apple vendor id and start date for your App

```
vim bin/itc.py
```

Archiving your sales reports
----------------------------

First you must change directories into the itc-archive root directory.

```
cd itc-archive
```

Then you can run the itc.py script.

```
./bin/itc.py
```

This will download all available daily, weekly, and monthly sales reports to the
`archive/` directory. You can run the `itc.py` script again and it will not
attempt to download any reports which have alreay been retrieved. This means you
can just setup a cron job to run the script a few times each day to make sure
your archives are up to date.

