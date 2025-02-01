# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 400)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_connection = QGroupBox(Form)
        self.groupBox_connection.setObjectName(u"groupBox_connection")
        self.gridLayout_connection = QGridLayout(self.groupBox_connection)
        self.gridLayout_connection.setObjectName(u"gridLayout_connection")
        self.label_device = QLabel(self.groupBox_connection)
        self.label_device.setObjectName(u"label_device")

        self.gridLayout_connection.addWidget(self.label_device, 0, 0, 1, 1)

        self.lineEdit_device = QLineEdit(self.groupBox_connection)
        self.lineEdit_device.setObjectName(u"lineEdit_device")

        self.gridLayout_connection.addWidget(self.lineEdit_device, 0, 1, 1, 1)

        self.label_cert = QLabel(self.groupBox_connection)
        self.label_cert.setObjectName(u"label_cert")

        self.gridLayout_connection.addWidget(self.label_cert, 1, 0, 1, 1)

        self.lineEdit_cert = QLineEdit(self.groupBox_connection)
        self.lineEdit_cert.setObjectName(u"lineEdit_cert")

        self.gridLayout_connection.addWidget(self.lineEdit_cert, 1, 1, 1, 1)

        self.button_browse_cert = QPushButton(self.groupBox_connection)
        self.button_browse_cert.setObjectName(u"button_browse_cert")

        self.gridLayout_connection.addWidget(self.button_browse_cert, 1, 2, 1, 1)

        self.label_key = QLabel(self.groupBox_connection)
        self.label_key.setObjectName(u"label_key")

        self.gridLayout_connection.addWidget(self.label_key, 2, 0, 1, 1)

        self.lineEdit_key = QLineEdit(self.groupBox_connection)
        self.lineEdit_key.setObjectName(u"lineEdit_key")

        self.gridLayout_connection.addWidget(self.lineEdit_key, 2, 1, 1, 1)

        self.button_browse_key = QPushButton(self.groupBox_connection)
        self.button_browse_key.setObjectName(u"button_browse_key")

        self.gridLayout_connection.addWidget(self.button_browse_key, 2, 2, 1, 1)

        self.button_connect = QPushButton(self.groupBox_connection)
        self.button_connect.setObjectName(u"button_connect")

        self.gridLayout_connection.addWidget(self.button_connect, 3, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_connection)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox_edit = QGroupBox(Form)
        self.groupBox_edit.setObjectName(u"groupBox_edit")
        self.verticalLayout_edit = QVBoxLayout(self.groupBox_edit)
        self.verticalLayout_edit.setObjectName(u"verticalLayout_edit")
        self.textEdit_editable = QTextEdit(self.groupBox_edit)
        self.textEdit_editable.setObjectName(u"textEdit_editable")

        self.verticalLayout_edit.addWidget(self.textEdit_editable)

        self.button_send = QPushButton(self.groupBox_edit)
        self.button_send.setObjectName(u"button_send")

        self.verticalLayout_edit.addWidget(self.button_send)


        self.horizontalLayout.addWidget(self.groupBox_edit)

        self.groupBox_readonly = QGroupBox(Form)
        self.groupBox_readonly.setObjectName(u"groupBox_readonly")
        self.verticalLayout_readonly = QVBoxLayout(self.groupBox_readonly)
        self.verticalLayout_readonly.setObjectName(u"verticalLayout_readonly")
        self.textEdit_readonly = QTextEdit(self.groupBox_readonly)
        self.textEdit_readonly.setObjectName(u"textEdit_readonly")
        self.textEdit_readonly.setReadOnly(True)

        self.verticalLayout_readonly.addWidget(self.textEdit_readonly)

        self.button_refresh = QPushButton(self.groupBox_readonly)
        self.button_refresh.setObjectName(u"button_refresh")

        self.verticalLayout_readonly.addWidget(self.button_refresh)


        self.horizontalLayout.addWidget(self.groupBox_readonly)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        self.groupBox_connection.setTitle(QCoreApplication.translate("Form", u"Device Connection", None))
        self.label_device.setText(QCoreApplication.translate("Form", u"Device Name:", None))
        self.label_cert.setText(QCoreApplication.translate("Form", u"Certificate File:", None))
        self.button_browse_cert.setText(QCoreApplication.translate("Form", u"Browse", None))
        self.label_key.setText(QCoreApplication.translate("Form", u"Key File:", None))
        self.button_browse_key.setText(QCoreApplication.translate("Form", u"Browse", None))
        self.button_connect.setText(QCoreApplication.translate("Form", u"Connect", None))
        self.groupBox_edit.setTitle(QCoreApplication.translate("Form", u"Editable Shadow Document", None))
        self.button_send.setText(QCoreApplication.translate("Form", u"Send", None))
        self.groupBox_readonly.setTitle(QCoreApplication.translate("Form", u"Reported Shadow Document", None))
        self.button_refresh.setText(QCoreApplication.translate("Form", u"Refresh", None))
        pass
    # retranslateUi

