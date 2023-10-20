# Copyright (C) 2023 Łebi

import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from tools_studio import ToolsStudio

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = "ToolsStudio.ver1"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, "icons", "python_icon.ico")))
    window = ToolsStudio()
    window.show()
    sys.exit(app.exec())
