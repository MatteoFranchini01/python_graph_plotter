# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QHBoxLayout,
    QListView, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1156, 754)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 201, 701))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.horizontalLayoutWidget)
        self.widget.setObjectName(u"widget")
        self.listView = QListView(self.widget)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(0, 320, 201, 381))
        self.tabWidget = QTabWidget(self.widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 201, 321))
        self.graph_1 = QWidget()
        self.graph_1.setObjectName(u"graph_1")
        self.stopRegButton = QPushButton(self.graph_1)
        self.stopRegButton.setObjectName(u"stopRegButton")
        self.stopRegButton.setGeometry(QRect(20, 100, 100, 32))
        self.minSpinBox = QDoubleSpinBox(self.graph_1)
        self.minSpinBox.setObjectName(u"minSpinBox")
        self.minSpinBox.setGeometry(QRect(120, 70, 62, 22))
        self.minLineCheckBox = QCheckBox(self.graph_1)
        self.minLineCheckBox.setObjectName(u"minLineCheckBox")
        self.minLineCheckBox.setGeometry(QRect(20, 70, 85, 20))
        self.alertMinCheckBox = QCheckBox(self.graph_1)
        self.alertMinCheckBox.setObjectName(u"alertMinCheckBox")
        self.alertMinCheckBox.setGeometry(QRect(20, 170, 85, 20))
        self.alertMaxCheckBox = QCheckBox(self.graph_1)
        self.alertMaxCheckBox.setObjectName(u"alertMaxCheckBox")
        self.alertMaxCheckBox.setGeometry(QRect(20, 140, 85, 20))
        self.maxLineCheckBox = QCheckBox(self.graph_1)
        self.maxLineCheckBox.setObjectName(u"maxLineCheckBox")
        self.maxLineCheckBox.setGeometry(QRect(20, 40, 85, 20))
        self.maxSpinBox = QDoubleSpinBox(self.graph_1)
        self.maxSpinBox.setObjectName(u"maxSpinBox")
        self.maxSpinBox.setGeometry(QRect(120, 40, 62, 22))
        self.tabWidget.addTab(self.graph_1, "")
        self.graph_2 = QWidget()
        self.graph_2.setObjectName(u"graph_2")
        self.alertMaxCheckBox_2 = QCheckBox(self.graph_2)
        self.alertMaxCheckBox_2.setObjectName(u"alertMaxCheckBox_2")
        self.alertMaxCheckBox_2.setGeometry(QRect(20, 140, 85, 20))
        self.minLineCheckBox_2 = QCheckBox(self.graph_2)
        self.minLineCheckBox_2.setObjectName(u"minLineCheckBox_2")
        self.minLineCheckBox_2.setGeometry(QRect(20, 70, 85, 20))
        self.alertMinCheckBox_2 = QCheckBox(self.graph_2)
        self.alertMinCheckBox_2.setObjectName(u"alertMinCheckBox_2")
        self.alertMinCheckBox_2.setGeometry(QRect(20, 170, 85, 20))
        self.stopRegButton_2 = QPushButton(self.graph_2)
        self.stopRegButton_2.setObjectName(u"stopRegButton_2")
        self.stopRegButton_2.setGeometry(QRect(20, 100, 100, 32))
        self.maxSpinBox_2 = QDoubleSpinBox(self.graph_2)
        self.maxSpinBox_2.setObjectName(u"maxSpinBox_2")
        self.maxSpinBox_2.setGeometry(QRect(120, 40, 62, 22))
        self.minSpinBox_2 = QDoubleSpinBox(self.graph_2)
        self.minSpinBox_2.setObjectName(u"minSpinBox_2")
        self.minSpinBox_2.setGeometry(QRect(120, 70, 62, 22))
        self.maxLineCheckBox_2 = QCheckBox(self.graph_2)
        self.maxLineCheckBox_2.setObjectName(u"maxLineCheckBox_2")
        self.maxLineCheckBox_2.setGeometry(QRect(20, 40, 85, 20))
        self.tabWidget.addTab(self.graph_2, "")
        self.graph_3 = QWidget()
        self.graph_3.setObjectName(u"graph_3")
        self.alertMaxCheckBox_3 = QCheckBox(self.graph_3)
        self.alertMaxCheckBox_3.setObjectName(u"alertMaxCheckBox_3")
        self.alertMaxCheckBox_3.setGeometry(QRect(20, 140, 85, 20))
        self.minLineCheckBox_3 = QCheckBox(self.graph_3)
        self.minLineCheckBox_3.setObjectName(u"minLineCheckBox_3")
        self.minLineCheckBox_3.setGeometry(QRect(20, 70, 85, 20))
        self.alertMinCheckBox_3 = QCheckBox(self.graph_3)
        self.alertMinCheckBox_3.setObjectName(u"alertMinCheckBox_3")
        self.alertMinCheckBox_3.setGeometry(QRect(20, 170, 85, 20))
        self.stopRegButton_3 = QPushButton(self.graph_3)
        self.stopRegButton_3.setObjectName(u"stopRegButton_3")
        self.stopRegButton_3.setGeometry(QRect(20, 100, 100, 32))
        self.maxSpinBox_3 = QDoubleSpinBox(self.graph_3)
        self.maxSpinBox_3.setObjectName(u"maxSpinBox_3")
        self.maxSpinBox_3.setGeometry(QRect(120, 40, 62, 22))
        self.minSpinBox_3 = QDoubleSpinBox(self.graph_3)
        self.minSpinBox_3.setObjectName(u"minSpinBox_3")
        self.minSpinBox_3.setGeometry(QRect(120, 70, 62, 22))
        self.maxLineCheckBox_3 = QCheckBox(self.graph_3)
        self.maxLineCheckBox_3.setObjectName(u"maxLineCheckBox_3")
        self.maxLineCheckBox_3.setGeometry(QRect(20, 40, 85, 20))
        self.tabWidget.addTab(self.graph_3, "")
        self.graph_4 = QWidget()
        self.graph_4.setObjectName(u"graph_4")
        self.alertMaxCheckBox_4 = QCheckBox(self.graph_4)
        self.alertMaxCheckBox_4.setObjectName(u"alertMaxCheckBox_4")
        self.alertMaxCheckBox_4.setGeometry(QRect(20, 140, 85, 20))
        self.minLineCheckBox_4 = QCheckBox(self.graph_4)
        self.minLineCheckBox_4.setObjectName(u"minLineCheckBox_4")
        self.minLineCheckBox_4.setGeometry(QRect(20, 70, 85, 20))
        self.alertMinCheckBox_4 = QCheckBox(self.graph_4)
        self.alertMinCheckBox_4.setObjectName(u"alertMinCheckBox_4")
        self.alertMinCheckBox_4.setGeometry(QRect(20, 170, 85, 20))
        self.stopRegButton_4 = QPushButton(self.graph_4)
        self.stopRegButton_4.setObjectName(u"stopRegButton_4")
        self.stopRegButton_4.setGeometry(QRect(20, 100, 100, 32))
        self.maxSpinBox_4 = QDoubleSpinBox(self.graph_4)
        self.maxSpinBox_4.setObjectName(u"maxSpinBox_4")
        self.maxSpinBox_4.setGeometry(QRect(120, 40, 62, 22))
        self.minSpinBox_4 = QDoubleSpinBox(self.graph_4)
        self.minSpinBox_4.setObjectName(u"minSpinBox_4")
        self.minSpinBox_4.setGeometry(QRect(120, 70, 62, 22))
        self.maxLineCheckBox_4 = QCheckBox(self.graph_4)
        self.maxLineCheckBox_4.setObjectName(u"maxLineCheckBox_4")
        self.maxLineCheckBox_4.setGeometry(QRect(20, 40, 85, 20))
        self.tabWidget.addTab(self.graph_4, "")

        self.horizontalLayout.addWidget(self.widget)

        self.graphicsContainer = QWidget(self.centralwidget)
        self.graphicsContainer.setObjectName(u"graphicsContainer")
        self.graphicsContainer.setGeometry(QRect(200, 0, 951, 701))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1156, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.stopRegButton.setText(QCoreApplication.translate("MainWindow", u"Stop Reg", None))
        self.minLineCheckBox.setText(QCoreApplication.translate("MainWindow", u"Min line", None))
        self.alertMinCheckBox.setText(QCoreApplication.translate("MainWindow", u"Alert Min", None))
        self.alertMaxCheckBox.setText(QCoreApplication.translate("MainWindow", u"Alert Max", None))
        self.maxLineCheckBox.setText(QCoreApplication.translate("MainWindow", u"Max line", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.graph_1), QCoreApplication.translate("MainWindow", u"G 1", None))
        self.alertMaxCheckBox_2.setText(QCoreApplication.translate("MainWindow", u"Alert Max", None))
        self.minLineCheckBox_2.setText(QCoreApplication.translate("MainWindow", u"Min line", None))
        self.alertMinCheckBox_2.setText(QCoreApplication.translate("MainWindow", u"Alert Min", None))
        self.stopRegButton_2.setText(QCoreApplication.translate("MainWindow", u"Stop Reg", None))
        self.maxLineCheckBox_2.setText(QCoreApplication.translate("MainWindow", u"Max line", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.graph_2), QCoreApplication.translate("MainWindow", u"G 2", None))
        self.alertMaxCheckBox_3.setText(QCoreApplication.translate("MainWindow", u"Alert Max", None))
        self.minLineCheckBox_3.setText(QCoreApplication.translate("MainWindow", u"Min line", None))
        self.alertMinCheckBox_3.setText(QCoreApplication.translate("MainWindow", u"Alert Min", None))
        self.stopRegButton_3.setText(QCoreApplication.translate("MainWindow", u"Stop Reg", None))
        self.maxLineCheckBox_3.setText(QCoreApplication.translate("MainWindow", u"Max line", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.graph_3), QCoreApplication.translate("MainWindow", u"G 3", None))
        self.alertMaxCheckBox_4.setText(QCoreApplication.translate("MainWindow", u"Alert Max", None))
        self.minLineCheckBox_4.setText(QCoreApplication.translate("MainWindow", u"Min line", None))
        self.alertMinCheckBox_4.setText(QCoreApplication.translate("MainWindow", u"Alert Min", None))
        self.stopRegButton_4.setText(QCoreApplication.translate("MainWindow", u"Stop Reg", None))
        self.maxLineCheckBox_4.setText(QCoreApplication.translate("MainWindow", u"Max line", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.graph_4), QCoreApplication.translate("MainWindow", u"G 4", None))
    # retranslateUi

