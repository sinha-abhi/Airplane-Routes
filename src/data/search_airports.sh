#!/bin/bash

# Create file with list of unfound airports
> missing_airports.txt
echo Searching for missing airports...
cat airport_names.txt | cut -f 2 -d ',' | while read x
do
	line=`grep "$x" airport_coords.txt`
	if [ "$line" == "" ]; then
		echo $x >> missing_airports.txt
	fi
done
echo Done
