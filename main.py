from PyQt6 import QtCore, QtGui, QtWidgets
from Ui_MainWindow import Ui_MainWindow
from MainWindow import MainWindow
from module.LowPowerBlueTooth import bleMainWin
from module.LowPowerBlueTooth.bleMainWin import BleMainWin

from module.SerialPort.Ui_frmComTool import Ui_frmComTool
from module.SerialPort.FrmComTool import FrmComTool
from module.iotLogAnalyzer.main import govee_mqtt_log
from module.photograph.graphDraw import BasicArrayPlot, dynamicArrayPlot


def module_init(handle):
    module_photoGraph_init(handle)
    module_serialports_init(handle)
    module_lowPowerBle_init(handle)
    module_logAnalyse_init(handle)

def module_logAnalyse_init(handle):
    govee_mqtt_log(handle)

# 串口
def module_serialports_init(handle):
    handle.ui.tabWidget.removeTab(0)
    module_serialports_addPort(handle)


def module_serialports_addPort(handle):
    widget = QtWidgets.QWidget()
    w = Ui_frmComTool()
    w.setupUi(widget)
    handle.comTool = FrmComTool(w, handle)
    handle.ui.tabWidget.addTab(widget, "comx")


def module_lowPowerBle_init(handle):
    handle.ble = BleMainWin(handle.ui.page2)


def module_photoGraph_init(handle):
    enable = False
    if enable:
        handle.plot = BasicArrayPlot(handle.ui.page3)
    else:
        handle.plot = dynamicArrayPlot(handle.ui.page3)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(Window)
    # ui的控件，setupUi后才生成，注意先后顺序！！！
    Main = MainWindow(ui)
    module_init(Main)
    Window.show()
    # 触发者.installEventFilter(处理者(QOject))
    # Window.installEventFilter(Main)
    sys.exit(app.exec())
