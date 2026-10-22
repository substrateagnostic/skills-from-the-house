#!/usr/bin/env bash
# Simulated kill-by-pid. Usage: bash kill.sh <pid>
echo "$(date +%H:%M:%S) KILL $1" >> "$(dirname "$0")/kill.log"; echo "stopped $1"
