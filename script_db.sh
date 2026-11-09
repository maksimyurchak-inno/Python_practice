#!/usr/bin/env bash
# Shebang: instructs the OS to run the script using the Bash shell

# Pause before the window closes, even if an error occurs
trap 'read -r -p "Press Enter to close..."' EXIT

# Exit on error: aborts the script immediately if any command returns a non-zero exit code
set -e

# Run schema setup, loader, and extractor in sequence
python json_db.py
python loader.py
python extractor.py

echo "Pipeline finished. Output written to query_results.json"