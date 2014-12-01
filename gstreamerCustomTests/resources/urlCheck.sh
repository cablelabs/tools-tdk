#!/bin/sh
yourURL=$1

temp=`curl --silent --head --fail "$yourURL" | head -1`
echo "Header is " $temp

if [ "$temp" != "" ]; then
    echo "File exists"
    exit 0
else
    echo "File doesnt exist"
    exit 1
fi

