from pocketbase import PocketBase
from flask_simple_crypt import SimpleCrypt
import os
from dotenv import load_dotenv
from flask_ckeditor import CKEditor

#Forms class
ckeditor = CKEditor()


#Pocketbase side
client = PocketBase('https://alma-mater.pockethost.io')
#client = PocketBase('http://pocketbase-fs8csgg.37.27.31.99.sslip.io')

#Initialise libraries

#Encrypt, decrypt & storage side
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

cipher = SimpleCrypt()
