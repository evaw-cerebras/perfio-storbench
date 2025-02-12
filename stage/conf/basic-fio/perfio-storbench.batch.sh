#!/usr/bin/env bash
# -*- mode: sh; sh-shell: bash; coding: utf-8-unix -*-
set -x -o pipefail

test -d log || mkdir log
rsync -ai --delete perfio-storbench.batch.fio perfio.fio

for job in $(cat perfio.raw.jobs); do
    job=$(echo ${job} | sed -e 's/\[//g' -e 's/\]//g')

    sudo time fio --output-format=json \
	 --eta=auto \
	 --eta-interval=10 \
	 --eta-newline=10 \
	 --status-interval=5 \
	 --output=log/perfio.${HOSTNAME}.${job}.log.json \
	 --section=${job} \
	 perfio.fio
done
