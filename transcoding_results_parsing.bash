#!/bin/bash

:<<purpose
    Парсинг информации о файлах и результата транскодинга в один файл 
purpose

f=`find ./Samples -name "*_tc"`
for dir in $f
do
cd "${dir}"
f=`find -name "file_info.txt"`
for file in $f
do
while read line
do 
echo $line | grep "Complete name" 
echo $line | grep "Format"
echo $line | grep "Duration"
echo $line | grep "Bit rate"
echo $line | grep "Width"
echo $line | grep "Height"
echo $line | grep "Frame rate"
done < ${file:2}
done
f=`find -name "transcoding_info_test*"`
echo -e "\nstd"
let "i=0"
for file in $f
do
let "i=$i+1"
echo "Test $i"
while read line 
do 
echo $line | grep "User time"
echo $line | grep "System time"
echo $line | grep "Percent of CPU this job got"
echo $line | grep "Elapsed (wall clock) time"
done < ${file:2}
done
f=`find -name "transcoding_info_tc*"`
echo -e "\ntc_malloc"
let "i=0"
for file in $f
do
let "i=$i+1"
echo "Test $i"
while read line
do
echo $line | grep "User time"
echo $line | grep "System time"
echo $line | grep "Percent of CPU this job got"
echo $line | grep "Elapsed (wall clock) time"
done < ${file:2}
done
echo -e "\n"
cd ../../
done >> parsed.txt

