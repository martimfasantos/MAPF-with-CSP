#! /bin/sh

files=()
for i in {1..20}; do
	files+=("$i")
done

VERBOSE=false
while getopts ":vf:" option; do
    case $option in
        v ) VERBOSE=true;;
        f ) files=("$OPTARG");;
    esac 
done

for w in ${files[@]}; do
    echo "Printing file $w"

	w=$(printf %02d $w)

    result=$(timeout 100 python proj.py graph/ex$w-graph.txt scen/ex$w-scen.txt > solution.txt)

    if [ $VERBOSE = true ]; then
	    cat solution.txt
    fi
    echo
done

