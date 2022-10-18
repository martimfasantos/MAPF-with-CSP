#!/bin/sh

files=()
for i in {1..20}; do
	files+=("$i")
done

while getopts ":f:" option; do
    case $option in
        f ) files=("$OPTARG");;
    esac 
done

for w in ${files[@]}; do
	w=$(printf %02d $w)

	echo $(python proj.py graph/ex$w-graph.txt scen/ex$w-scen.txt)
done

