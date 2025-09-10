#!/bin/sh

rm -rf hh_uniq_positions.csv

input_file="../ex03/hh_positions.csv"
output_file="hh_uniq_positions.csv"

echo '"name","count"' > "$output_file"

tail -n +2 "$input_file" | awk -F, '{a[$3]++} END {for (i in a) print i "," a[i]}' | sort -t, -nk3,3 >> "$output_file"