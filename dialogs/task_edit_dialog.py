# dialogs/task_edit_dialog.py
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                             QCheckBox, QDialogButtonBox, QLabel)

class TaskEditDialog(QDialog):
    def __init__(self, title="", important=False, urgent=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Задача")
        self.setModal(True)

        layout = QVBoxLayout(self)

        form = QFormLayout()
        self.title_edit = QLineEdit()
        self.title_edit.setText(title)
        form.addRow("Название:", self.title_edit)

        self.important_cb = QCheckBox()
        self.important_cb.setChecked(important)
        form.addRow("Важная:", self.important_cb)

        self.urgent_cb = QCheckBox()
        self.urgent_cb.setChecked(urgent)
        form.addRow("Срочная:", self.urgent_cb)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "title": self.title_edit.text(),
            "important": self.important_cb.isChecked(),
            "urgent": self.urgent_cb.isChecked()
        }