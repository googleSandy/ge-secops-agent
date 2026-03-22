#!/bin/bash
# Replacement string
REPLACEMENT='source "$(dirname "$0")/.env"'

# Loop through provided arguments (filenames)
for file in "$@"; do
  if [ -f "$file" ]; then
    echo "Refactoring $file..."
    # On Mac sed -i '' is used for in-place editing.
    # This replaces the line starting with WEBHOOK_URL with the source command.
    sed -i '' "s|source "$(dirname "$0")/.env"
  else
    echo "Skip: $file not found."
  fi
done
