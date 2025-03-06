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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QGraphicsView,
    QHBoxLayout, QListView, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(200, 0, 601, 551))
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 201, 551))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.horizontalLayoutWidget)
        self.widget.setObjectName(u"widget")
        self.maxLineCheckBox = QCheckBox(self.widget)
        self.maxLineCheckBox.setObjectName(u"maxLineCheckBox")
        self.maxLineCheckBox.setGeometry(QRect(10, 10, 85, 20))
        self.minLineCheckBox = QCheckBox(self.widget)
        self.minLineCheckBox.setObjectName(u"minLineCheckBox")
        self.minLineCheckBox.setGeometry(QRect(10, 40, 85, 20))
        self.maxSpinBox = QDoubleSpinBox(self.widget)
        self.maxSpinBox.setObjectName(u"maxSpinBox")
        self.maxSpinBox.setGeometry(QRect(110, 10, 62, 22))
        self.minSpinBox = QDoubleSpinBox(self.widget)
        self.minSpinBox.setObjectName(u"minSpinBox")
        self.minSpinBox.setGeometry(QRect(110, 40, 62, 22))
        self.listView = QListView(self.widget)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(0, 170, 201, 381))
        self.stopRegButton = QPushButton(self.widget)
        self.stopRegButton.setObjectName(u"stopRegButton")
        self.stopRegButton.setGeometry(QRect(10, 70, 100, 32))
        self.alertMaxCheckBox = QCheckBox(self.widget)
        self.alertMaxCheckBox.setObjectName(u"alertMaxCheckBox")
        self.alertMaxCheckBox.setGeometry(QRect(10, 110, 85, 20))
        self.alertMinCheckBox = QCheckBox(self.widget)
        self.alertMinCheckBox.setObjectName(u"alertMinCheckBox")
        self.alertMinCheckBox.setGeometry(QRect(10, 140, 85, 20))

        self.horizontalLayout.addWidget(self.widget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.maxLineCheckBox.setText(QCoreApplication.translate("MainWindow", u"Max line", None))
        self.minLineCheckBox.setText(QCoreApplication.translate("MainWindow", u"Min line", None))
        self.stopRegButton.setText(QCoreApplication.translate("MainWindow", u"Stop Reg", None))
        self.alertMaxCheckBox.setText(QCoreApplication.translate("MainWindow", u"Alert Max", None))
        self.alertMinCheckBox.setText(QCoreApplication.translate("MainWindow", u"Alert Min", None))
    # retranslateUi

