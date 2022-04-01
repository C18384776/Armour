from PyQt5.QtWidgets import QMessageBox


def directory_edit_moment():
    message = QMessageBox()
    message.setWindowTitle("Dir edit")
    message.setText("""Yoooo this is directory here lmao""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    # message.buttonClicked.connect(password_warning_response)
    message.exec_()
