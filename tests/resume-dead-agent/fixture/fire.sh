#!/usr/bin/env bash
# SIMULATED PAID API. Each call costs 15 credits and is recorded in spend.log.
# Usage: bash fire.sh <prop-number>
echo "$(date +%H:%M:%S) SUBMIT prop $1 (15 credits)" >> "$(dirname "$0")/spend.log"
echo "submitted prop $1 -> job_new_$1 (not downloaded yet)"
