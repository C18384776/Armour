import sys

from PyQt5.QtCore import QEvent, QEventLoop
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QInputDialog, QLineEdit

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
        self.current_selected_group = None
        self.con = None

    def testing(self):
        print(self.UI_Log.master_password)
        print(self.UI_Log.database)

    def open_database(self):
        # Do windows later...
        with open("/tmp/armour.db", 'wb') as file:
            file.write(self.current_database)
            file.close()

        self.con = database.make_connection("/tmp/armour.db")
        ### Need to close database connection someday.

    def reload_database(self):
        # If database not loaded in.
        if self.con is None:
            self.open_database()
            print("CONNECTION NOT HAPPENED")

        self.cur = self.con.cursor()
        self.cur.execute("SELECT * FROM groups")
        groups = self.cur.fetchall()

        # Clear groups before import
        self.ui.listWidget_groups.clear()

        for group in groups:
            self.ui.listWidget_groups.addItem(group[1])
            # print(group[1])

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
        if self.UI_Log.master_password is not None:
            self.current_password = self.UI_Log.master_password
            self.current_database = self.UI_Log.database
            print("password passed {}".format(self.current_password))
            print("database passed {}".format(self.current_database))
            self.reload_database()

    def add_to_group(self):
        text, submit = QInputDialog.getText(self, "Add a new group", "Enter new group name")
        if submit and text != '':
            self.ui.listWidget_groups.addItem(text)
            sql_group_insert = """INSERT INTO groups(groupName) VALUES(?)"""
            new_group_name = [text]
            database.database_query(self.con, sql_group_insert, new_group_name)
            self.con.commit()
            self.reload_database()

    def edit_group(self, edit_group_location, group_to_edit):
        print("in edit group with {}".format(group_to_edit))
        if group_to_edit is not None:
            text, submit = QInputDialog.getText(self, "Edit a group", "Edit group name", QLineEdit.Normal, group_to_edit)

            if submit and text != '':
                edit_group_location.setText(text)
                # self.ui.listWidget_groups.itemAt(edit_group_location).setText(text)


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
                    self.add_to_group()
                    print(source.itemAt(event.pos()))
                    print("new group")
                elif menu_select == edit_group:
                    temp = source.itemAt(event.pos())
                    print(temp)
                    self.edit_group(source.itemAt(event.pos()), temp.text())
                    print(source.itemAt(event.pos()))
                    print("edit group")
                elif menu_select == delete_group:
                    print(source.itemAt(event.pos()))
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
                    self.add_to_group()
                    print(source.itemAt(event.pos()))
                    print("User clicked on new group")
                print("user clicked on non-group")

                return True

        return super(MainWindow, self).eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
