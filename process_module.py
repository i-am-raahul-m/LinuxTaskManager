import psutil
from time import sleep
import csv
import os


def get_current_processes_info():
    file_name = "process_info.csv"
    
    with open(file_name, 'w', newline='') as file:
        file_is_empty = os.stat(file_name).st_size == 0

        fieldnames = ['pid', 'name', 'exe', 'status', 'nice', 'ppid', 'cpu_affinity', 'cpu_num', 'cpu_percent', 
                      'num_ctx_switches', 'num_fds', 'threads', 'num_threads', 'io_counters', 'memory_full_info', 
                      'memory_percent', 'cwd']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file_is_empty:
                writer.writeheader()

        for proc in psutil.process_iter(fieldnames):
            proc_info = proc.info  # Dictionary with key-value pairs of process info

            #[voluntary_ctx_switches, involuntary_ctx_switches]
            proc_info['num_ctx_switches'] = list(proc_info['num_ctx_switches'])

            #[pthread1[id, user_time, system_time], pthread2[id, user_time, system_time], ...] 
            proc_info['threads'] = [list(i) for i in list(proc_info['threads'])]

            #[read_count, write_count, read_bytes, write_bytes, read_chars, write_chars]
            proc_info['io_counters'] = list(proc_info['io_counters'])

            #[rss, vms, shared, text, lib, data, dirty, uss, ps, swap]
            proc_info['memory_full_info'] = list(proc_info['memory_full_info'])
            writer.writerow(proc.info)


if __name__ == '__main__':
    refresh_rate = 1
    while True:
        get_current_processes_info()
        sleep(refresh_rate)