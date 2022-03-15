import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QEventLoop
from PyQt5.QtWidgets import QAction, QMessageBox
import database
from entry import Entry


global entry_result


def table_widget(source, event, table_wid, main_window, connection, id_of_group):
    if event.button() == QtCore.Qt.RightButton:
        print("Right Button Pressed")
        index = table_wid.indexAt(event.pos())
        # Display content of cell
        print(index.data())

        menu = QtWidgets.QMenu()
        copy_username_action = QAction("Copy Username")
        copy_password_action = QAction("Copy Password")
        copy_totp_action = QAction("Copy TOTP")
        new_entry_action = QAction("New Entry")
        edit_entry_action = QAction("Edit Entry")
        delete_entry_action = QAction("Delete Entry")
        open_url_action = QAction("Open Website")

        menu.addAction(copy_username_action)
        menu.addAction(copy_password_action)
        menu.addAction(copy_totp_action)
        menu.addSeparator()
        menu.addAction(new_entry_action)
        menu.addAction(edit_entry_action)
        menu.addAction(delete_entry_action)
        menu.addSeparator()
        menu.addAction(open_url_action)

        if index.data() is not None:
            print(index.data())
            menu_select = menu.exec(event.globalPos())
            if menu_select == copy_username_action:
                pass
            if menu_select == copy_password_action:
                pass
            if menu_select == copy_totp_action:
                pass
            if menu_select == new_entry_action:
                print("New entry selected")
                new_entry_list = new_entry(id_of_group, connection)
                return new_entry_list
            if menu_select == edit_entry_action:
                edit_entry_list = edit_entry()
                return edit_entry_list
            if menu_select == delete_entry_action:
                # Selected row to delete.
                row_to_remove = index.row()
                # Selected row ID from database.
                id_of_entry = table_wid.item(row_to_remove, 0)
                # Selected row group ID from database.
                group_id_of_entry = table_wid.item(row_to_remove, 7)
                delete_entry(index.row(), id_of_entry.text(), group_id_of_entry.text(), main_window, connection)
            if menu_select == open_url_action:
                pass
            else:
                print("user clicked out of group.")

            return True
        # User right clicks empty space.
        else:
            menu.clear()
            menu.addAction(new_entry_action)
            menu_select = menu.exec(event.globalPos())

            if menu_select == new_entry_action:
                new_entry_list = new_entry(id_of_group, connection)
                return new_entry_list

            return True
    elif event.button() == QtCore.Qt.LeftButton:
        index = table_wid.indexAt(event.pos())
        print(index.data())
        print("Left button pressed")


def get_entry_fields(UI_entry):
    print("In get entry fields")
    result = UI_entry.get_entry_fields()
    print(result)
    print(result[0])
    print(result[1])
    print(result[2])
    print(result[3])
    print(result[4])
    print(result[5])
    globals()['entry_result'] = result


def new_entry(id_of_group, connection):
    UI_entry = Entry()
    UI_entry.__init__()

    # Detect that button was clicked from here and try to pass down variables
    UI_entry.ui.submit_button.clicked.connect(lambda: UI_entry.submitted())
    UI_entry.ui.submit_button.clicked.connect(lambda: get_entry_fields(UI_entry))
    UI_entry.show()
    loop = QEventLoop()
    # By default, login is hidden on close()
    # This attribute makes it destroyed.
    UI_entry.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    UI_entry.destroyed.connect(loop.quit)
    loop.exec()
    print("New entry window opened")
    # print(entry_result)
    # List is only returned if submission button is clicked and valid from New Entry Window.
    try:
        if entry_result[5] is False:
            return False
        else:
            insert_entry(entry_result, id_of_group, connection)
            globals()['entry_result'][5] = False
            return True
            # return [entry_result[0], entry_result[1], entry_result[2], entry_result[3], entry_result[4]]
    except NameError:
        print("table_widget.py: entry_result does not exist.")


def edit_entry():
    UI_entry = Entry()
    UI_entry.__init__()
    # Detect that button was clicked from here and try to pass down variables
    UI_entry.ui.submit_button.clicked.connect(lambda: UI_entry.submitted())
    UI_entry.ui.submit_button.clicked.connect(lambda: get_entry_fields(UI_entry))
    UI_entry.show()

def insert_entry(entry_result, id_of_group, connection):
    print("in insert entry method with {}".format(entry_result))
    print(entry_result[5])

    sql_entry_insert = """INSERT INTO passwords( passwordWebsite, 
    passwordName, passwordPassword, passwordUrl, 
    passwordCreation, password2FA, groupId) VALUES(?,?,?,?,?,?,?)"""

    pass_entry_one = [entry_result[0], entry_result[1], entry_result[2],
                      entry_result[4], datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
                      entry_result[5], id_of_group]
    database.database_query(connection, sql_entry_insert, pass_entry_one)
    connection.commit()


def delete_entry(row_to_delete, id_of_entry, group_id_of_entry, main_window, connection):
    print("in delete entry method with {} {} {}".format(row_to_delete, id_of_entry, group_id_of_entry))

    reply = QMessageBox.question(main_window, "Remove a group",
                                 "Do you really want to remove this entry?\n"
                                 "It will be moved to the Recycle Bin or delete entirely "
                                 "if it's there already.",
                                 QMessageBox.Yes | QMessageBox.No)

    # Move to recycle bin if not in it already; otherwise delete forever.
    if reply == QMessageBox.Yes and int(group_id_of_entry) != 5:
        print("Inside move to recycle")
        sql_entry_move_to_bin = """UPDATE passwords SET groupId = 5 WHERE passwordId = (?)"""
        database.database_query(connection, sql_entry_move_to_bin, [id_of_entry])
        connection.commit()
        return True
    elif reply == QMessageBox.Yes and int(group_id_of_entry) == 5:
        print("Inside recycle delete")
        sql_delete_entry = """DELETE FROM passwords WHERE passwordId = (?)"""
        database.database_query(connection, sql_delete_entry, [id_of_entry])
        connection.commit()
        return True
