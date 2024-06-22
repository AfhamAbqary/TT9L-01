from pocketbase import PocketBase
from pocketbase.client import FileUpload
from flask_simple_crypt import SimpleCrypt
import os
from dotenv import load_dotenv
from flask_ckeditor import CKEditor
import random

#Forms class
ckeditor = CKEditor()


#Pocketbase side
client = PocketBase('https://alma-mater.pockethost.io')

#Initialise libraries

#Encrypt, decrypt & storage side
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

cipher = SimpleCrypt()
