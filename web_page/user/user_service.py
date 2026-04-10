#HASH DE SENHA PARA FUNCIONAR COM SIGNUP DO SITE E SOFTWARE

import hashlib
import os
from .user_repository import insert_user

def hash_password(password, salt):
    password_bytes = password.encode('utf-8')
    salted_password = password_bytes + salt

    hashed = hashlib.sha256(salted_password).hexdigest()

    return hashed

def create_user(firstname, lastname, username, email, password):
    salt = os.urandom(16)

    hashed_password = hash_password(password, salt)

    insert_user(firstname, lastname, username, email, hashed_password, salt)