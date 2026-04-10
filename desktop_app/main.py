#CODIGO MAIN PARA RODAR O SOFTWARE

import sys
from PySide6.QtWidgets import QApplication
from app.login_index import LogIn
app = QApplication(sys.argv)

window = LogIn()

window.show()
sys.exit(app.exec())