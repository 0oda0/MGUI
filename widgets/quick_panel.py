# widgets/quick_panel.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from widgets.top_processes_widget import TopProcessesWidget
from widgets.pinned_apps_widget import PinnedAppsWidget

class QuickPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(280)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Блок топ-процессов
        processes_frame = QFrame()
        processes_frame.setFrameShape(QFrame.Shape.StyledPanel)
        processes_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        proc_layout = QVBoxLayout(processes_frame)
        proc_label = QLabel("⚡ Топ-5 процессов по CPU")
        proc_label.setStyleSheet("font-weight: bold; padding: 5px;")
        self.top_proc = TopProcessesWidget(compact=True)
        proc_layout.addWidget(proc_label)
        proc_layout.addWidget(self.top_proc)
        layout.addWidget(processes_frame)

        # Блок закреплённых программ
        pinned_frame = QFrame()
        pinned_frame.setFrameShape(QFrame.Shape.StyledPanel)
        pinned_frame.setStyleSheet("background-color: #2d2d2d; border-radius: 8px;")
        pinned_layout = QVBoxLayout(pinned_frame)
        pinned_label = QLabel("📌 Закреплённые программы")
        pinned_label.setStyleSheet("font-weight: bold; padding: 5px;")
        self.pinned = PinnedAppsWidget()
        pinned_layout.addWidget(pinned_label)
        pinned_layout.addWidget(self.pinned)
        layout.addWidget(pinned_frame)

        layout.addStretch()