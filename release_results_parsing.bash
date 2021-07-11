#!/bin/bash

:<<purpose
    Парсинг информации о файлах и результата транскодинга в один файл 
purpose

f=`find ./Release_results -name "*_tc"`
for dir in $f
do
cd "${dir}"
f=`find -name "transcoding_info_std*"`
echo -e "\n${dir}"
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
done >> ./Parsed_results/release_results.txt