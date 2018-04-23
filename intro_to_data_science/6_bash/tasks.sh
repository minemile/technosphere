#!/usr/bin/env bash

echo "First task"
grep "GET" logs/2049-03-{09,11}*.tsv | cut -f3 | sort -n | uniq -c | sort | awk '{print $2}' | tail

echo "Second task"
cut -f3 logs/* | sort -n | uniq -c | awk '$1 > 150' | wc -l | awk '{print $1}'
