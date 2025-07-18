import json
import glob
import numpy as np

def load_fio_json(filepath):
    """
    Load a single FIO JSON file.
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def extract_job_metrics(job):
    """
    Extract some common performance metrics from a single job entry.
    Adjust the keys below based on which metrics you want to analyze.
    """
    metrics = {}

    # Read metrics
    read = job.get('read', {})
    metrics['read_io_bytes'] = read.get('io_bytes', 0)
    metrics['read_bw'] = read.get('bw', 0)
    metrics['read_iops'] = read.get('iops', 0)

    # For latency, we might be interested in the overall latency stats (lat_ns)
    lat_ns = read.get('lat_ns', {})
    metrics['read_latency_mean'] = lat_ns.get('mean', 0)
    metrics['read_latency_stddev'] = lat_ns.get('stddev', 0)

    # Optionally, you could extract additional metrics, e.g.:
    # metrics['clat_mean'] = read.get('clat_ns', {}).get('mean', 0)
    # metrics['clat_stddev'] = read.get('clat_ns', {}).get('stddev', 0)

    # Write metrics can be extracted similarly if needed
    write = job.get('write', {})
    metrics['write_io_bytes'] = write.get('io_bytes', 0)
    metrics['write_bw'] = write.get('bw', 0)
    metrics['write_iops'] = write.get('iops', 0)

    return metrics

def process_fio_logs(directory_path):
    """
    Process all JSON log files in a given directory.
    Returns a dictionary with aggregated lists of metrics.
    """
    # Define data structure to accumulate metrics across files
    aggregated_metrics = {
        'read_bw': [],
        'read_iops': [],
        'read_latency_mean': [],
        'read_latency_stddev': [],
        'write_bw': [],
        'write_iops': [],
        # Add more keys as needed
    }

    # Loop through all JSON files in the directory
    for filepath in glob.glob(f"{directory_path}/*.json"):
        data = load_fio_json(filepath)
        jobs = data.get('jobs', [])

        # If multiple jobs exist per file, iterate through each
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
    Compute the average and standard deviation for a list of values.
    """
    avg = np.mean(metric_values)
    stddev = np.std(metric_values)
    return avg, stddev

def compare_to_baseline(test_stats, baseline_stats, stddev_threshold):
    """
    Compare test statistics to baseline values.

    Parameters:
    - test_stats: A dictionary with keys like 'read_bw', 'read_latency_stddev', etc.
    - baseline_stats: A similar dictionary of baseline averages (or you can include baseline stddev)
    - stddev_threshold: The threshold above which the test is flagged

    Returns a result dictionary where each metric is flagged if its standard deviation exceeds the threshold.
    """
    comparison_results = {}
    for metric, (avg, stddev) in test_stats.items():
        baseline_value = baseline_stats.get(metric)
        # Example: flag if the standard deviation exceeds the threshold.
        flag = stddev >= stddev_threshold
        comparison_results[metric] = {
            "test_avg": avg,
            "test_stddev": stddev,
            "baseline": baseline_value,
            "flagged": flag
        }
    return comparison_results

def main():
    # Example directory where your FIO JSON logs are stored.
    logs_directory = "4k"

    # Process logs to aggregate metrics
    aggregated_metrics = process_fio_logs(logs_directory)

    # Compute statistics (average and stddev) for each metric
    test_stats = {}
    for metric, values in aggregated_metrics.items():
        if values:  # Avoid division by zero on empty lists
            test_stats[metric] = compute_statistics(values)
        else:
            test_stats[metric] = (0, 0)

    # Example baseline stats (you would define these from your known good logs)
    baseline_stats = {
        'read_bw': 20020544,        # e.g., expected bandwidth in bytes/sec
        'read_iops': 5005136.04,      # expected IOPS
        'read_latency_mean': 37.0,    # expected average latency in ns
        'read_latency_stddev': 43.0,  # expected stddev for latency
        'write_bw': 0,
        'write_iops': 0,
    }

    # Define your standard deviation threshold for flagging deviations.
    stddev_threshold = 50  # Adjust as needed

    # Compare the computed stats against the baseline
    comparison_results = compare_to_baseline(test_stats, baseline_stats, stddev_threshold)

    # Write the comparison results to a text report
    with open("comparison_report.txt", "w") as report:
        for metric, result in comparison_results.items():
            line = (f"{metric}: Test Avg = {result['test_avg']:.2f}, "
                    f"Test STDDEV = {result['test_stddev']:.2f}, "
                    f"Baseline = {result['baseline']}, "
                    f"Flagged = {result['flagged']}\n")
            report.write(line)

    print("Comparison report generated as 'comparison_report.txt'.")

if __name__ == "__main__":
    main()
