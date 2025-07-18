#!/usr/bin/env bash
# FIO-Plot functionality test chart generator for major chart types

#[  2D Bar Graph, Queue-Depth
#[-----------------------------------------------------------------------------]
#[ type of data to graph from logs located in the input dir, choose one of:
#[  -r   {read,write,rw,readwrite,
#[         randread,randwrite,randrw,
#[         trim,randtrim,trimwrite}
#[  --rw == long-form for '-r'
#[  ^ these flags are apparently the same, oddly not descriptive for long-arg
#[-----------------------------------------------------------------------------]
time ~/.local/bin/fio-plot \
     --input-directory ./nullprocess.tmp/benchmark/null/4k \
     --source "Jump" \
     --title "Null Engine on EPYC 4564P" \
     --bargraph2d-qd \
     --rw randread \
