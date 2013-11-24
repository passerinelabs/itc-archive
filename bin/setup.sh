#!/bin/bash

echo "*** Creating directories"
mkdir -p archive/daily archive/weekly archive/monthly depot java

echo "*** Downloading Autoingestion tool"
curl -s -O http://www.apple.com/itunesnews/docs/Autoingestion.class.zip

echo "*** Extracting Autoingestion tool"
unzip -p Autoingestion.class.zip Autoingestion/Autoingestion.class  > java/Autoingestion.class

echo "*** Cleaning up"
rm Autoingestion.class.zip
