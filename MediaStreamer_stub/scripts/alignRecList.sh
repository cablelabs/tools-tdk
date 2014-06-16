#!/bin/bash
#This file will align the list of urls as one entry per line

grep . "${1}" | while read line
do
if [ "${line#*"#"}" != "$line" ]
    then
    echo -n $line
    else
    echo  $line
fi
done
