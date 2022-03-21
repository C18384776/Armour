import sys

from PyQt5 import QtWidgets
from ui_prevpass import Ui_PreviousPasswords
import qdarkstyle

class PreviousPasswords(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.ui = Ui_PreviousPasswords()
        self.ui.setupUi(self)
        self.show()

        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PreviousPasswords()
    window.show()
    sys.exit(app.exec_())
