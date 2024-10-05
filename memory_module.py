import psutil
import csv
import os
from time import sleep

def get_memory_analytics():
    memory_stats = psutil.virtual_memory()

    # Prepare data for CSV
    data = {
        'total_memory(B)': memory_stats.total,
        'available_memory(B)': memory_stats.available,
        'used_memory(B)': memory_stats.used,
        'free_memory(B)': memory_stats.free,
        'percent_used(%)': memory_stats.percent,
        'active_memory(B)': memory_stats.active,  # Active memory
        'inactive_memory(B)': memory_stats.inactive,  # Inactive memory
        'buffers(B)': memory_stats.buffers,  # Buffers
        'cached(B)': memory_stats.cached,  # Cached
        'shared_memory(B)': memory_stats.shared,  # Shared memory
        'slab(B)': memory_stats.slab  # Slab
    }

    # Write data to CSV
    file_name = 'memory_analytics.csv'

    # Cheking if file exists or if the file is empty
    file_exists = os.path.isfile(file_name)
    file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        
        # Write header if file is new
        if not file_exists or file_is_empty:
            writer.writeheader()
        
        # Write the memory stats
        writer.writerow(data)


def get_swap_memory_details():
    # Get swap memory stats
    swap_stats = psutil.swap_memory()

    # Prepare data for CSV
    data = {
        'total_swap(B)': swap_stats.total,
        'used_swap(B)': swap_stats.used,
        'free_swap(B)': swap_stats.free,
        'percent_used(%)': swap_stats.percent,
        'swap_in(B)': swap_stats.sin,  # Cumulative swap in
        'swap_out(B)': swap_stats.sout  # Cumulative swap out
    }

    # Write data to CSV
    file_name = 'swap_memory_analytics.csv'

    # Cheking if file exists or if the file is empty
    file_exists = os.path.isfile(file_name)
    file_is_empty = os.stat(file_name).st_size == 0 if file_exists else True

    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())

        # Write header if file is new
        if not file_exists or file_is_empty:
            writer.writeheader()

        # Write the swap memory stats
        writer.writerow(data)


if __name__ == '__main__':
    refresh_rate = 1
    while True:
        get_memory_analytics()
        get_swap_memory_details()
        sleep(refresh_rate)
