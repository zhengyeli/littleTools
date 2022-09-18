# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import image

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widgetTitle = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetTitle.sizePolicy().hasHeightForWidth())
        self.widgetTitle.setSizePolicy(sizePolicy)
        self.widgetTitle.setObjectName("widgetTitle")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widgetTitle)
        self.horizontalLayout_2.setContentsMargins(10, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widgetTop = QtWidgets.QWidget(self.widgetTitle)
        self.widgetTop.setObjectName("widgetTop")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widgetTop)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnMain = QtWidgets.QToolButton(self.widgetTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMain.sizePolicy().hasHeightForWidth())
        self.btnMain.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/main_main.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnMain.setIcon(icon)
        self.btnMain.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.btnMain.setObjectName("btnMain")
        self.horizontalLayout_3.addWidget(self.btnMain)
        self.btnConfig = QtWidgets.QToolButton(self.widgetTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnConfig.sizePolicy().hasHeightForWidth())
        self.btnConfig.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/image/main_config.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnConfig.setIcon(icon1)
        self.btnConfig.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.btnConfig.setObjectName("btnConfig")
        self.horizontalLayout_3.addWidget(self.btnConfig)
        self.btnData = QtWidgets.QToolButton(self.widgetTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnData.sizePolicy().hasHeightForWidth())
        self.btnData.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/image/main_data.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnData.setIcon(icon2)
        self.btnData.setChecked(False)
        self.btnData.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.btnData.setObjectName("btnData")
        self.horizontalLayout_3.addWidget(self.btnData)
        self.btnHelp = QtWidgets.QToolButton(self.widgetTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnHelp.sizePolicy().hasHeightForWidth())
        self.btnHelp.setSizePolicy(sizePolicy)
        self.btnHelp.setStyleSheet("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/image/main_person.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnHelp.setIcon(icon3)
        self.btnHelp.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.btnHelp.setObjectName("btnHelp")
        self.horizontalLayout_3.addWidget(self.btnHelp)
        self.btnExit = QtWidgets.QToolButton(self.widgetTop)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnExit.sizePolicy().hasHeightForWidth())
        self.btnExit.setSizePolicy(sizePolicy)
        self.btnExit.setStyleSheet("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/image/main_exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.btnExit.setIcon(icon4)
        self.btnExit.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.btnExit.setObjectName("btnExit")
        self.horizontalLayout_3.addWidget(self.btnExit)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2.addWidget(self.widgetTop)
        self.verticalLayout.addWidget(self.widgetTitle)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page1 = QtWidgets.QWidget()
        self.page1.setObjectName("page1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.page1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.page1)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.tabWidget.setFont(font)
        self.tabWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.TextElideMode.ElideNone)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.Home = QtWidgets.QWidget()
        self.Home.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Home.sizePolicy().hasHeightForWidth())
        self.Home.setSizePolicy(sizePolicy)
        self.Home.setMaximumSize(QtCore.QSize(714, 16777215))
        self.Home.setObjectName("Home")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Home)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabWidget.addTab(self.Home, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.stackedWidget.addWidget(self.page1)
        self.page2 = QtWidgets.QWidget()
        self.page2.setObjectName("page2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.page2)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widgetLeftConfig = QtWidgets.QWidget(self.page2)
        self.widgetLeftConfig.setMaximumSize(QtCore.QSize(130, 16777215))
        self.widgetLeftConfig.setObjectName("widgetLeftConfig")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widgetLeftConfig)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tbtnConfig1 = QtWidgets.QToolButton(self.widgetLeftConfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbtnConfig1.sizePolicy().hasHeightForWidth())
        self.tbtnConfig1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setKerning(True)
        self.tbtnConfig1.setFont(font)
        self.tbtnConfig1.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tbtnConfig1.setObjectName("tbtnConfig1")
        self.verticalLayout_3.addWidget(self.tbtnConfig1)
        self.tbtnConfig2 = QtWidgets.QToolButton(self.widgetLeftConfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbtnConfig2.sizePolicy().hasHeightForWidth())
        self.tbtnConfig2.setSizePolicy(sizePolicy)
        self.tbtnConfig2.setObjectName("tbtnConfig2")
        self.verticalLayout_3.addWidget(self.tbtnConfig2)
        self.tbtnConfig3 = QtWidgets.QToolButton(self.widgetLeftConfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbtnConfig3.sizePolicy().hasHeightForWidth())
        self.tbtnConfig3.setSizePolicy(sizePolicy)
        self.tbtnConfig3.setObjectName("tbtnConfig3")
        self.verticalLayout_3.addWidget(self.tbtnConfig3)
        self.tbtnConfig4 = QtWidgets.QToolButton(self.widgetLeftConfig)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tbtnConfig4.sizePolicy().hasHeightForWidth())
        self.tbtnConfig4.setSizePolicy(sizePolicy)
        self.tbtnConfig4.setObjectName("tbtnConfig4")
        self.verticalLayout_3.addWidget(self.tbtnConfig4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 417, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.horizontalLayout_4.addWidget(self.widgetLeftConfig)
        self.tetoutput = QtWidgets.QTextEdit(self.page2)
        font = QtGui.QFont()
        font.setBold(True)
        self.tetoutput.setFont(font)
        self.tetoutput.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.tetoutput.setLineWidth(0)
        self.tetoutput.setReadOnly(True)
        self.tetoutput.setObjectName("tetoutput")
        self.horizontalLayout_4.addWidget(self.tetoutput)
        self.stackedWidget_2 = QtWidgets.QStackedWidget(self.page2)
        self.stackedWidget_2.setObjectName("stackedWidget_2")
        self.horizontalLayout_4.addWidget(self.stackedWidget_2)
        self.stackedWidget.addWidget(self.page2)
        self.page3 = QtWidgets.QWidget()
        self.page3.setObjectName("page3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lab3 = QtWidgets.QLabel(self.page3)
        self.lab3.setObjectName("lab3")
        self.verticalLayout_5.addWidget(self.lab3)
        self.stackedWidget.addWidget(self.page3)
        self.page4 = QtWidgets.QWidget()
        self.page4.setObjectName("page4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lab4 = QtWidgets.QLabel(self.page4)
        self.lab4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lab4.setObjectName("lab4")
        self.verticalLayout_4.addWidget(self.lab4)
        self.stackedWidget.addWidget(self.page4)
        self.verticalLayout.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnMain.setText(_translate("MainWindow", "串口调试"))
        self.btnConfig.setText(_translate("MainWindow", "蓝牙调试"))
        self.btnData.setText(_translate("MainWindow", "警情查询"))
        self.btnHelp.setText(_translate("MainWindow", "调试帮助"))
        self.btnExit.setText(_translate("MainWindow", "用户退出"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Home), _translate("MainWindow", "Home"))
        self.tbtnConfig1.setText(_translate("MainWindow", "保存窗口设置"))
        self.tbtnConfig2.setText(_translate("MainWindow", "恢复窗口设置"))
        self.tbtnConfig3.setText(_translate("MainWindow", "恢复默认设置"))
        self.tbtnConfig4.setText(_translate("MainWindow", "调试信息另存"))
        self.lab3.setText(_translate("MainWindow", "TextLabel"))
        self.lab4.setText(_translate("MainWindow", "调试帮助"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
