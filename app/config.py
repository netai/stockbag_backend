import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'GR238jh$hdjsl&#jakdg4k&hd73hjd')