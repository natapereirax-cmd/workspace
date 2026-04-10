from PySide6.QtWidgets import (
    QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QFontDatabase
from app.backend.users import get_user, hash_password, email_exists
from app.menu_index import MainWindow
from app.login_style import style
from app.backend.service import create_user
import re


class LogIn(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(style())
        self.setFixedSize(450, 550)
        self.setWindowTitle('LogIn')

        self.setWindowIcon(QIcon('desktop_app/app/images/workspace_icon.png'))

        font_id_1 = QFontDatabase.addApplicationFont('desktop_app/app/fonts/BebasNeue-Regular.ttf')
        font_id_2 = QFontDatabase.addApplicationFont('desktop_app/app/fonts/CaviarDreams.ttf')

        bg_img = QLabel(self)
        bg_img.setPixmap(QPixmap('desktop_app/app/images/login_bg.png'))
        bg_img.setScaledContents(True)
        bg_img.setGeometry(0, 0, self.width(), self.height())
        bg_img.lower()

        self.email = QLineEdit()
        self.email.setPlaceholderText('email')
        self.email.addAction(QIcon('desktop_app/app/images/user_icon.png'), QLineEdit.LeadingPosition)

        self.password = QLineEdit()
        self.password.setPlaceholderText('password')
        self.password.setEchoMode(QLineEdit.Password)
        self.password.addAction(QIcon('desktop_app/app/images/password_icon.png'), QLineEdit.LeadingPosition)

        self.warning_text  = QLabel('')
        self.warning_text.setObjectName('warning_text')

        login_btn = QPushButton('Log In')
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setObjectName('login')
        login_btn.clicked.connect(self.pressed_login)

        msg = QLabel("Don't have an account?")

        signup_btn = QPushButton('Sign Up')
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.setObjectName('signup')
        signup_btn.clicked.connect(self.signup_screen)

        layout = QVBoxLayout()
        layout.setContentsMargins(80, 250, 80, 20)
        layout.addWidget(self.email)
        layout.addSpacing(10)
        layout.addWidget(self.password)
        layout.addSpacing(10)
        layout.addWidget(login_btn)
        layout.addWidget(self.warning_text, alignment=Qt.AlignCenter)
        layout.addSpacing(10)
        layout.addWidget(msg, alignment=Qt.AlignCenter)
        layout.addWidget(signup_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
    
    def pressed_login(self):
        email = self.email.text().strip()
        password = self.password.text().strip()

        if not email or not password:
            self.warning_text.setText('Fill all fields above')
            self.warning_text.setStyleSheet('color: #FD2E2E')
            return

        user = get_user(email)

        if not user:
            self.warning_text.setText('Invalid Credentials!')
            self.warning_text.setStyleSheet('color: #FD2E2E')
            return

        salt = user['salt']
        stored_hash = user['password']

        input_hash = hash_password(password, salt)

        if input_hash == stored_hash:
            self.warning_text.setText('Welcome!')
            self.warning_text.setStyleSheet('color: #53FF4D')

            self.menu = MainWindow(user)
            self.menu.show()

            self.close()
        else:
            self.warning_text.setText('Invalid Credentials!')
            self.warning_text.setStyleSheet('color: #FD2E2E')
    
    def signup_screen(self):
        dialog = Signup()
        dialog.exec_()

class Signup(QDialog):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(style())
        self.setFixedSize(450, 500)
        self.setWindowTitle('SignUp')

        self.setWindowIcon(QIcon('desktop_app/app/images/workspace_icon.png'))

        bg_img = QLabel(self)
        bg_img.setPixmap(QPixmap('desktop_app/app/images/signup_bg.png'))
        bg_img.setScaledContents(True)
        bg_img.setGeometry(0, 0, self.width(), self.height())
        bg_img.lower()

        self.setObjectName('sign_up')

        self.firstname = QLineEdit()
        self.firstname.setPlaceholderText('First Name')

        self.lastname = QLineEdit()
        self.lastname.setPlaceholderText('Last Name')

        self.username = QLineEdit()
        self.username.setPlaceholderText('Username')

        self.email = QLineEdit()
        self.email.setPlaceholderText('Email')

        self.password = QLineEdit()
        self.password.setPlaceholderText('Password')
        self.password.setEchoMode(QLineEdit.Password)

        signup_btn = QPushButton('Sign Up')
        signup_btn.setObjectName('signup_2')
        signup_btn.setCursor(Qt.PointingHandCursor)
        signup_btn.clicked.connect(self.pressed_signup)

        self.warning_txt = QLabel('')

        name_layout = QHBoxLayout()
        name_layout.addWidget(self.firstname)
        name_layout.addWidget(self.lastname)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(60, 200, 60, 20)
        layout.addLayout(name_layout)
        layout.addSpacing(5)
        layout.addWidget(self.username)
        layout.addSpacing(5)
        layout.addWidget(self.email)
        layout.addSpacing(5)
        layout.addWidget(self.password)
        layout.addSpacing(20)
        layout.addWidget(self.warning_txt)
        layout.addWidget(signup_btn)
        layout.addSpacing(20)

    def pressed_signup(self):
        firstname = self.firstname.text().strip()
        lastname = self.lastname.text().strip()
        username = self.username.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()

        if not all ([firstname, lastname, username, email, password]):
            self.warning_txt.setText('Fill All Fields!')
            self.warning_txt.setStyleSheet('color: #FD2E2E;')
            return
        
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', firstname) or not re.match(r'^[A-Za-zÀ-ÿ\s]+$', lastname):
            self.warning_txt.setText('Names Cannot Contain\nNumbers Or symbols!')
            self.warning_txt.setStyleSheet('color: #FD2E2E;')
            return
        
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            self.warning_txt.setText('Valid Email')
            self.warning_txt.setStyleSheet('color: #53FF4D;')
        else:
            self.warning_txt.setText('Invalid Email Format!')
            self.warning_txt.setStyleSheet('color: #FD2E2E;')
            return

        exists = email_exists(email)

        if exists:
            self.warning_txt.setText('This Email Already Has An Account!')
            self.warning_txt.setStyleSheet('color: #FD2E2E;')
            return
        

        if (
            len(password) >= 4 and
            len(password) <= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[^A-Za-z0-9]', password)
        ):
            self.warning_txt.setText('Valid Password')
            self.warning_txt.setStyleSheet('color: #53FF4D;')
        else:
            self.warning_txt.setText("Your Password Is Too Weak!\nYour PassWord Can't Exceed 8 Characters")
            self.warning_txt.setStyleSheet('color: #FD2E2E;')
            return
        
        create_user(firstname, lastname, username, email, password)
        self.warning_txt.setText('Account Created')
        self.warning_txt.setStyleSheet('color: #53FF4D;')

        
