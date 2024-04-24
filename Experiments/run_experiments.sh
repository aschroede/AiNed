#!/bin/bash
# Note that before running this file you must have installed ained either via
# 1. pip install ained
# 2.

# Climb two directories up and add to pythonpath so python knows where to hunt for ained module
new_path="$(dirname "$(pwd)")"

# Check if already in PYTHONPATH
if [[ ":$PYTHONPATH:" != *":$new_path:"* ]]; then
  export PYTHONPATH="$new_path:$PYTHONPATH"
fi

input_dir="Inputs"
output_dir="Outputs"

# Create output directory
[ ! -d "$output_dir" ] && mkdir -p "$output_dir"

# Get total number of files for progress
total_files=$(ls -1 "$input_dir" | wc -l)
current_file=0

# Loop over each input file and process it
for input_file in "$input_dir"/*
do
  ((current_file++))
  filename=$(basename "$input_file")
  filename="${filename%.*}"
  output_file="$output_dir/${filename}-result"

  echo -ne "Processing $current_file of $total_files files\r"
  python3 -m ained.main process-file "$input_file" "$output_file"
done

echo -ne "\nFinished processing files.\n"