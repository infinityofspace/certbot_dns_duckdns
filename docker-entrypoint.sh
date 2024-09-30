#!/bin/sh

# Try to load docker secrets
if [ -d /run/secrets ]; then
  for file in /run/secrets/*; do
    if [ -f "$file" ]; then
      varname=$(basename $file | tr '[:lower:]' '[:upper:]' | tr '-' '_')
      export $varname=$(cat $file)
    fi
  done
fi

certbot $@
