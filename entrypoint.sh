#!/usr/bin/env sh
set -e

# Seed default only if the file does not already exist
if [ ! -f /data/distributions.csv ]; then
  mkdir -p /data
  cp /opt/defaults/distributions.csv /data/distributions.csv
fi

# Hand off to the main process
exec "$@"