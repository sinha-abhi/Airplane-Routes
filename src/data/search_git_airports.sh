#!/bin/bash

# Search data file from GitHub
> /git_data/missing_airports.txt
echo Searching for missing airports from github database...
cat airport_names.txt | cut -f 2 -d ',' | while read x
do
	line=`grep "$x" 
