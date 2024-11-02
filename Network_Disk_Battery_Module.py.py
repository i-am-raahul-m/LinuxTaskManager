import psutil
import csv
from datetime import datetime
import os

# Class for Network Monitoring
class NetworkMonitor:
    @staticmethod
    def get_network_info():
        network_info = {
            "Network I/O": {
                "Bytes Sent": psutil.net_io_counters().bytes_sent,
                "Bytes Received": psutil.net_io_counters().bytes_recv,
                "Packets Sent": psutil.net_io_counters().packets_sent,
                "Packets Received": psutil.net_io_counters().packets_recv
            },
            "Interfaces": {}
        }

        interfaces = psutil.net_if_stats()
        addresses = psutil.net_if_addrs()

        for interface, stats in interfaces.items():
            network_info["Interfaces"][interface] = {
                "Status": "UP" if stats.isup else "DOWN",
                "Speed (Mbps)": stats.speed,
                "MTU": stats.mtu,
                "Addresses": []
            }
            if interface in addresses:
                for addr in addresses[interface]:
                    address_info = {
                        "Family": str(addr.family),
                        "Address": addr.address,
                        "Broadcast": addr.broadcast if addr.broadcast else None,
                        "Netmask": addr.netmask if addr.netmask else None
                    }
                    network_info["Interfaces"][interface]["Addresses"].append(address_info)

        return network_info


# Class for Disk Monitoring
class DiskMonitor:
    @staticmethod
    def get_disk_info():
        disk_info = {
            "Disk Usage": [],
            "Disk I/O": []
        }

        # Disk usage information
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info["Disk Usage"].append({
                    "Partition": partition.device,
                    "Mountpoint": partition.mountpoint,
                    "File System Type": partition.fstype,
                    "Total Space (GB)": usage.total / (1024 ** 3),
                    "Used Space (GB)": usage.used / (1024 ** 3),
                    "Free Space (GB)": usage.free / (1024 ** 3),
                    "Percentage Used (%)": usage.percent
                })
            except PermissionError:
                continue

        # Disk I/O information
        io_counters = psutil.disk_io_counters(perdisk=True)
        for disk, io in io_counters.items():
            disk_info["Disk I/O"].append({
                "Disk": disk,
                "Read Count": io.read_count,
                "Write Count": io.write_count,
                "Bytes Read": io.read_bytes,
                "Bytes Written": io.write_bytes,
                "Read Time (ms)": io.read_time,
                "Write Time (ms)": io.write_time
            })

        return disk_info


# Class for Battery Monitoring
class BatteryMonitor:
    @staticmethod
    def get_battery_info():
        battery = psutil.sensors_battery()
        return {
            "Percentage": battery.percent,
            "Plugged In": battery.power_plugged,
            "Time Left (minutes)": battery.secsleft // 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Charging"
        }


# Save results to CSV files
def save_network_info_to_csv(network_info):
    filename = 'network_monitor.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Network I/O Statistics"])
        writer.writerow(["Bytes Sent", "Bytes Received", "Packets Sent", "Packets Received"])
        writer.writerow([
            network_info["Network I/O"]["Bytes Sent"],
            network_info["Network I/O"]["Bytes Received"],
            network_info["Network I/O"]["Packets Sent"],
            network_info["Network I/O"]["Packets Received"]
        ])

        writer.writerow([])
        writer.writerow(["Network Interfaces"])
        for interface, details in network_info["Interfaces"].items():
            writer.writerow([f"Interface: {interface}"])
            writer.writerow(["Status", "Speed (Mbps)", "MTU"])
            writer.writerow([details["Status"], details["Speed (Mbps)"], details["MTU"]])
            writer.writerow(["Addresses:"])
            for addr in details["Addresses"]:
                writer.writerow([addr["Family"], addr["Address"], addr.get("Broadcast", ""), addr.get("Netmask", "")])

    print(f"Network monitor data has been saved to {filename}")


def save_disk_info_to_csv(disk_info):
    filename = 'disk_monitor.csv'
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Disk Usage - Partition', 'Mountpoint', 'File System Type', 'Total Space (GB)',
                         'Used Space (GB)', 'Free Space (GB)', 'Percentage Used (%)'])
        for usage in disk_info["Disk Usage"]:
            writer.writerow([usage['Partition'], usage['Mountpoint'], usage['File System Type'],
                             f"{usage['Total Space (GB)']:.2f}", f"{usage['Used Space (GB)']:.2f}",
                             f"{usage['Free Space (GB)']:.2f}", usage['Percentage Used (%)']])

        writer.writerow([])

        writer.writerow(['Disk I/O - Disk', 'Read Count', 'Write Count', 'Bytes Read', 'Bytes Written',
                         'Read Time (ms)', 'Write Time (ms)'])
        for io in disk_info["Disk I/O"]:
            writer.writerow([io['Disk'], io['Read Count'], io['Write Count'], io['Bytes Read'],
                             io['Bytes Written'], io['Read Time (ms)'], io['Write Time (ms)']])

    print(f"Disk monitor data has been saved to {filename}")


def save_battery_info_to_csv(battery_info):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"battery_monitor_{current_time}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Battery Monitor Information"])
        writer.writerow(["Percentage (%)", "Plugged In", "Time Left (minutes)"])
        writer.writerow([battery_info["Percentage"], battery_info["Plugged In"], battery_info["Time Left (minutes)"]])

    print(f"Battery monitor data has been written to {filename}")


if __name__ == "__main__":
    network_info = NetworkMonitor.get_network_info()
    save_network_info_to_csv(network_info)

    disk_info = DiskMonitor.get_disk_info()
    save_disk_info_to_csv(disk_info)

    battery_info = BatteryMonitor.get_battery_info()
    save_battery_info_to_csv(battery_info)
