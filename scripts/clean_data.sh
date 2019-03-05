#!/bin/bash


if [ $# -lt 2 ]; then 
	echo "usage: $0 [data_file] [target_file]" 
    echo "warning: the target_file will be overwritten"
	exit 1
fi

echo "Creating target file in the data directory..."

file=../data/$2
> $file

# Based on the format from Transtats, we want data from columns 1, 2, and 5
cat $1 | while read line
do
    # We don't want the N in front of the N-Number if its there
    tailnum=`echo $line | cut -f 1 -d ',' | sed "s/^\"N/\"/"`
    org=`echo $line | cut -f 2 -d ','`
    dest=`echo $line | cut -f 5 -d ','`

    echo "$tailnum,$org,$dest" >> $file
done
echo "Done"


echo "Shutting down after script completion..."
shutdown now
