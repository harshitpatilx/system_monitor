# System Monitor

A lightweight, real-time desktop system monitoring application built with Python, PySide6 and psutil.

System Monitor provides a simple interface to monitor hardware resource utilization and inspect running processes on a Windows computer.

## Features

### System Overview
- Real-time CPU utilization monitoring.
- Individual CPU core utilization.
- Physical and logical CPU core information.
- RAM usage monitoring.
- Disk space and utilization monitoring.

### Process Manager
- Displays currently running processes.
- Shows process IDs (PID).
- Displays individual process CPU utilization.
- Displays process memory consumption.
- Shows process status.
- Search processes by name.
- Automatic sorting by CPU utilization.

### Interface
- Desktop GUI built with PySide6.
- Separate Overview and Processes tabs.
- Automatically refreshed system statistics.
- Periodic process information updates.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| PySide6 | Desktop graphical interface |
| psutil | System and process monitoring |

## Project Structure

```text
system-monitor/
│
├── main.py
├── window.py
├── system_stats.py
├── process_monitor.py
├── requirements.txt
│
└── assets/
```

## Requirements

- Python 3.10 or newer
- Windows 10/11
- pip

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/system-monitor.git
```

Navigate to the project directory:

```bash
cd system-monitor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

The application opens with two main sections:

- **Overview:** Displays CPU, RAM and disk statistics.
- **Processes:** Displays running processes and their resource consumption.

## Dependencies

- [psutil](https://github.com/giampaolo/psutil)
- [PySide6](https://doc.qt.io/qtforpython-6/)

## Project Status

Currently under development.

This project is being developed as a personal Python programming project, with an emphasis on system monitoring, process management and desktop application development.

## License

MIT License.