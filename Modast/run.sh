#!/bin/bash

declare -a files=(
    #"/home/cristian/Downloads/random_T16384_R1.0_S10.0_data.json"
    #"./sequential_T32768_R500186.26208613266_S300.0_data.json"
    #"./fake_mock_56000.json"
    #"./three.json"
    "random_T2048_R2.0_S30.0_data.json"
    "sequential_T2048_R2.0_S30.0_data.json"
    "skew_T2048_R2.0_S30.0_data.json"
)

declare -a windows=(
    "2"
    #"2"
    #"4"
    #"8"
    #"16"
    #"32"
    #"64"
    #"128"
    #"256"
    #"512"
    #"1024"
    #"2048"
    #""
    #"4096"
    #"8192"
    #"16384"
    #"32768"
    #"-1"
)

t="true"

for f in "${files[@]}"
do
    # Suppose f = "/home/user/file.json"
    # Split filename by '/'
    words=$(echo $f | tr "/" "\n")
    # Result: ["home" "user" "file.json"]

    # Get last word
    for w in $words
    do
        file=$w
    done
    # Result: "file.json"

    # Remove everything after last '.' (remove .json)
    file=${file%.*}
    # Result: "file"

    for w in "${windows[@]}"
    do
        SECONDS=0
        echo Processing file $f with window $w
        python3 modast.py -f $f -w $w -s $t -separate $t -o "Result_${file}_${w}" -d "./eduardo_3_pequenos/"
        duration=$SECONDS
        echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
    done
done

