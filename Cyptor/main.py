import os
from app import CyptorApp

os.chdir(os.path.dirname(os.path.abspath(__file__)))
CyptorApp().run()
