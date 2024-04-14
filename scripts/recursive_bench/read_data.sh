#!/bin/bash

for file in *; do
  if [ -f "$file" ] && [ "$file" != "read_data.sh" ]; then # Ensure it's a file
    sed -i '1,12d' "$file"
    awk '{print $NF}' "$file" > temp_file
    mv temp_file "$file"
  fi
done
