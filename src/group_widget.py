from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, QInputDialog, QLineEdit, QMessageBox
import database


def group_widget(source, event, cursor, list_widget, connection, main_window):
    menu = QtWidgets.QMenu()
    new_group_action = QAction("New Group")
    edit_group_action = QAction("Edit Group")
    delete_group_action = QAction("Delete Group")
    menu.addAction(new_group_action)
    menu.addAction(edit_group_action)
    menu.addAction(delete_group_action)

    # User right-clicks on a group.
    if source.itemAt(event.pos()):
        menu_select = menu.exec(event.globalPos())

        if menu_select == new_group_action:
            success = add_to_group(cursor, list_widget, connection, main_window)
            return success
        elif menu_select == edit_group_action:
            temp = source.itemAt(event.pos())
            success = edit_group(source.itemAt(event.pos()), temp.text(), main_window, cursor, connection)
            return success
        elif menu_select == delete_group_action:
            temp = source.itemAt(event.pos())
            delete_group(source.itemAt(event.pos()), temp.text(), main_window, list_widget, connection)
            print(source.itemAt(event.pos()))
        else:
            print("user clicked out of group.")

        return True
    # User right clicks empty space.
    else:
        menu.clear()
        menu.addAction(new_group_action)
        menu_select = menu.exec(event.globalPos())

        if menu_select == new_group_action:
            success = add_to_group(cursor, list_widget, connection, main_window)
            print(source.itemAt(event.pos()))
            return success

        return True


def add_to_group(cursor, list_widget, connection, main_window):
    text, submit = QInputDialog.getText(main_window, "Add a new group", "Enter new group name")

    # Query checks if exact name already exists.
    cursor.execute("SELECT groupName FROM groups WHERE groupName = (?)", [text])
    groups = cursor.fetchall()
    print("Inside group ADD: {}".format(groups))
    if submit and text != '' and groups == []:
        list_widget.addItem(text)
        sql_group_insert = """INSERT INTO groups(groupName) VALUES(?)"""
        new_group_name = [text]
        database.database_query(connection, sql_group_insert, new_group_name)
        connection.commit()
        return True


def edit_group(edit_group_location, group_to_edit, main_window, cursor, connection):
    print("in edit group with {}".format(group_to_edit))
    if group_to_edit is not None:
        text, submit = QInputDialog.getText(main_window,
                                            "Edit a group", "Edit group name",
                                            QLineEdit.Normal,
                                            group_to_edit)

        # Query checks if exact name already exists.
        cursor.execute("SELECT groupName FROM groups WHERE groupName = (?)", [text])
        groups = cursor.fetchall()
        print("Inside group EDIT: {}".format(groups))

        if submit and text != '' and groups == []:
            # edit_group_location.setText(text)
            sql_group_update = """UPDATE groups SET groupName = (?) WHERE groupName = (?)"""
            edit_group_name = [text, group_to_edit]
            database.database_query(connection, sql_group_update, edit_group_name)
            connection.commit()
            return True


def delete_group(delete_group_location, group_to_delete, main_window, list_widget, connection, action_button=False):
    print("in delete group method with {}".format(group_to_delete))
    print(delete_group_location)

    reply = QMessageBox.question(main_window, "Remove a group",
                                 "Do you really want to remove the group " +
                                 str(group_to_delete) +
                                 "?", QMessageBox.Yes | QMessageBox.No)

    if reply == QMessageBox.Yes and group_to_delete != "Recycle Bin":
        if action_button == True:
            row = list_widget.row(list_widget.item(delete_group_location))
        else:
            row = list_widget.row(delete_group_location)
        list_widget.takeItem(row)
        sql_group_delete = """DELETE FROM groups WHERE groupId = (?)"""
        delete_group_name = [delete_group_location]
        database.database_query(connection, sql_group_delete, delete_group_name)
        connection.commit()
        return True
