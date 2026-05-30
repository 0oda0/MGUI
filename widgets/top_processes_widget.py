# widgets/top_processes_widget.py (обновлённый)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtCore import QTimer, Qt
import psutil

class TopProcessesWidget(QWidget):
    def __init__(self, compact=False):
        super().__init__()
        self.compact = compact
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_processes)
        self.timer.start(2000)
        self.refresh_processes()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        if self.compact:
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["Процесс", "CPU"])
        else:
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Процесс", "CPU (%)", "Память (MB)"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.itemDoubleClicked.connect(self.kill_process)

        layout.addWidget(self.table)

        if not self.compact:
            refresh_btn = QPushButton("Обновить сейчас")
            refresh_btn.clicked.connect(self.refresh_processes)
            layout.addWidget(refresh_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def refresh_processes(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                cpu = proc.info['cpu_percent'] or 0
                mem = (proc.info['memory_info'].rss / (1024 * 1024)) if proc.info['memory_info'] else 0
                processes.append({
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'cpu': cpu,
                    'mem': mem
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(key=lambda x: x['cpu'], reverse=True)
        top5 = processes[:5]

        self.table.setRowCount(len(top5))
        for row, proc in enumerate(top5):
            name_item = QTableWidgetItem(f"{proc['name']} ({proc['pid']})")
            cpu_item = QTableWidgetItem(f"{proc['cpu']:.1f}%")
            name_item.setData(Qt.ItemDataRole.UserRole, proc['pid'])

            if self.compact:
                self.table.setItem(row, 0, name_item)
                self.table.setItem(row, 1, cpu_item)
            else:
                mem_item = QTableWidgetItem(f"{proc['mem']:.1f} MB")
                self.table.setItem(row, 0, name_item)
                self.table.setItem(row, 1, cpu_item)
                self.table.setItem(row, 2, mem_item)

    def kill_process(self, item):
        pid = item.data(Qt.ItemDataRole.UserRole)
        if pid:
            reply = QMessageBox.question(self, "Завершить процесс",
                                         f"Завершить процесс PID {pid}?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    proc = psutil.Process(pid)
                    proc.terminate()
                    QMessageBox.information(self, "Успех", f"Процесс {pid} завершён")
                    self.refresh_processes()
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", str(e))