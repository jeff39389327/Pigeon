#!/bin/bash

folder_path="/home/train"
cd "$folder_path"

for file in *; do
    if [ -f "$file" ]; then
        base=${file%.*}
        extension=${file##*.}
        counter=1
        new_file="${base}(${counter}).${extension}"
        while [ -f "$new_file" ]; do
            let counter+=1
            new_file="${base}(${counter}).${extension}"
        done
        cp "$file" "$new_file"
    fi
done
