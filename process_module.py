import psutil
import subprocess
from time import sleep
import csv
import os
import stat

refresh_rate = 1  # seconds
csv_max_size = 100000000  # Bytes

class Process_Analytics_Module:
    def __init__(self):
        while True:
            self.get_current_processes_info()
            sleep(refresh_rate)

    def get_current_processes_info(self):
        file_name = "process_info.csv"
        file_exists = os.path.isfile(file_name)

        # Delete file if too big in size
        if (file_exists and os.stat(file_name).st_size >= csv_max_size):
            os.remove(file_name)
        
        # Writing process info into csv file
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


class Process_Interactive_Module:
    """ Creates, assigns work to and kills processes
    run_process() -> runs created process
    wait_for_process() -> waits until the complete execution of running process before flow of control moves further
    kill_process() -> kills the process it is called on immediately """
    
    worker_script_path = os.path.join(os.path.dirname(__file__), 'worker.py')
    worker_executable_path = ''
    extension = '.py'

    def __init__(self, task_string, ext, preemtable = False):
        try:
            self.preemptable = preemtable
            self.task_string = task_string
            if ext == '.c':
                self.worker_script_path = os.path.join(os.path.dirname(__file__), 'worker.c')
                self.worker_executable_path = os.path.join(os.path.dirname(__file__), 'worker')
                self.__create_worker()  # Create the worker script
                self.__compile_worker()  # Compile the C work script
                self.extension = '.c'

        except Exception as e:
            print(f"An error occurred: {e}")
    

    ### PRIVATE METHODS
    def __create_worker(self):
        # Write the work script to a temporary file
        with open(self.worker_script_path, 'w') as file:
            file.write(self.task_string)
        
        # Give permission to execute the created script file
        os.chmod(self.worker_script_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    def __compile_worker(self):
        # Compile the C code into an executable
        compile_command = ['gcc', self.worker_script_path, '-o', self.worker_executable_path]
        subprocess.run(compile_command, check=True)  # This will raise an error if the compilation fails

    # Function to create a new process
    def __create_process(self):
        if self.extension == '.py':
            # Create task to give process
            self.__create_worker()

            # Define the command to run as a separate process
            command = [self.worker_script_path]

        if self.extension == '.c':
            # Define the command to run the compiled work executable
            command = [self.worker_executable_path]
        
        # Create a subprocess
        process = subprocess.Popen(command)
        return process


    ### PUBLIC METHODS
    def run_process(self):
        self.process = self.__create_process()  # Create the process
        print(f"PROCESS PID: {self.process.pid} EXECUTION BEGUN.")

        if not self.preemptable:
            # Wait for the process to complete
            self.process.wait()
            print(f"PROCESS PID: {self.process.pid} EXECUTION COMPLETE.")

            # Terminate the process (optional since we are waiting)
            self.kill_process()

    def wait_for_process(self):
        self.process.wait()

    # User-defined method to kill the process prematurely
    def kill_process(self):
        try:
            self.process.terminate()  # Terminate the process
            self.process.wait()  # Wait for it to exit
            print(f"PROCESS PID: {self.process.pid} KILLED.")

        except psutil.NoSuchProcess:
            print("Process does not exist.")

        except Exception as e:
            print(f"Error killing the process: {e}")
        
        # Cleanup: Remove the work script file
        if os.path.exists(self.worker_script_path):
            os.remove(self.worker_script_path)

        if self.extension == '.c':
            # Cleanup: Remove the work executable
            if os.path.exists(self.worker_executable_path):
                os.remove(self.worker_executable_path)


if __name__ == '__main__':
    # Process_Analytics_Module()
    task_string = """#!/usr/bin/env python3
import time

def perform_work():
    for i in range(10):
        print(f"Worfing... {i + 1}")
        time.sleep(1)

if __name__ == "__main__":
    perform_work()
"""

    task_string2 = """#!/usr/bin/env python3
import math

def prime_gen(n = 1000):
    for i in range(2, n+1):
        for j in range(2, int(math.sqrt(i))+1):
            if i%j == 0:
                break
        else:
            print(i)        

if __name__ == "__main__":
    prime_gen()
"""
    task_string3 = r"""#include <stdio.h>
#include <unistd.h>

void perform_work() {
    for (int i = 0; i < 10; i++) {
        printf("Worling... %d\n", i + 1);
        sleep(1);  // Sleep for 1 second
    }
}

int main() {
    perform_work();
    return 0;
}
"""
    p = Process_Interactive_Module(task_string2, '.py', False)
    p.run_process()