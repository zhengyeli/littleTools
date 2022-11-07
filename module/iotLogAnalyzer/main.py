from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtWidgets import QDockWidget, QWidget, QMainWindow

from module.iotLogAnalyzer import mqtt_split as log_prase
from module.iotLogAnalyzer.MTextEdit import MTextEdit


def Log_Prase_Handle():
    C = log_prase.Mqtt_Prase()
    C.run_prase()


class govee_mqtt_log:
    def __init__(self, handle):
        self.out_edit = None
        self.out_dock = None
        self.in_edit = None
        self.in_dock = None
        if handle is not None:
            self.mainPtr = handle
            self.page4 = self.mainPtr.ui.page4
        else:
            self.page4 = QWidget()

        if self.page4 is None:
            self.MainWindow = QMainWindow()
        else:
            if type(self.page4) == QMainWindow:
                self.MainWindow = self.page4
            else:
                self.MainWindow = QMainWindow()
                self.page4.layout().addWidget(self.MainWindow)

        self.MainWindow.setDockNestingEnabled(True)
        self.MainWindow.setStatusBar(None)
        self.MainWindow.setMenuBar(None)

        self.C = log_prase.Mqtt_Prase()
        self.C.run_prase()
        self.C.utils.__del__()

        self.form_init()

    def form_init(self):
        self.in_dock = QDockWidget()
        self.in_edit = MTextEdit()
        self.in_dock.setWidget(self.in_edit)
        self.MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.in_dock)
        # 为什么不能直接使用 self.in_edit.signal_fileDragInput.connect(self.file_input)
        self.in_edit.signal_fileDragInput.connect(lambda fileDir: self.file_input(fileDir))

        self.out_dock = QDockWidget()
        self.out_edit = MTextEdit()
        self.out_dock.setWidget(self.out_edit)
        self.MainWindow.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.out_dock)

    def file_input(self, file_dir):
        self.C.prase_custom_file_set(file_dir)
        self.C.run_prase()
        self.C.utils.__del__()

        self.out_edit.clear()
        self.in_edit.clear()

        file = QFile(self.C.utils.in_file_dir)
        file.open(QFile.OpenModeFlag.ReadOnly)
        steam = QTextStream(file)
        log = steam.readAll()
        file.close()
        self.in_edit.insertPlainText(log)
        self.in_dock.setWindowTitle(self.C.utils.in_file_dir)

        file = QFile(self.C.utils.out_file_dir)
        file.open(QFile.OpenModeFlag.ReadOnly)
        steam = QTextStream(file)
        log = steam.readAll()
        file.close()
        self.out_edit.insertPlainText(log)
        self.out_dock.setWindowTitle(self.C.utils.out_file_dir)


if __name__ == '__main__':
    Log_Prase_Handle()
