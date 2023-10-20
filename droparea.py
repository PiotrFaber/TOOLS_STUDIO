# Copyright (C) 2023 Łebi

from pathlib import Path
from PySide6.QtWidgets import QLineEdit


class DropAreaDir(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)

    def dragEnterEvent(self, event):
        self.setStyleSheet("background-color: rgb(250, 170, 50)")
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            file_path = Path(file_path)
            if Path(file_path).is_dir():
                self.setText(str(file_path))
            else:
                event.ignore()
        else:
            event.ignore()
        self.setStyleSheet("background-color: rgb(250, 250, 250)")
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("background-color: rgb(250, 250, 250)")
        event.accept()


class DropAreaFile(QLineEdit,):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setAutoFillBackground(True)
        self.file_type = ""

    def getFileType(self, file_type):
        self.file_type = file_type

    def dragEnterEvent(self, event):
        self.setStyleSheet("background-color: rgb(250, 170, 50)")
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mime_data = event.mimeData()
        if mime_data.hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            file_path = Path(file_path)
            if Path(file_path).is_file():
                if self.file_type == str(file_path)[-4:]:
                    self.setText(str(file_path))
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()
        self.setStyleSheet("background-color: rgb(250, 250, 250)")
        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("background-color: rgb(250, 250, 250)")
        event.accept()
