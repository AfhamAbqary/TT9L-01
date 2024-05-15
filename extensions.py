from pocketbase import PocketBase
from flask_simple_crypt import SimpleCrypt
import os
from dotenv import load_dotenv
import hashlib

#Pocketbase side
client = PocketBase('https://alma-mater.pockethost.io')

#Encrypt, decrypt & storage side
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

cipher = SimpleCrypt()
