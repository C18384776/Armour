import sys

from PyQt5.QtCore import QEvent, QEventLoop
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction

from ui_main import *
from registration import UiRegistration
from login import UiLogin
import database


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.listWidget_groups.installEventFilter(self)

        self.ui.actionNew_Database.triggered.connect(lambda: self.new_database_clicked())

        self.ui.actionOpen_Database.triggered.connect(lambda: self.open_database_clicked())

        self.ui.actionAbout.triggered.connect(lambda: self.testing())

        self.current_password = None
        self.current_database = None

    def testing(self):
        print(self.UI_Log.master_password)
        print(self.UI_Log.database)

    def reload_database(self):
        # Do windows later...
        with open("/tmp/armour.db", 'wb') as file:
            file.write(self.current_database)
            file.close()

        con = database.make_connection("/tmp/armour.db")


        # with open("testing.db", 'rb') as file:
        #     file.read()
        #     print(file.read())

    def new_database_clicked(self):
        self.reg_window = QtWidgets.QWidget()
        self.UI_Reg = UiRegistration()
        self.UI_Reg.setup_ui_registration(self.reg_window)
        self.reg_window.show()
        print("Register Opened")

    def open_database_clicked(self):
        self.login_window = QtWidgets.QWidget()
        self.UI_Log = UiLogin()
        self.UI_Log.setup_ui_login(self.login_window)
        self.login_window.show()
        loop = QEventLoop()
        # By default, login is hidden on close()
        # This attribute makes it destroyed.
        self.login_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.login_window.destroyed.connect(loop.quit)
        loop.exec()
        print("Login Opened")
        # Assigns current settings.
        self.current_password = self.UI_Log.master_password
        self.current_database = self.UI_Log.database
        print("password passed {}".format(self.current_password))
        print("database passed {}".format(self.current_database))
        self.reload_database()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.ui.listWidget_groups:
            menu = QtWidgets.QMenu()
            new_group = QAction("New Group")
            edit_group = QAction("Edit Group")
            delete_group = QAction("Delete Group")
            menu.addAction(new_group)
            menu.addAction(edit_group)
            menu.addAction(delete_group)

            # User right-clicks on a group.
            if source.itemAt(event.pos()):
                menu_select = menu.exec(event.globalPos())

                if menu_select == new_group:
                    print("new group")
                elif menu_select == edit_group:
                    print("edit group")
                elif menu_select == delete_group:
                    print("Delete group")
                else:
                    print("user clicked out of group.")

                return True
            # User right clicks empty space.
            else:
                menu.clear()
                menu.addAction(new_group)
                menu_select = menu.exec(event.globalPos())

                if menu_select == new_group:
                    print("User clicked on new group")
                print("user clicked on non-group")

                return True

        return super(MainWindow, self).eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
