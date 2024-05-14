from pocketbase import PocketBase
import os
from dotenv import load_dotenv
import hashlib

#Pocketbase side
client = PocketBase('https://alma-mater.pockethost.io')

#Encrypt, decrypt & storage side
load_dotenv()
HASH_KEY = os.getenv("HASH_KEY")

