#!/bin/bash
:<<purpose
Транскодирование всех файлов в директории, сохранение информации о файле и результата транскодирования в отдельную директорию
purpose

f=`find ./Samples -name "*.mkv" -or -name "*.mp4" -or -name "*.yuv" -or -name "*.avi" -or -name "*.y4m" -or -name "*.mpg"  -or -name "*.mpeg" -or -name "*.mkv.md5" -or -name "*.md5sum" -or -name "*.qt" -or -name "*.mxf" -or -name "*.wmv" -or -name "*.AVI" -or -name "*.divx" -or -name "*.3gp" -or -name "*.webm" -or -name "*.ts"`
path="/home/aleksandr/Pract"
#ldd /usr/bin/ffmpeg | grep -e 'tcmalloc'
for file in $f
do
echo "--------Processing ${file} tc--------"
#mkdir "${file}_tc"
cd ./"${file}_tc"
mediainfo "../../${file}" >> file_info.txt
ldd /usr/bin/ffmpeg | grep -e 'tcmalloc'
/usr/bin/time -v /usr/bin/ffmpeg -i "../../${file}" -c:v libx264 -f mov "${path}${file:1}_tc"/"output_tc1".mov 2> transcoding_info_tc_test1.txt
/usr/bin/time -v /usr/bin/ffmpeg -i "../../${file}" -c:v libx264 -f mov "${path}${file:1}_tc"/"output_tc2".mov 2> transcoding_info_tc_test2.txt
/usr/bin/time -v /usr/bin/ffmpeg -i "../../${file}" -c:v libx264 -f mov "${path}${file:1}_tc"/"output_tc3".mov 2> transcoding_info_tc_test3.txt
cd ../../
done
#export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4
#for file in $f
#do
#echo "--------Processing ${file} tc_malloc--------"
#cd ./"${file}_tc"
#/usr/bin/time -v /usr/bin/ffmpeg -i "../../${file}" -c:v libx264 -f mov "${path}${file:1}_tc"/"output_tc1".mov 2> transcoding_info_tc_test1.txt
#/usr/bin/time -v /usr/bin/ffmpeg -i "../../${file}" -c:v libx264 -f mov "${path}${file:1}_tc"/"output_tc2".mov 2> transcoding_info_tc_test2.txt
#/usr/bin/time -v /usr/bin/ffmpeg -i "../../${file}" -c:v libx264 -f mov "${path}${file:1}_tc"/"output_tc3".mov 2> transcoding_info_tc_test3.txt
#cd ../../ 
#done