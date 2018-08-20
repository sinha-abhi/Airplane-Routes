#!/bin/bash

# Get airplane route data for the passed tail number
if [ $# -lt 2 ]; then 
	echo "usage: bash data_setup.sh [file] [tail_num]" 
	exit 1
fi

> plane_data.csv
filename=$1
tailnum=$2
echo "Searching for tail num $tailnum in file $filename..."
grep $tailnum $filename > plane_data.csv
sed -i -e "s/\"$tailnum\",//g" plane_data.csv
echo "Done"

if [ ! -s plane_data.csv ]; then
	echo "Failed to find tail number in data file"
	exit 1
fi

# Clean up airport name file
echo "Cleaning up airport name file..."
if [ ! -s airport_names.txt ]; then
	> airport_names.txt
	sed 1d L_AIRPORT_ID.csv | while read line
	do
		line=`echo $line | sed 's/"//g'`
		code=`echo $line | sed 's/"//g' | cut -f 1 -d ','`
		name=`echo $line | cut -f 2- -d ':' | sed 's/[^a-zA-Z0-9]/ /g'`
		echo $code,$name >> airport_names.txt
	done
	echo "Done"
else
	echo "Airport name file already exists, skipping clean up"
fi

#  Map airport codes to airport names
echo "Mapping airport codes to their names..."
cat airport_names.txt | while read line
do
	code=`echo $line | cut -f 1 -d ','`
	name=`echo $line | cut -f 2 -d ','`
	sed -i -e "s/$code/$name/g" plane_data.csv
done
sed -i -e 's/, /,/g' plane_data.csv
echo "Done"

# Clean up airport coordinates
echo "Cleaning up airport coordinates file..."
if [ ! -s airport_coords.txt ]; then
	> airport_coords.txt 
	cat AIRPORT_GPS_COORD.csv | while read line
	do
		line=`echo $line | sed 's/"//g'`
		airportname=`echo $line | cut -f2 -d,`
		lat=`echo $line | cut -f7 -d,`
		long=`echo $line | cut -f8 -d,`
		echo "$airportname,$lat,$long" >> airport_coords.txt 
	done
	sed -i -e 's/\///g' airport_coords.txt
	sed -i -e 's/ Airport//g' airport_coords.txt
	echo "Done"
else
	echo "Airport coordinates file already exists, skipping clean up"
fi

# Map airport names to coordinates
echo "Mapping airport names to their coordinates..."
cat airport_coords.txt | while read line
do
	name=`echo $line | cut -f 1 -d ','`
	coord=`echo $line | cut -f 2- -d ','`
	sed -i -e "s/$name/$coord/g" plane_data.csv
done
echo "Done"
