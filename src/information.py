from PyQt5.QtWidgets import QMessageBox

# This file contains the help messages for users.


def directory_edit_registration_moment():
    message = QMessageBox()
    message.setWindowTitle("Save Location Help")
    message.setText("""This field represents the place where the the database file will be kept.\n
    Please remember the place where this database file will be stored as you'll need it to login.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def password_registration_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Master Password Help")
    message.setText("""The master password is the password that will be used to unlock the database file\n
    This password should be memorable and long.\n
    Try to use random words instead of random characters as they are easier to remember and more secure\n
    An example of a secure password is "reimburse growing abdominal apprehend founding graduate".\n
    Do not forget this password as it is used to unlock your password database.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def password_strength_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Strength Help")
    message.setText("""Password strength represents a bar that tells you how un-hackable your password is.\n
    The higher the number of bits your password has, the stronger your password is.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def secret_file_registration_moment():
    message = QMessageBox()
    message.setWindowTitle("Secret File Help")
    message.setText("""This option is for expert users.\n
    This option acts as a second password in addition to the master password which is used to unlock the database.\n
    The person should choose a file that they want to use as a password such as a picture and choose it using the "browse" menu.\n
    Do not lose this file as losing it will mean you will not be able to access the database.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def directory_edit_login_moment():
    message = QMessageBox()
    message.setWindowTitle("Database File Help")
    message.setText("""This field represents the place where you saved the database file.\n
    Please select it by clicking the "browse" button.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def password_login_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Master Password Help")
    message.setText("""This field is where you put the password you set back when you registered the database.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def secret_file_login_moment():
    message = QMessageBox()
    message.setWindowTitle("Secret File Help")
    message.setText("""This field is where you select the secret file you chose to be used as an additional password.\n
    Click "browse" to select it.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def entry_website_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Website Entry Help")
    message.setText("""This field is for the websites name that your password is associated with.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def entry_username_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Username Entry Help")
    message.setText("""This field is for the username for the application that your password is associated with.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def entry_password_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Entry Help")
    message.setText("""This field is for the password for the application that your registering to.\n
    Use the "Generator" button to open a password generator that will make you a strong unique password.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def entry_url_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password URL Entry Help")
    message.setText("""This field is for the "URL" or address of the website your password is associated with. 
    For example: "twitter.com".""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def entry_twofa_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Two Factor Authentication Entry Help")
    message.setText("""This field is for the second factor authentication (2FA) of the website you registered to.\n
    These codes act as an additional password to the password you are already providing a website with.\n
    Oftentimes, a website will give you an option to perform "second factor authentication" and give you a long
    list of characters like "JBSWY3DPEHPK3PXP".\n
    Please put that long list of characters into the "2FA" field in the Armour password manager.\n
    From this list of characters, the program will be able to generate you a six digit code that you can then use
    to login with when you right click on a password entry and click "Copy 2FA\"""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def passgen_password_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Entry Help")
    message.setText("""This field is where the random password will appear.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def passgen_strength_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Entry Help")
    message.setText("""This bar represents how strong the generated password is.\n
    The bigger the number of bits the better.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def passgen_length_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Length Entry Help")
    message.setText("""This field allows you to change the desired length of the password.\n
    To change the length of the password you can use the slider or the box with the number. """)
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def passgen_types_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Character Types Help")
    message.setText("""This field allows you to choose what specific character types you want included in the password.\n
    The choices are letters a to z in lower and upper case; numbers 0 to 9 and special characters.\n
    If a user does not choose any box, it is assumed that they want all characters included.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()


def passgen_include_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Entry Include Help")
    message.setText("""This field allows you to choose what specific character types you want included in the password.\n
    The choices are letters a to z in lower and upper case; numbers 0 to 9 and special characters.\n
    If a user does not choose any box, it is assumed that they want all characters included.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()

def passgen_exclude_help_moment():
    message = QMessageBox()
    message.setWindowTitle("Password Entry Exclude Help")
    message.setText("""This field allows you to choose what specific character types you want included in the password.\n
    The choices are letters a to z in lower and upper case; numbers 0 to 9 and special characters.\n
    If a user does not choose any box, it is assumed that they want all characters included.""")
    message.setIcon(QMessageBox.Information)
    message.setStandardButtons(QMessageBox.Ok)
    message.setDefaultButton(QMessageBox.Ok)
    message.exec_()
