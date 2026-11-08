from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QProgressBar,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit,
    QHeaderView
)

from PySide6.QtCore import QTimer

from system_stats import *


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Monitor")
        self.setMinimumSize(700, 500)

        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(1000)
        self.process_timer = QTimer(self)

        self.process_timer.timeout.connect(
            self.update_processes
        )

        self.process_timer.start(2000)

        self.update_processes()

    def init_ui(self):

        root_layout = QVBoxLayout(self)

        self.tabs = QTabWidget()

        overview_tab = QWidget()
        main_layout = QVBoxLayout(overview_tab)

        # CPU Section
        cpu_group = QGroupBox("CPU")
        cpu_layout = QVBoxLayout()

        self.cpu_label = QLabel("CPU Usage: 0%")
        self.cpu_bar = QProgressBar()

        cpu_layout.addWidget(self.cpu_label)
        cpu_layout.addWidget(self.cpu_bar)

        # Individual CPU Cores
        self.core_layout = QGridLayout()

        self.core_bars = []
        self.core_labels = []

        logical_cores = get_cpu_info()["logical_cores"]

        for i in range(logical_cores):

            label = QLabel(f"Core {i + 1}")
            bar = QProgressBar()

            self.core_labels.append(label)
            self.core_bars.append(bar)

            row = i // 4
            column = (i % 4) * 2

            self.core_layout.addWidget(label, row, column)
            self.core_layout.addWidget(bar, row, column + 1)

        core_group = QGroupBox("Individual CPU Cores")
        core_group.setLayout(self.core_layout)

        cpu_layout.addWidget(core_group)

        cpu_group.setLayout(cpu_layout)

        # RAM Section
        ram_group = QGroupBox("Memory")
        ram_layout = QVBoxLayout()

        self.ram_label = QLabel("RAM Usage: 0%")
        self.ram_bar = QProgressBar()

        ram_layout.addWidget(self.ram_label)
        ram_layout.addWidget(self.ram_bar)

        ram_group.setLayout(ram_layout)

        # Disk Section
        disk_group = QGroupBox("Disk")
        disk_layout = QVBoxLayout()

        self.disk_label = QLabel("Disk Usage: 0%")
        self.disk_bar = QProgressBar()

        disk_layout.addWidget(self.disk_label)
        disk_layout.addWidget(self.disk_bar)

        disk_group.setLayout(disk_layout)

        # Main Layout
        main_layout.addWidget(cpu_group)
        main_layout.addWidget(ram_group)
        main_layout.addWidget(disk_group)

        # Process Manager Tab

        process_tab = QWidget()
        process_layout = QVBoxLayout(process_tab)

        self.process_search = QLineEdit()
        self.process_search.setPlaceholderText("Search processes...")

        self.process_table = QTableWidget()

        self.process_table.setColumnCount(5)

        self.process_table.setHorizontalHeaderLabels([
            "PID",
            "Process",
            "CPU (%)",
            "Memory (MB)",
            "Status"
        ])

        self.process_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.process_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.process_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.process_search.textChanged.connect(
            self.filter_processes
        )

        process_layout.addWidget(self.process_search)
        process_layout.addWidget(self.process_table)

        self.tabs.addTab(overview_tab, "Overview")
        self.tabs.addTab(process_tab, "Processes")

        root_layout.addWidget(self.tabs)

    def update_stats(self):

        # CPU
        cpu = get_cpu_info()

        self.cpu_label.setText(
            f"CPU Usage: {cpu['usage']:.2f}%"
        )

        self.cpu_bar.setValue(int(cpu["usage"]))

        for i, usage in enumerate(cpu["per_core"]):

            self.core_labels[i].setText(f"Core {i + 1}")
            self.core_bars[i].setValue(int(usage))

        # RAM
        ram = get_memory_info()

        self.ram_label.setText(
            f"RAM: {bytes_to_gb(ram['used'])} GB / "
            f"{bytes_to_gb(ram['total'])} GB "
            f"({ram['percent']}%)"
        )

        self.ram_bar.setValue(int(ram["percent"]))

        # Disk
        disk = get_disk_info()

        self.disk_label.setText(
            f"Disk: {bytes_to_gb(disk['used'])} GB / "
            f"{bytes_to_gb(disk['total'])} GB "
            f"({disk['percent']}%)"
        )

        self.disk_bar.setValue(int(disk["percent"]))

    def update_processes(self):

        from process_monitor import get_processes

        processes = get_processes(sort_by="cpu")

        self.process_table.setRowCount(len(processes))

        for row, process in enumerate(processes):

            values = [
                str(process["pid"]),
                process["name"],
                f'{process["cpu"]:.2f}',
                f'{process["memory"]:.2f}',
                process["status"]
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(value)

                self.process_table.setItem(
                    row,
                    column,
                    item
                )

        self.filter_processes(self.process_search.text())
    
    
    def filter_processes(self, text):

        text = text.lower()

        for row in range(self.process_table.rowCount()):

            item = self.process_table.item(row, 1)

            if item is None:
                continue

            process_name = item.text().lower()

            self.process_table.setRowHidden(
                row,
                text not in process_name
            )