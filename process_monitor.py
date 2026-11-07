import psutil

from system_stats import bytes_to_mb


def get_processes(sort_by="cpu"):
    """Collect information about currently running processes."""

    process_list = []

    for process in psutil.process_iter():

        try:
            cpu = process.cpu_percent(interval=None)
            memory = process.memory_info()

            process_data = {
                "pid": process.pid,
                "name": process.name(),
                "cpu": cpu,
                "memory": bytes_to_mb(memory.rss),
                "status": process.status()
            }

            process_list.append(process_data)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if sort_by == "cpu":
        process_list.sort(
            key=lambda p: p["cpu"],
            reverse=True
        )

    elif sort_by == "memory":
        process_list.sort(
            key=lambda p: p["memory"],
            reverse=True
        )

    return process_list