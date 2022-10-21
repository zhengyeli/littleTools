from PyQt6 import QtGui
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QTextDocument, QPalette
from PyQt6.QtWidgets import QTextEdit, QMessageBox, QWidget, QGridLayout, QLabel, QPushButton, QPlainTextEdit

from module.iotLogAnalyzer.findStringAsk import Ui_search


class MTextEdit(QPlainTextEdit):
    signal_fileDragInput = pyqtSignal(str)
    signal_keyPressed = pyqtSignal(QtGui.QKeyEvent)

    def __init__(self, parent):
        super(MTextEdit, self).__init__()
        self.textEdit_findStr = None
        self.setReadOnly(False)

        self.findModeStep = 0
        self.isInFindMode = False

        self.input_file_dir = "None"
        self.findStringWidget = QWidget()
        self.findStringUi = Ui_search()
        self.findStringUi.setupUi(self.findStringWidget)
        self.findStringWidget.setVisible(False)

        self.findForward = QTextDocument.FindFlag.FindBackward
        self.bigOrLowSensitive = False

        self.findString_InputWindow_Init()

    def findString_InputWindow_Init(self):
        self.findStringUi.find.clicked.connect(self.findString)
        self.findStringUi.upOrLowBox.clicked.connect(self.findString_settings_changed)
        self.findStringUi.backForward.clicked.connect(self.findString_settings_changed)
        self.findStringUi.forward.clicked.connect(self.findString_settings_changed)

    def findStringInputWindowShow(self, b):
        self.findStringWidget.setVisible(b)

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent) -> None:
        if e.type() == QDragEnterEvent.Type.DragEnter:
            self.input_file_dir = e.mimeData().text().replace('file:///', '')
            self.signal_fileDragInput.emit(self.input_file_dir)
        else:
            return super().dragEnterEvent(e)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        self.signal_keyPressed.emit(e)
        if e.type() == QtGui.QKeyEvent.Type.KeyPress:
            # print(e.key())
            if e.key() == 16777249:  # ctrl
                self.findModeStep = 1
                return
            elif e.key() == 70:  # F
                if self.findModeStep == 1:
                    self.findModeStep = 2
                    self.isInFindMode = True
                    self.findStringInputWindowShow(True)
                    return
                else:
                    self.findModeStep = 0
            elif e.key() == 16777216:  # ESC
                self.findModeStep = 0
                self.isInFindMode = False
                self.findStringInputWindowShow(False)
                return

        super().keyPressEvent(e)

    def findNextString(self):
        string = self.findStringUi.lineEdit_findStr.text()
        if self.find(string, self.findForward):  # 查找后一个
            # 查找到后高亮显示
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Highlight,
                             palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight))
            self.setPalette(palette)
        else:
            QMessageBox.information(QWidget(), "注意", "没有找到内容")

    def findString(self):
        string = self.findStringUi.lineEdit_findStr.text()
        if len(string) == 0:
            return
        if self.find(string, QTextDocument.FindFlag.FindWholeWords):
            # 查找到后高亮显示
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Highlight,
                             palette.color(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight))
            self.setPalette(palette)
        else:
            QMessageBox.information(QWidget(), "注意", "没有找到内容")

    def findString_settings_changed(self):
        self.bigOrLowSensitive = self.findStringUi.upOrLowBox.isChecked()
        if self.findStringUi.backForward.isChecked():
            self.findForward = QTextDocument.FindFlag.FindBackward
        else:
            self.findForward = QTextDocument.FindFlag.FindBackward
