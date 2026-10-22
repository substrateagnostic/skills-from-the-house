#!/usr/bin/env bash
# Fetch a finished job's result by id (free). Usage: bash fetch.sh <job_id> <prop-number>
echo "glb-bytes-$2" > "$(dirname "$0")/propforge/out/prop_$2.glb"
echo "$(date +%H:%M:%S) FETCH $1 -> prop_$2.glb (free)" >> "$(dirname "$0")/fetch.log"
echo "fetched $1"
