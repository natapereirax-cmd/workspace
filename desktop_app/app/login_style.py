#ESTILIZAÇÃO DA TELA DE LOGIN E SIGNUP

def style():
    return """
    QLineEdit {
        background-color: #ffffff;
        height: 40px;
        font-family: Caviar Dreams;
        font-size: 20px;
    }
    
    QPushButton#login {
        background-color: transparent;
        color: white;
        border: none;
        border-radius: none;
        font-family: Bebas Neue;
        font-size: 40px;
    }

    QPushButton:hover#login {
        font-size: 50px;
    }

    QLabel {
        font-family: Caviar Dreams;
        font-size: 16px;
        color: white;
    }

    QPushButton#signup {
        font-family: Bebas Neue;
        font-size: 25px;
        background-color: transparent;
        color:#5384e6;
    }

    QPushButton:hover#signup {
        font-size: 30px;
    }

    QPushButton#signup_2 {
        font-family: Bebas Neue;
        font-size: 40px;
        background-color: transparent;
        border: transparent;
        color:#5384e6;
    }

    QPushButton:hover#signup_2 {
        font-size: 50px;
    }

"""