#!/bin/bash

# Create file with list of unfound airports
if [ $# -lt 1 ]; then
	echo "usage: bash search_airports.sh [file]"
	exit 1
fi

> missing_airports.txt
echo Searching for missing airports...
cat airport_names.txt | cut -f 2 -d ',' | while read x
do
	line=`grep "$x" "$1"`
	if [ "$line" == "" ]; then
		echo $x >> missing_airports.txt
	fi
done
echo Done
