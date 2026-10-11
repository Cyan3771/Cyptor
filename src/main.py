from pathlib import Path
from app import CyptorApp

PROJECT_ROOT = Path(__file__).resolve()

app = CyptorApp()
app.run()
