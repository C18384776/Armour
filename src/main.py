import sys

from PyQt5.QtCore import QEvent, QEventLoop
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QInputDialog, QLineEdit, QMessageBox

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
        self.ui.listWidget_groups.itemClicked.connect(self.group_clicked)

        self.ui.actionNew_Database.triggered.connect(lambda: self.new_database_clicked())
        self.ui.actionOpen_Database.triggered.connect(lambda: self.open_database_clicked())

        self.ui.tableWidget_entries.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.current_password = None
        self.current_database = None
        self.current_selected_group = None
        self.con = None

    def group_clicked(self, item):
        print("Clicked: {}".format(item.text()))

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
            print("CONNECTION HAPPENED")

        # (Re)load groups
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

        self.cur.execute("SELECT * FROM passwords WHERE groupId = (?)", [1])
        entries = self.cur.fetchall()
        # (Re)load password entries for specific selected group.
        self.ui.tableWidget_entries.setRowCount(len(entries))
        print(entries)
        row = 0
        for entry in entries:
            self.ui.tableWidget_entries.setItem(row, 0, QtWidgets.QTableWidgetItem(str(entry[1])))
            self.ui.tableWidget_entries.setItem(row, 1, QtWidgets.QTableWidgetItem(str(entry[2])))
            self.ui.tableWidget_entries.setItem(row, 2, QtWidgets.QTableWidgetItem(str(entry[3])))
            self.ui.tableWidget_entries.setItem(row, 3, QtWidgets.QTableWidgetItem(str(entry[4])))
            self.ui.tableWidget_entries.setItem(row, 4, QtWidgets.QTableWidgetItem(str(entry[5])))
            self.ui.tableWidget_entries.setItem(row, 5, QtWidgets.QTableWidgetItem(str(entry[6])))
            row += 1

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

        # Query checks if exact name already exists.
        self.cur.execute("SELECT groupName FROM groups WHERE groupName = (?)", [text])
        groups = self.cur.fetchall()
        print("Inside group ADD: {}".format(groups))
        if submit and text != '' and groups == []:
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

            # Query checks if exact name already exists.
            self.cur.execute("SELECT groupName FROM groups WHERE groupName = (?)", [text])
            groups = self.cur.fetchall()
            print("Inside group EDIT: {}".format(groups))

            if submit and text != '' and groups == []:
                edit_group_location.setText(text)
                sql_group_update = """UPDATE groups SET groupName = (?) WHERE groupName = (?)"""
                edit_group_name = [text, group_to_edit]
                database.database_query(self.con, sql_group_update, edit_group_name)
                self.con.commit()
                self.reload_database()

    def delete_group(self, delete_group_location, group_to_delete):
        print("in delete group method with {}".format(group_to_delete))

        reply = QMessageBox.question(self, "Remove a group",
                                     "Do you really want to remove the group " + str(group_to_delete) + "?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes and group_to_delete != "Recycle Bin":
            row = self.ui.listWidget_groups.row(delete_group_location)
            self.ui.listWidget_groups.takeItem(row)
            sql_group_delete = """DELETE FROM groups WHERE groupName = (?)"""
            delete_group_name = [group_to_delete]
            database.database_query(self.con, sql_group_delete, delete_group_name)
            self.con.commit()
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
                    self.add_to_group()
                elif menu_select == edit_group:
                    temp = source.itemAt(event.pos())
                    self.edit_group(source.itemAt(event.pos()), temp.text())
                elif menu_select == delete_group:
                    temp = source.itemAt(event.pos())
                    self.delete_group(source.itemAt(event.pos()), temp.text())
                    print(source.itemAt(event.pos()))
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

                return True

        return super(MainWindow, self).eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
