import psutil
import csv
import os
from time import sleep


def cpu_times():
    # Call psutil to get CPU times
    cpu_stats = psutil.cpu_times(percpu=False)

    # Extract the fields of interest
    data = {
        'User Time': cpu_stats.user,
        'System Time': cpu_stats.system,
        'Idle Time': cpu_stats.idle,
        'IO Wait': getattr(cpu_stats, 'iowait', None),
        'IRQ': getattr(cpu_stats, 'irq', None),
        'SoftIRQ': getattr(cpu_stats, 'softirq', None),
        'Steal': getattr(cpu_stats, 'steal', None),
        'Guest': getattr(cpu_stats, 'guest', None),
        'Guest Nice': getattr(cpu_stats, 'guest_nice', None)
    }

    # Define the CSV file name
    file_name = 'cpu_times.csv'

    # Check if the file exists or is empty
    file_exists = os.path.isfile(file_name)
    file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

    # Open the CSV file in append mode ('a')
    with open(file_name, 'a', newline='') as csvfile:
        # Define the appropriate headers for the CPU times
        fieldnames = ['User Time', 'System Time', 'Idle Time', 'IO Wait', 'IRQ', 'SoftIRQ', 'Steal', 'Guest', 'Guest Nice']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is new or empty
        if not file_exists or file_is_empty:
            writer.writeheader()

        # Write the current CPU times as a row in the CSV
        writer.writerow(data)


def cpu_times_per_core():
    # Get CPU times for each core
    cpu_stats_per_core = psutil.cpu_times(percpu=True)

    # Loop through each core and process its data
    for i, cpu_stats in enumerate(cpu_stats_per_core):
        # Extract the fields of interest for the current core
        data = {
            'User Time': cpu_stats.user,
            'System Time': cpu_stats.system,
            'Idle Time': cpu_stats.idle,
            'IO Wait': getattr(cpu_stats, 'iowait', None),
            'IRQ': getattr(cpu_stats, 'irq', None),
            'SoftIRQ': getattr(cpu_stats, 'softirq', None),
            'Steal': getattr(cpu_stats, 'steal', None),
            'Guest': getattr(cpu_stats, 'guest', None),
            'Guest Nice': getattr(cpu_stats, 'guest_nice', None)
        }

        # Define the CSV file name for this core
        file_name = f'cpu_times_core_{i+1}.csv'

        # Check if the file exists and is empty
        file_exists = os.path.isfile(file_name)
        file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

        # Open the CSV file in append mode ('a')
        with open(file_name, 'a', newline='') as csvfile:
            # Define the appropriate headers for CPU times
            fieldnames = ['User Time', 'System Time', 'Idle Time', 'IO Wait', 'IRQ', 'SoftIRQ', 'Steal', 'Guest', 'Guest Nice']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file is new or empty
            if not file_exists or file_is_empty:
                writer.writeheader()

            # Write the current CPU times as a row in the CSV
            writer.writerow(data)


def cpu_times_percent():
    # Call psutil to get CPU times percentages (system-wide)
    cpu_stats_percent = psutil.cpu_times_percent(percpu=False)

    # Extract the fields of interest
    data = {
        'User Time (%)': cpu_stats_percent.user,
        'System Time (%)': cpu_stats_percent.system,
        'Idle Time (%)': cpu_stats_percent.idle,
        'IO Wait (%)': getattr(cpu_stats_percent, 'iowait', None),
        'IRQ (%)': getattr(cpu_stats_percent, 'irq', None),
        'SoftIRQ (%)': getattr(cpu_stats_percent, 'softirq', None),
        'Steal (%)': getattr(cpu_stats_percent, 'steal', None),
        'Guest (%)': getattr(cpu_stats_percent, 'guest', None),
        'Guest Nice (%)': getattr(cpu_stats_percent, 'guest_nice', None)
    }

    # Define the CSV file name
    file_name = 'cpu_times_percent.csv'

    # Check if the file exists and is empty
    file_exists = os.path.isfile(file_name)
    file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

    # Open the CSV file in append mode ('a')
    with open(file_name, 'a', newline='') as csvfile:
        # Define the appropriate headers for CPU times percentage
        fieldnames = ['User Time (%)', 'System Time (%)', 'Idle Time (%)', 'IO Wait (%)', 'IRQ (%)', 'SoftIRQ (%)', 'Steal (%)', 'Guest (%)', 'Guest Nice (%)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is new or empty
        if not file_exists or file_is_empty:
            writer.writeheader()

        # Write the current CPU times percentages as a row in the CSV
        writer.writerow(data)


def cpu_times_percent_per_core():
    # Get CPU times percentages for each core
    cpu_stats_per_core = psutil.cpu_times_percent(percpu=True)

    # Loop through each core and process its data
    for i, cpu_stats in enumerate(cpu_stats_per_core):
        # Extract the fields of interest for the current core
        data = {
            'User Time (%)': cpu_stats.user,
            'System Time (%)': cpu_stats.system,
            'Idle Time (%)': cpu_stats.idle,
            'IO Wait (%)': getattr(cpu_stats, 'iowait', None),
            'IRQ (%)': getattr(cpu_stats, 'irq', None),
            'SoftIRQ (%)': getattr(cpu_stats, 'softirq', None),
            'Steal (%)': getattr(cpu_stats, 'steal', None),
            'Guest (%)': getattr(cpu_stats, 'guest', None),
            'Guest Nice (%)': getattr(cpu_stats, 'guest_nice', None)
        }

        # Define the CSV file name for this core
        file_name = f'cpu_times_percent_core_{i+1}.csv'

        # Check if the file exists and is empty
        file_exists = os.path.isfile(file_name)
        file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

        # Open the CSV file in append mode ('a')
        with open(file_name, 'a', newline='') as csvfile:
            # Define the appropriate headers for CPU times percentage
            fieldnames = ['User Time (%)', 'System Time (%)', 'Idle Time (%)', 'IO Wait (%)', 'IRQ (%)', 'SoftIRQ (%)', 'Steal (%)', 'Guest (%)', 'Guest Nice (%)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header only if the file is new or empty
            if not file_exists or file_is_empty:
                writer.writeheader()

            # Write the current CPU times percentages as a row in the CSV
            if data['Idle Time (%)'] != 0 :
                writer.writerow(data)


def cpu_usage_analytics():
    # Get overall CPU usage and per-core CPU usage
    overall_cpu_usage = psutil.cpu_percent(percpu=False)
    per_core_cpu_usage = psutil.cpu_percent(percpu=True)

    # Prepare the data for the overall CPU usage
    data = {'Overall CPU Usage (%)': overall_cpu_usage}

    # Add per-core usage to the data (dynamically generate the keys for each core)
    for i, usage in enumerate(per_core_cpu_usage):
        data[f'Core {i+1} Usage (%)'] = usage

    # Define the CSV file name
    file_name = 'cpu_usage_analytics.csv'

    # Check if the file exists and is empty
    file_exists = os.path.isfile(file_name)
    file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

    # Open the CSV file in append mode ('a')
    with open(file_name, 'a', newline='') as csvfile:
        # Dynamically generate headers based on the number of cores
        fieldnames = ['Overall CPU Usage (%)'] + [f'Core {i+1} Usage (%)' for i in range(len(per_core_cpu_usage))]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is new or empty
        if not file_exists or file_is_empty:
            writer.writeheader()

        # Write the current CPU usage data as a row in the CSV
        writer.writerow(data)


def cpu_specs():
    # Get overall CPU frequency (combined) and per-core CPU frequency
    core_count = psutil.cpu_count(logical=False)  # Physical core count
    logical_core_count = psutil.cpu_count(logical=True)  # Logical core count (includes hyperthreading)
    overall_cpu_freq = psutil.cpu_freq(percpu=False)
    per_core_cpu_freq = psutil.cpu_freq(percpu=True)

    # Prepare the data for the overall CPU frequency
    data = {
        'Core Count': core_count,
        'Logical Core Count': logical_core_count,
        'CPU Current Freq (MHz)': overall_cpu_freq.current,
        'CPU Min Freq (MHz)': overall_cpu_freq.min,
        'CPU Max Freq (MHz)': overall_cpu_freq.max
    }

    # Add per-core frequency data (dynamically generate keys for each core)
    for i, freq in enumerate(per_core_cpu_freq):
        data[f'Core {i+1} Current Freq (MHz)'] = freq.current
        data[f'Core {i+1} Min Freq (MHz)'] = freq.min
        data[f'Core {i+1} Max Freq (MHz)'] = freq.max

    # Define the CSV file name
    file_name = 'cpu_specs.csv'

    # Check if the file exists and is empty
    file_exists = os.path.isfile(file_name)
    file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

    # Open the CSV file in append mode ('a')
    with open(file_name, 'a', newline='') as csvfile:
        # Dynamically generate headers based on the number of cores
        fieldnames = ['Core Count', 'Logical Core Count', 'CPU Current Freq (MHz)', 'CPU Min Freq (MHz)', 'CPU Max Freq (MHz)']
        temp_list = [(f'Core {i+1} Current Freq (MHz)', f'Core {i+1} Min Freq (MHz)', f'Core {i+1} Max Freq (MHz)') for i in range(len(per_core_cpu_freq))]
        temp_list_flattened = [i for j in temp_list for i in j]
        fieldnames += temp_list_flattened

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is new or empty
        if not file_exists or file_is_empty:
            writer.writeheader()

        # Write the current CPU frequencies as a row in the CSV
        writer.writerow(data)


def cpu_stats():
    # Get CPU stats (context switches, interrupts, etc.)
    stats = psutil.cpu_stats()

    # Prepare the data for the relevant fields
    data = {
        'Context Switches': stats.ctx_switches,
        'Interrupts': stats.interrupts,
        'Soft Interrupts': stats.soft_interrupts,
        'Syscalls': stats.syscalls
    }

    # Define the CSV file name
    file_name = 'cpu_stats.csv'

    # Check if the file exists and is empty
    file_exists = os.path.isfile(file_name)
    file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

    # Open the CSV file in append mode ('a')
    with open(file_name, 'a', newline='') as csvfile:
        # Define the headers for the CSV file
        fieldnames = ['Context Switches', 'Interrupts', 'Soft Interrupts', 'Syscalls']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is new or empty
        if not file_exists or file_is_empty:
            writer.writeheader()

        # Write the current CPU stats as a row in the CSV
        writer.writerow(data)


if __name__ == "__main__":
    refresh_rate = 1  # csv files data refresh rate
    cpu_specs()
    while True:
        cpu_times()
        cpu_times_per_core()
        cpu_times_percent()
        cpu_times_percent_per_core()
        cpu_usage_analytics()
        cpu_stats()
        sleep(refresh_rate)
