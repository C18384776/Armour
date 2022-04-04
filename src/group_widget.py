from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QAction, QInputDialog, QLineEdit, QMessageBox
import database


def group_widget(source, event, cursor, list_widget, connection, main_window):
    """
    Generate a menu for group widget.

    :param source:
    Selected QListWidget.

    :param event:
    User right click

    :param cursor:
    Database cursor.

    :param list_widget:
    QListWidget object.

    :param connection:
    Database connection

    :param main_window:
    Main window class.
    """
    # Initialise a right click menu.
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

        # Users choice.
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
        else:
            print("user clicked out of group.")

        return True
    # User right clicks empty space.
    else:
        # Clears the big menu above if empty space clicked.
        menu.clear()
        # Since no group was clicked, there can only be an option to add a new group.
        menu.addAction(new_group_action)
        menu_select = menu.exec(event.globalPos())

        if menu_select == new_group_action:
            success = add_to_group(cursor, list_widget, connection, main_window)
            return success

        return True


def add_to_group(cursor, list_widget, connection, main_window):
    """
    Add a group to group list.

    :param cursor:
    Database cursor.

    :param list_widget:
    QListWidget of the program.

    :param connection:
    Database connection.

    :param main_window:
    Main window class.
    """
    # Dialog asking user to submit a group name.
    text, submit = QInputDialog.getText(main_window, "Add a new group", "Enter new group name")

    # Query checks if exact name already exists.
    cursor.execute("SELECT groupName FROM groups WHERE groupName = (?)", [text])
    groups = cursor.fetchall()

    # Submit the entered group to the database when it is not empty and doesn't already exist.
    if submit and text != '' and groups == []:
        list_widget.addItem(text)
        sql_group_insert = """INSERT INTO groups(groupName) VALUES(?)"""
        new_group_name = [text]
        database.database_query(connection, sql_group_insert, new_group_name)
        connection.commit()
        return True


def edit_group(edit_group_location, group_to_edit, main_window, cursor, connection):
    """
    Edit a group already there.

    :param edit_group_location:

    :param group_to_edit:
    Name of the group that needs to be edited.

    :param main_window:
    Main window class.

    :param cursor:
    Database cursor.

    :param connection:
    Database connection.
    """
    # Only edit if not recycle bin.
    if group_to_edit is not None and group_to_edit != "Recycle Bin":
        text, submit = QInputDialog.getText(main_window,
                                            "Edit a group", "Edit group name",
                                            QLineEdit.Normal,
                                            group_to_edit)

        # Query checks if exact name already exists.
        cursor.execute("SELECT groupName FROM groups WHERE groupName = (?)", [text])
        groups = cursor.fetchall()

        # If text is not empty.
        if submit and text != '' and groups == []:
            sql_group_update = """UPDATE groups SET groupName = (?) WHERE groupName = (?)"""
            edit_group_name = [text, group_to_edit]
            database.database_query(connection, sql_group_update, edit_group_name)
            connection.commit()
            main_window.reload_database()
            return True


def delete_group(delete_group_location, group_to_delete, main_window,
                 list_widget, connection, action_button=False):
    """
    Delete a group.

    :param delete_group_location:
    :param group_to_delete:
    :param main_window:
    :param list_widget:
    :param connection:
    :param action_button:
    :return:
    """
    # Message box asking if user really wants to delete group.
    reply = QMessageBox.question(main_window, "Remove a group",
                                 "Do you really want to remove the group " +
                                 str(group_to_delete) +
                                 "?", QMessageBox.Yes | QMessageBox.No)

    # Delete group if not recycle bin and if user clicked yes.
    if reply == QMessageBox.Yes and group_to_delete != "Recycle Bin":
        # If user triggered method from taskbar.
        if action_button:
            row = list_widget.row(list_widget.item(delete_group_location - 1))
            list_widget.takeItem(row)
        else:
            row = list_widget.row(delete_group_location)
            list_widget.takeItem(row)

        # Delete group from database.
        sql_group_delete = """DELETE FROM groups WHERE groupName = (?)"""
        delete_group_name = [group_to_delete]
        database.database_query(connection, sql_group_delete, delete_group_name)
        connection.commit()
        return True
