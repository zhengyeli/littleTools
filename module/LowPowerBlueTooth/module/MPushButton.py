from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QToolButton, QInputDialog, QLineEdit, QMessageBox, QPushButton


class MPushButton(QPushButton):
    signal_longPress = pyqtSignal(int)

    def __init__(self, widget):
        super().__init__(widget)
        self.cmd = None
        self.motherWidget = widget

        self.t_PressTimer = QTimer()
        self.i_PressCount = 0
        self.b_longpress = False
        self.prevButton = None
        self.nextButton = None

        self.FatherButton = super()
        self.FatherButton.pressed.connect(self.longpressed)
        self.FatherButton.released.connect(self.longreleased)
        # self.FatherButton.clicked.connect(self.clicked)

    def longpressed(self):
        self.t_PressTimer.start(20)

    def longreleased(self):
        self.t_PressTimer.stop()
        if 500 < self.i_PressCount < 1000:
            self.signal_longPress.emit(500)
            text = QInputDialog.getText(self.motherWidget, "我只是打酱油的~", "input button name", QLineEdit.EchoMode.Normal)
            if text[1]:
                buttonName = text[0] # 获取输入
                self.FatherButton.setText(buttonName)
            else:
                return

        elif 1000 <= self.i_PressCount < 2000:
            self.signal_longPress.emit(1000)
            text = QInputDialog.getText(self.motherWidget, "我只是打酱油的~", "input CMD + DATA (BB0101)", QLineEdit.EchoMode.Normal)
            if text[1]:
                cmd = text[0]  # 获取输入
                self.cmd = cmd
        elif 2000 <= self.i_PressCount:
            # NOT WORK NOW
            ans = QMessageBox.question(self.motherWidget, "tip", "delete button ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                   QMessageBox.StandardButton.Yes)
            if ans == QMessageBox.StandardButton.Yes:
                pass
            elif ans == QMessageBox.StandardButton.No:
                pass
            self.i_PressCount = 1  # clear
            
    def countPressMs(self):
        self.i_PressCount += 20
        
    # def clicked(self, checked: bool = ...) -> None:
    #     return super(MPushButton, self).clicked()
