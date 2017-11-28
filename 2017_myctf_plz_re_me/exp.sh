#!/bin/bash
printable="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\"!#$%&'()*+,-./:;<=>?@[\\]^_\`{|}~ "

function set_key_padding() {
    unset key_padding
    local i
    for i in `seq 1 $1`
    do
        key_padding=${key_padding}${printable:0:1}
    done
}

for kindex in {1..8} 
do
    for i in `seq 0 $((${#printable}-1))`
    do
        set_key_padding $((7-${#key_known}))
        key=${key_known}${printable:$i:1}${key_padding}
        echo "trying "${key}
        count_array[$i]=`echo ${key} | ./pin -t ./inscount0.so -- ./a.out >> /dev/null ; cat inscount.out | cut -d " " -f 2`
        echo ${count_array[$i]}
    done

    max_count=${count_array[0]}
    max_index_array=(0)
    for i in `seq 1 $((${#printable}-1))`
    do
        if ((${max_count} == ${count_array[$i]}))
        then
            max_index_array=($max_index_array $i)
        fi

        if ((${max_count} < ${count_array[$i]}))
        then
            max_count=${count_array[$i]}
            max_index_array=($i)
        fi
    done

    if ((${#max_index_array[@]} > 1))
    then
        echo "It seems multiple candidates appeared..."
        for i in `seq 0 $((${#max_index_array[@]}-1))`
        do
            echo ${printable:${max_index_array[$i]}:1}
        done
    fi

    key_known=${key_known}${printable:${max_index_array[0]}:1}
    echo "known key: "${key_known}

done
