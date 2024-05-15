from pocketbase import PocketBase
from flask_simple_crypt import SimpleCrypt
import os
from dotenv import load_dotenv

#Pocketbase side
client = PocketBase('https://alma-mater.pockethost.io')

#Initialise libraries

#Encrypt, decrypt & storage side
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

cipher = SimpleCrypt()
