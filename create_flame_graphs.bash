#!/bin/bash
:<<purpose
Создание flame графов на debug сборке ffmpeg
purpose

f=`find ./Release_results -name "*.mkv" -or -name "*.mp4" -or -name "*.yuv" -or -name "*.avi" -or -name "*.y4m" -or -name "*.mpg"  -or -name "*.mpeg" -or -name "*.mkv.md5" -or -name "*.md5sum" -or -name "*.qt" -or -name "*.mxf" -or -name "*.wmv" -or -name "*.AVI" -or -name "*.divx" -or -name "*.3gp" -or -name "*.webm" -or -name "*.ts"`
path="/home/aleksandr/Pract/"
path_to_flame_graph_lib="/home/aleksandr/FlameGraph"
ldd /home/aleksandr/bin_debug/ffmpeg | grep -e 'tcmalloc'
for file in $f
do
echo "--------Processing ${file} std--------"
cd ./"${file}_tc"
cd "${path_to_flame_graph_lib}"
perf record -F 99 -ag -- /home/aleksandr/bin_debug/ffmpeg -i "${path}${file:1}" -c:v libx264 -f mov "${path}${file:1}_tc"/"output_std".mov
perf script | ./stackcollapse-perf.pl > out.perf-folded
cat out.perf-folded | ./flamegraph.pl > "${path}${file:1}_tc"/std_flame_graph.svg
cd ../../
done
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libtcmalloc_minimal.so.4
ldd /home/aleksandr/bin_debug/ffmpeg | grep -e 'tcmalloc'
for file in $f
do
echo "--------Processing ${file} tc_malloc--------"
cd ./"${file}_tc"
perf record -F 99 -ag -- /home/aleksandr/bin_debug/ffmpeg -i "${path}${file:1}" -c:v libx264 -f mov "${path}${file:1}_tc"/"output_tc".mov
perf script | ./stackcollapse-perf.pl > out.perf-folded
cat out.perf-folded | ./flamegraph.pl > "${path}${file:1}_tc"/tc_flame_graph.svg
cd ../../ 
done