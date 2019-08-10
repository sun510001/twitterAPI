#!/bin/bash
function checkpy(){
     count=`ps -ef|grep $1|grep -v "grep"|wc -l`
     # echo $count
     sleep 1
     if [ 0 == "$count" ]
         then `nohup python3 -u 'tweetsearch.py' > python.log 2>&1 &`
     fi
}

while :
do
     checkpy python3
     sleep 960
done
