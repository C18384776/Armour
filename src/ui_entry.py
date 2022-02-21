from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Entry(object):
    def setupUi(self, Entry):
        Entry.setObjectName("Entry")
        Entry.resize(516, 327)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Entry)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.website_layout = QtWidgets.QHBoxLayout()
        self.website_layout.setObjectName("website_layout")
        self.website_label = QtWidgets.QLabel(Entry)
        self.website_label.setObjectName("website_label")
        self.website_layout.addWidget(self.website_label)
        self.website_lineEdit = QtWidgets.QLineEdit(Entry)
        self.website_lineEdit.setObjectName("website_lineEdit")
        self.website_layout.addWidget(self.website_lineEdit)
        self.website_help = QtWidgets.QToolButton(Entry)
        self.website_help.setObjectName("website_help")
        self.website_layout.addWidget(self.website_help)
        self.verticalLayout_2.addLayout(self.website_layout)
        self.username_layout = QtWidgets.QHBoxLayout()
        self.username_layout.setObjectName("username_layout")
        self.username_label = QtWidgets.QLabel(Entry)
        self.username_label.setObjectName("username_label")
        self.username_layout.addWidget(self.username_label)
        self.username_lineEdit = QtWidgets.QLineEdit(Entry)
        self.username_lineEdit.setObjectName("username_lineEdit")
        self.username_layout.addWidget(self.username_lineEdit)
        self.username_help = QtWidgets.QToolButton(Entry)
        self.username_help.setObjectName("username_help")
        self.username_layout.addWidget(self.username_help)
        self.verticalLayout_2.addLayout(self.username_layout)
        self.password_layout = QtWidgets.QHBoxLayout()
        self.password_layout.setObjectName("password_layout")
        self.password_label = QtWidgets.QLabel(Entry)
        self.password_label.setObjectName("password_label")
        self.password_layout.addWidget(self.password_label)
        self.password_layout_2 = QtWidgets.QVBoxLayout()
        self.password_layout_2.setObjectName("password_layout_2")
        self.password_lineEdit = QtWidgets.QLineEdit(Entry)
        self.password_lineEdit.setObjectName("password_lineEdit")
        self.password_layout_2.addWidget(self.password_lineEdit)
        self.password_error_label = QtWidgets.QLabel(Entry)
        self.password_error_label.setObjectName("password_error_label")
        self.password_layout_2.addWidget(self.password_error_label)
        self.password_layout.addLayout(self.password_layout_2)
        self.password_view_button = QtWidgets.QPushButton(Entry)
        self.password_view_button.setObjectName("password_view_button")
        self.password_layout.addWidget(self.password_view_button)
        self.password_generator_button = QtWidgets.QPushButton(Entry)
        self.password_generator_button.setObjectName("password_generator_button")
        self.password_layout.addWidget(self.password_generator_button)
        self.password_help = QtWidgets.QToolButton(Entry)
        self.password_help.setObjectName("password_help")
        self.password_layout.addWidget(self.password_help)
        self.verticalLayout_2.addLayout(self.password_layout)
        self.repeat_layout = QtWidgets.QHBoxLayout()
        self.repeat_layout.setObjectName("repeat_layout")
        self.repeat_label = QtWidgets.QLabel(Entry)
        self.repeat_label.setTextFormat(QtCore.Qt.PlainText)
        self.repeat_label.setObjectName("repeat_label")
        self.repeat_layout.addWidget(self.repeat_label)
        self.repeat_lineEdit = QtWidgets.QLineEdit(Entry)
        self.repeat_lineEdit.setObjectName("repeat_lineEdit")
        self.repeat_layout.addWidget(self.repeat_lineEdit)
        self.verticalLayout_2.addLayout(self.repeat_layout)
        self.strength_layout = QtWidgets.QHBoxLayout()
        self.strength_layout.setObjectName("strength_layout")
        self.strength_label = QtWidgets.QLabel(Entry)
        self.strength_label.setObjectName("strength_label")
        self.strength_layout.addWidget(self.strength_label)
        self.strength_progressBar = QtWidgets.QProgressBar(Entry)
        self.strength_progressBar.setProperty("value", 24)
        self.strength_progressBar.setObjectName("strength_progressBar")
        self.strength_layout.addWidget(self.strength_progressBar)
        self.strength_help = QtWidgets.QToolButton(Entry)
        self.strength_help.setObjectName("strength_help")
        self.strength_layout.addWidget(self.strength_help)
        self.verticalLayout_2.addLayout(self.strength_layout)
        self.url_layout = QtWidgets.QHBoxLayout()
        self.url_layout.setObjectName("url_layout")
        self.url_label = QtWidgets.QLabel(Entry)
        self.url_label.setObjectName("url_label")
        self.url_layout.addWidget(self.url_label)
        self.url_lineEdit = QtWidgets.QLineEdit(Entry)
        self.url_lineEdit.setObjectName("url_lineEdit")
        self.url_layout.addWidget(self.url_lineEdit)
        self.url_help = QtWidgets.QToolButton(Entry)
        self.url_help.setObjectName("url_help")
        self.url_layout.addWidget(self.url_help)
        self.verticalLayout_2.addLayout(self.url_layout)
        self.twofa_layout = QtWidgets.QHBoxLayout()
        self.twofa_layout.setObjectName("twofa_layout")
        self.label_6 = QtWidgets.QLabel(Entry)
        self.label_6.setObjectName("label_6")
        self.twofa_layout.addWidget(self.label_6)
        self.twofa_lineEdit = QtWidgets.QLineEdit(Entry)
        self.twofa_lineEdit.setObjectName("twofa_lineEdit")
        self.twofa_layout.addWidget(self.twofa_lineEdit)
        self.twofa_help = QtWidgets.QToolButton(Entry)
        self.twofa_help.setObjectName("twofa_help")
        self.twofa_layout.addWidget(self.twofa_help)
        self.verticalLayout_2.addLayout(self.twofa_layout)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setObjectName("button_layout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.button_layout.addItem(spacerItem)
        self.cancel_button = QtWidgets.QPushButton(Entry)
        self.cancel_button.setObjectName("cancel_button")
        self.button_layout.addWidget(self.cancel_button)
        self.submit_button = QtWidgets.QPushButton(Entry)
        self.submit_button.setObjectName("submit_button")
        self.button_layout.addWidget(self.submit_button)
        self.verticalLayout_2.addLayout(self.button_layout)

        self.retranslateUi(Entry)
        QtCore.QMetaObject.connectSlotsByName(Entry)

    def retranslateUi(self, Entry):
        _translate = QtCore.QCoreApplication.translate
        Entry.setWindowTitle(_translate("Entry", "Form"))
        self.website_label.setText(_translate("Entry", "Website\n"
"Name"))
        self.website_help.setText(_translate("Entry", "?"))
        self.username_label.setText(_translate("Entry", "Username"))
        self.username_help.setText(_translate("Entry", "?"))
        self.password_label.setText(_translate("Entry", "Password"))
        self.password_error_label.setText(_translate("Entry", "Password cannot be empty!"))
        self.password_view_button.setText(_translate("Entry", "View"))
        self.password_generator_button.setText(_translate("Entry", "Generator"))
        self.password_help.setText(_translate("Entry", "?"))
        self.repeat_label.setText(_translate("Entry", "Repeat\n"
"Password"))
        self.strength_label.setText(_translate("Entry", "Password\n"
"Strength"))
        self.strength_help.setText(_translate("Entry", "?"))
        self.url_label.setText(_translate("Entry", "URL"))
        self.url_help.setText(_translate("Entry", "?"))
        self.label_6.setText(_translate("Entry", "2FA"))
        self.twofa_help.setText(_translate("Entry", "?"))
        self.cancel_button.setText(_translate("Entry", "Cancel"))
        self.submit_button.setText(_translate("Entry", "Submit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Entry = QtWidgets.QWidget()
    ui = Ui_Entry()
    ui.setupUi(Entry)
    Entry.show()
    sys.exit(app.exec_())
