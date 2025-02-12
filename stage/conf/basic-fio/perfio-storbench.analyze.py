#!/usr/bin/env python3
'''
[───────────────────────────────────────────────────────────────────────────────]
[ Purpose    ─» Block Storage Analysis: bench, plot, analyze, report [BPAR]
[ Filename   ─» perfio-storbench.analyze.py
[ Project    ─» PerfIO-StorBench
[ Author     ─» Eva Winterschön
[ License    ─» BSD-6-Clause
[ Date-INIT  ─» 2024-0802
[ Date-RMOD  ─» 2024-1110
[ Version    ─» 0.4.6
[───────────────────────────────────────────────────────────────────────────────]
[ Requires
[ ╰───────────» python3
[           ╰─» jinja2
[           ╰─» jinja2-cli
[           ╰─» numpy
[───────────────────────────────────────────────────────────────────────────────]
[ References
[ ╰───────────» ⌄unten⌄
[ • PEP-008  ─» [PEP-8 Style Guide](https://peps.python.org/pep-0008/)
[ • PEP-257  ─» [Docstrings Ref](https://peps.python.org/pep-0257/)
[ • PEP-324  ─» [SubProcess Module](https://peps.python.org/pep-0324/)
[ • Doc-Sig  ─» [Py Docs](https://www.python.org/community/sigs/current/doc-sig/)
[───────────────────────────────────────────────────────────────────────────────]
'''
# Erforderlich Modules
import argparse
import jinja2
import os
import psutil
import shutil
import subprocess
import sys
import json
import glob
import numpy as np

# Validate src-layout import adjustment
if not __package__:
    '''
    Check if using 'src-layout' hierarchy method of app development, if so then
    adjust import path to ensure functionality if called via 'src/package'
    https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
    '''
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)


def load_fio_json(filepath):
    """
    PROC: load the JSON
    RET: data
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def extract_job_metrics(job):
    """
    Extract common perf metrics from a single job entry
    TODO: adjust metrics into conf vars array
    """
    metrics = {}

    # Read 'em
    read = job.get('read', {})
    metrics['read_io_bytes'] = read.get('io_bytes', 0)
    metrics['read_bw'] = read.get('bw', 0)
    metrics['read_iops'] = read.get('iops', 0)

    # For latency eval, overall stats are (lat_ns)
    lat_ns = read.get('lat_ns', {})
    metrics['read_latency_mean'] = lat_ns.get('mean', 0)
    metrics['read_latency_stddev'] = lat_ns.get('stddev', 0)

    # Also, because we love numbers, we get the mean and stddev
    metrics['clat_mean'] = read.get('clat_ns', {}).get('mean', 0)
    metrics['clat_stddev'] = read.get('clat_ns', {}).get('stddev', 0)

    # Same deal but for write based workloads
    write = job.get('write', {})
    metrics['write_io_bytes'] = write.get('io_bytes', 0)
    metrics['write_bw'] = write.get('bw', 0)
    metrics['write_iops'] = write.get('iops', 0)

    # TODO: wrap the metrics calls w/ error|fail state codes
    # TODO: basic exception handler raise func is limited, go find the lib from summer 2018
    # TODO: how can we live with outselves w/o syslog & ES APM trace loggers?!
    return metrics

def process_fio_logs(directory_path):
    """
    PROC: all json logs in dir path
    RET: dict of aggregated lists of metrics
    """
    # data struct for accumulation metrics across files
    aggregated_metrics = {
        'read_bw': [],
        'read_iops': [],
        'read_latency_mean': [],
        'read_latency_stddev': [],
        'write_bw': [],
        'write_iops': [],
	# TODO: more, especially rollups
    }

    # aka LogGlobbing()
    for filepath in glob.glob(f"{directory_path}/*.json"):
        data = load_fio_json(filepath)
        jobs = data.get('jobs', [])

        for job in jobs:
            metrics = extract_job_metrics(job)

            aggregated_metrics['read_bw'].append(metrics.get('read_bw', 0))
            aggregated_metrics['read_iops'].append(metrics.get('read_iops', 0))
            aggregated_metrics['read_latency_mean'].append(metrics.get('read_latency_mean', 0))
            aggregated_metrics['read_latency_stddev'].append(metrics.get('read_latency_stddev', 0))

            aggregated_metrics['write_bw'].append(metrics.get('write_bw', 0))
            aggregated_metrics['write_iops'].append(metrics.get('write_iops', 0))

    return aggregated_metrics

def compute_statistics(metric_values):
    """
    PROC: Compute AVG & STD_DEV for list values
    RET: same
    """
    avg = np.mean(metric_values)
    stddev = np.std(metric_values)
    return avg, stddev

def compare_to_baseline(test_stats, baseline_stats, stddev_threshold):
    """
    PROC: compare stats to baselines

    PARAMS:
    - test_stats: dict of keys, eg: 'read_bw', 'read_latency_stddev', etc
    - baseline_stats: initially a dict of baseline avgs, TODO: add baseline stddev to dict
    - stddev_threshold: var defining test-fail flag if result is > STDDEV thresh

    RET: dict containing each flagged metric from STDDEV threshhold overage evaluation
    """
    comparison_results = {}
    for metric, (avg, stddev) in test_stats.items():
        baseline_value = baseline_stats.get(metric)

        flag = stddev >= stddev_threshold
        comparison_results[metric] = {
            "test_avg": avg,
            "test_stddev": stddev,
            "baseline": baseline_value,
            "flagged": flag
        }

    return comparison_results

def main():
    # TODO: import usual argparser/confparse stuff from rfc1918 shared libs
    # TODO: put logs dir var into arg parse && conf file
    # Process... the... logs...
    logs_directory = "path/to/logs"
    aggregated_metrics = process_fio_logs(logs_directory)

    # Evaluate aggregated metrics, otherwise ignore
    test_stats = {}
    for metric, values in aggregated_metrics.items():
        if values:
            test_stats[metric] = compute_statistics(values)
        else:
            test_stats[metric] = (0, 0)
            # TODO: not now though, add metrics processing logic according to conf'd array of defined workflow needs

    """
    Static baseline metrics for comparative threshold evals and so on
    TODO: prefer sourcing / adapting from 'storage benchmark database' drive SKU table, which was customized for ZFS evals
    TODO: update w/ hardware type associatives, determinant of capacity static baselines
	  - SATA3{SPIN,SSD} -> somewhere.. 'verwalterin'?
          - SAS3{SPIN,SSD} -> nasa for SAS3-SPIN, R630 cluster for SAS3-SSD
          - PMEM{dax,dev-dax,etc} [see below]
          - NVMe-PCIe{gen3,gen4,gen5} -> Gen3 are in 'upgrayyed' but need offload to SAN, don't have gen4,gen5 yet (TBD)
          - Ceph/RDB{10G,25G,40/50G,100G} -> a variety of these baselines for different network link speeds should be memory-backed to ignore the vast potential of different disk configs
          - reference PMEM LT's from 'prinzessin' (Gentoo Q3'23, Optane-200 128GB DIMMs) or 'upgrayyed'(same box but Fedora Q3'24, Optane-200 512GB DIMMs) for diff DDR4-3200 perf limits
    """
    baseline_stats = {
        'read_bw': 20020544,          # bytes/sec
        'read_iops': 5005136.04,      # bare io/ps
        'read_latency_mean': 37.0,    # avg nanosec latency
        'read_latency_stddev': 43.0,  # stddev for latency
        'write_bw': 0,                # TBD for writes
        'write_iops': 0,              # TBD ...
	'write_latency_mean':0,       # TBD ...
	'write_latency_stddev':0      # TBD ...
    }

    # STDDEV Threshold for failures
    stddev_threshold = 50  # TODO: expand functionality for variable STDDEV w/ test criterias

    # Generate comparisons
    # TODO: account for additional workflows
    comparison_results = compare_to_baseline(test_stats, baseline_stats, stddev_threshold)

    #
    # TODO: pull the PDF report generator code from RFC1918
    # TODO: hook to fio-plot for generating graphs from the logs & include in report
    # TODO: grab db_conn lib, avoid MySQL's stupid locked-dir upload requirement in 8.x or add eval check before SQL exec
    # TODO: use ANSI SQL so that ClickHouse works without alterations to query
    # TODO: option flag to push report elsewhere via 'rclone', eg S3 or B2 bucket, others
    with open("perfio-storbench.comp-report.out", "w") as report:
        for metric, result in comparison_results.items():
            line = (f"{metric}: Test Avg = {result['test_avg']:.2f}, "
                    f"Test STDDEV = {result['test_stddev']:.2f}, "
                    f"Baseline = {result['baseline']}, "
                    f"Flagged = {result['flagged']}\n")
            report.write(line)

    print("Evaluation complete, see report in [perfio-storbench.comp-report.out]")

if __name__ == "__main__":
    main()
    # argparse/confparse
    # logs logs logs
    # error code maps
    # setup src-layout packaging
    # test w/ Cython
    # APM traces
