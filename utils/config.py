import os
from dotenv import load_dotenv
load_dotenv()

class TgConf:
    token=os.getenv('TOKEN')

class DbConfig:
    HOST=os.getenv('HOST')
    PORT=os.getenv('PORT')
    USER=os.getenv('USeR')
    PASSWORD=os.getenv('PASSWORD')
    DATABASE=os.getenv('DATABASE')

class AdminConfig:
    Admins=os.getenv('ADMINS')



class CF:

    TG=TgConf
    DBC=DbConfig
    Admins=AdminConfig