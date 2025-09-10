#!/bin/sh

input_file="../ex02/hh_sorted.csv"
output_file="hh_positions.csv"

rm -rf "$output_file"

echo "\"id\",\"created_at\",\"name\",\"has_test\",\"alternate_url\"" > "$output_file"

while IFS= read -r line; do
    if [ "$line" = '"id","created_at","name","has_test","alternate_url"' ]; then
        continue
    fi
    
    id=$(echo "$line" | awk -F',' '{print $1}')
    created_at=$(echo "$line" | awk -F',' '{print $2}')
    name=$(echo "$line" | awk -F',' '{for (i=3; i<NF; i++) printf $i ","; print $NF}' | sed 's/"//g')
    has_test=$(echo "$line" | awk -F',' '{print $(NF-1)}')
    alternate_url=$(echo "$line" | awk -F',' '{print $NF}')

    position=$(echo "$name" | grep -oE '(Junior|Middle|Senior)' | tr '\n' '/' | sed 's/\/$//')
    
    if [ -z "$position" ]; then
        position="-"
    fi

    echo "$id,$created_at,\"$position\",$has_test,$alternate_url" >> "$output_file"
done < "$input_file"