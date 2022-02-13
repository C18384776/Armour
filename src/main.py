import sys

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction

from ui_main import *


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        self.ui.listWidget_groups.installEventFilter(self)

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
