# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RDM_DMX_Master.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QTabWidget,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(451, 530)
        self.actionDMX = QAction(MainWindow)
        self.actionDMX.setObjectName(u"actionDMX")
        self.actionRDM = QAction(MainWindow)
        self.actionRDM.setObjectName(u"actionRDM")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 20, 451, 491))
        self.RDM_tab = QWidget()
        self.RDM_tab.setObjectName(u"RDM_tab")
        self.label_9 = QLabel(self.RDM_tab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(170, 340, 109, 18))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_3 = QLabel(self.RDM_tab)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(40, 80, 61, 20))
        self.label_3.setFont(font)
        self.label_2 = QLabel(self.RDM_tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(270, 60, 61, 16))
        self.label_10 = QLabel(self.RDM_tab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(180, 120, 16, 16))
        self.label_4 = QLabel(self.RDM_tab)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(150, 10, 141, 41))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        self.label_4.setFont(font1)
        self.label_11 = QLabel(self.RDM_tab)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(180, 160, 16, 16))
        self.source_UID = QLineEdit(self.RDM_tab)
        self.source_UID.setObjectName(u"source_UID")
        self.source_UID.setGeometry(QRect(200, 160, 211, 21))
        self.source_UID.setFrame(True)
        self.slave_Response = QLabel(self.RDM_tab)
        self.slave_Response.setObjectName(u"slave_Response")
        self.slave_Response.setGeometry(QRect(20, 370, 411, 51))
        self.slave_Response.setAutoFillBackground(True)
        self.label_5 = QLabel(self.RDM_tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(40, 120, 101, 20))
        self.label_5.setFont(font)
        self.parametro = QComboBox(self.RDM_tab)
        self.parametro.addItem("")
        self.parametro.addItem("")
        self.parametro.addItem("")
        self.parametro.setObjectName(u"parametro")
        self.parametro.setGeometry(QRect(200, 80, 211, 22))
        self.label_6 = QLabel(self.RDM_tab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(40, 160, 101, 20))
        self.label_6.setFont(font)
        self.port_ID = QLineEdit(self.RDM_tab)
        self.port_ID.setObjectName(u"port_ID")
        self.port_ID.setGeometry(QRect(200, 240, 211, 21))
        self.port_ID.setMaxLength(32767)
        self.port_ID.setFrame(True)
        self.label_7 = QLabel(self.RDM_tab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(40, 200, 101, 20))
        self.label_7.setFont(font)
        self.label_13 = QLabel(self.RDM_tab)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(180, 240, 16, 16))
        self.classe = QComboBox(self.RDM_tab)
        self.classe.addItem("")
        self.classe.addItem("")
        self.classe.addItem("")
        self.classe.setObjectName(u"classe")
        self.classe.setGeometry(QRect(120, 80, 68, 22))
        self.label_12 = QLabel(self.RDM_tab)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(180, 200, 16, 16))
        self.label = QLabel(self.RDM_tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(130, 60, 49, 16))
        self.send_command = QPushButton(self.RDM_tab)
        self.send_command.setObjectName(u"send_command")
        self.send_command.setGeometry(QRect(170, 290, 121, 24))
        self.label_8 = QLabel(self.RDM_tab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(40, 240, 101, 20))
        self.label_8.setFont(font)
        self.destination_UID = QLineEdit(self.RDM_tab)
        self.destination_UID.setObjectName(u"destination_UID")
        self.destination_UID.setGeometry(QRect(200, 120, 211, 21))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.destination_UID.sizePolicy().hasHeightForWidth())
        self.destination_UID.setSizePolicy(sizePolicy)
        self.destination_UID.setBaseSize(QSize(0, 0))
        self.destination_UID.setFrame(True)
        self.sub_device = QLineEdit(self.RDM_tab)
        self.sub_device.setObjectName(u"sub_device")
        self.sub_device.setGeometry(QRect(200, 200, 211, 21))
        self.sub_device.setFrame(True)
        self.tabWidget.addTab(self.RDM_tab, "")
        self.DMX_tab = QWidget()
        self.DMX_tab.setObjectName(u"DMX_tab")
        self.label_14 = QLabel(self.DMX_tab)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(240, 250, 101, 20))
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        self.label_14.setFont(font2)
        self.spinBox_2 = QSpinBox(self.DMX_tab)
        self.spinBox_2.setObjectName(u"spinBox_2")
        self.spinBox_2.setGeometry(QRect(280, 210, 91, 22))
        self.send_command_2 = QPushButton(self.DMX_tab)
        self.send_command_2.setObjectName(u"send_command_2")
        self.send_command_2.setGeometry(QRect(160, 340, 121, 24))
        self.spinBox_3 = QSpinBox(self.DMX_tab)
        self.spinBox_3.setObjectName(u"spinBox_3")
        self.spinBox_3.setGeometry(QRect(280, 250, 91, 22))
        self.spinBox_4 = QSpinBox(self.DMX_tab)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setGeometry(QRect(130, 250, 91, 22))
        self.label_15 = QLabel(self.DMX_tab)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(240, 210, 101, 20))
        self.label_15.setFont(font2)
        self.label_16 = QLabel(self.DMX_tab)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(70, 210, 101, 20))
        self.label_16.setFont(font2)
        self.distination_UID_2 = QLineEdit(self.DMX_tab)
        self.distination_UID_2.setObjectName(u"distination_UID_2")
        self.distination_UID_2.setGeometry(QRect(210, 130, 211, 21))
        sizePolicy.setHeightForWidth(self.distination_UID_2.sizePolicy().hasHeightForWidth())
        self.distination_UID_2.setSizePolicy(sizePolicy)
        self.distination_UID_2.setBaseSize(QSize(0, 0))
        self.distination_UID_2.setFrame(True)
        self.label_17 = QLabel(self.DMX_tab)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(30, 130, 141, 20))
        self.label_17.setFont(font)
        self.label_18 = QLabel(self.DMX_tab)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(60, 250, 101, 20))
        self.label_18.setFont(font2)
        self.spinBox = QSpinBox(self.DMX_tab)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setGeometry(QRect(130, 210, 91, 22))
        self.label_19 = QLabel(self.DMX_tab)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(150, 30, 141, 41))
        self.label_19.setFont(font1)
        self.tabWidget.addTab(self.DMX_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 451, 22))
        self.menuAjuda = QMenu(self.menubar)
        self.menuAjuda.setObjectName(u"menuAjuda")
        self.menuSair = QMenu(self.menubar)
        self.menuSair.setObjectName(u"menuSair")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuSair.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionDMX.setText(QCoreApplication.translate("MainWindow", u"RDM", None))
        self.actionRDM.setText(QCoreApplication.translate("MainWindow", u"DMX", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Resposta do slave", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Comando", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Par\u00e2metro", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"0x", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"RDM - Master", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"0x", None))
        self.slave_Response.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"UID de destino", None))
        self.parametro.setItemText(0, QCoreApplication.translate("MainWindow", u"Unique Branch", None))
        self.parametro.setItemText(1, QCoreApplication.translate("MainWindow", u"Mute", None))
        self.parametro.setItemText(2, QCoreApplication.translate("MainWindow", u"Unmute", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"UID da fonte", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Sub device", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"0x", None))
        self.classe.setItemText(0, QCoreApplication.translate("MainWindow", u"DISC", None))
        self.classe.setItemText(1, QCoreApplication.translate("MainWindow", u"GET", None))
        self.classe.setItemText(2, QCoreApplication.translate("MainWindow", u"SET", None))

        self.label_12.setText(QCoreApplication.translate("MainWindow", u"0x", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Classe", None))
        self.send_command.setText(QCoreApplication.translate("MainWindow", u"Enviar comando", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Port ID", None))
        self.destination_UID.setInputMask("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.RDM_tab), QCoreApplication.translate("MainWindow", u"Mode RDM", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Verde", None))
        self.send_command_2.setText(QCoreApplication.translate("MainWindow", u"Enviar comando", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Azul", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Branco", None))
        self.distination_UID_2.setInputMask("")
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Endere\u00e7o da lumin\u00e1ria", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Vermelho", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"DMX - Master", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.DMX_tab), QCoreApplication.translate("MainWindow", u"Mode DMX", None))
        self.menuAjuda.setTitle(QCoreApplication.translate("MainWindow", u"Ajuda", None))
        self.menuSair.setTitle(QCoreApplication.translate("MainWindow", u"Sair", None))
    # retranslateUi

