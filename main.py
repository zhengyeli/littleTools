from PyQt6 import QtCore, QtGui, QtWidgets
from Ui_MainWindow import Ui_MainWindow
from MainWindow import MainWindow

from module.SerialPort.Ui_frmComTool import Ui_frmComTool
from module.SerialPort.FrmComTool import FrmComTool

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Window)
    # ui的控件，setupUi后才生成，注意先后顺序！！！
    Main = MainWindow(ui)
    Window.show()
    # 触发者.installEventFilter(处理者(QOject))
    # Window.installEventFilter(Main)
    sys.exit(app.exec())
