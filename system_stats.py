import psutil


def get_cpu_info():
    """Collect CPU utilization and core information."""

    cpu_usage = psutil.cpu_percent(interval=None, percpu=True)

    return {
        "usage": psutil.cpu_percent(interval=None),
        "per_core": cpu_usage,
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True)
    }


def get_memory_info():
    """Collect RAM utilization information."""

    memory = psutil.virtual_memory()

    return {
        "total": memory.total,
        "used": memory.used,
        "available": memory.available,
        "percent": memory.percent
    }


def get_disk_info(path="C:/"):
    """Collect disk utilization information."""

    disk = psutil.disk_usage(path)

    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent
    }


def bytes_to_gb(value):
    """Convert bytes into gigabytes."""

    return round(value / (1024 ** 3), 2)


def bytes_to_mb(value):
    """Convert bytes into megabytes."""

    return round(value / (1024 ** 2), 2)