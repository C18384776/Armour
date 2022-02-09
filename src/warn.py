from PyQt5.QtWidgets import QMessageBox


def password_warning_message():
    message = QMessageBox()
    message.setWindowTitle("Weak Password Detected")
    message.setText("""
                        Your password appears to be weak.
                        Weak password make it easier for people
                        to hack your account. While you may proceed 
                        with the current password, it is strongly 
                        recommended that you set a password of more 
                        than 100 bits as shown in the progress bar.

                        Click "Yes" to proceed or "No" to go back.""")
    message.setIcon(QMessageBox.Warning)
    message.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    message.setDefaultButton(QMessageBox.No)
    message.buttonClicked.connect(password_warning_response)
    message.exec_()


def password_warning_response(response):
    password_dialog_response = response.text()
    password_dialog_response = password_dialog_response.strip('&')
