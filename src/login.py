from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from ui_login import *


class Login(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Login = QtWidgets.QWidget()
        self.ui = UiLogin
        self.ui.setup_ui_login(self, Login)
        self.show()
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Login = QtWidgets.QWidget()
#     ui = UiLogin()
#     ui.setup_ui_login(Login)
#     Login.show()
#     sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())
