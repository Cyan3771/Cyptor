from pathlib import Path
from app import CyptorApp

PROJECT_ROOT = Path(__file__).resolve()


def main():
    app = CyptorApp()
    app.run()


if __name__ == "__main__":
    main()
