"""helpers/sys.py — System Performance Information Utility Functions"""
from datetime import datetime

import psutil


def _get_size(bytes, suffix='B'):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < factor:
            return f'{bytes:.2f}{unit}{suffix}'
        bytes /= factor


# @log("Boot Time: {boot_time}")
def log_system_boot_time() -> str:
    """Log System Boot Time"""
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    return f'{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}'


# @log("CPU: {cpu_usage}% utilized of {physical_cores} physical CPU cores ({total_cores} total.")
def log_system_cpu_usage() -> dict:
    """Log System CPU Usage"""
    return {
        'cpu_usage': psutil.cpu_percent(),
        'physical_cores': psutil.cpu_count(logical=False),
        'total_cores': psutil.cpu_count(logical=True),
    }


def log_system_virtual_mem_usage() -> dict:
    """Log System Virtual Mem Usage"""
    virtual_memory = psutil.virtual_memory()
    return {
        'virtual_memory': virtual_memory,
        'total_mem': _get_size(virtual_memory.total),
        'available_mem': _get_size(virtual_memory.available),
        'used_mem': _get_size(virtual_memory.used),
        'pct_mem': virtual_memory.percent,
    }


# @log('Disk: {pct_disk}% used of {total_disk} total, with {free_disk} remaining.')
def log_system_disk_usage() -> dict:
    """Log System Disk Usage"""
    partition = psutil.disk_partitions()[0]
    partition_usage = psutil.disk_usage(partition.mountpoint)
    return {
        'partition': partition,
        'partition_usage': partition_usage,
        'total_disk': _get_size(partition_usage.total),
        'free_disk': _get_size(partition_usage.free),
        'pct_disk': partition_usage.percent,
    }
