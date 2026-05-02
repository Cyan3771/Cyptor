from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Center, Vertical
from ui.screens.base import BaseScreen


class EncryptionScreen(BaseScreen):
    """加密屏幕"""
    BINDINGS = [("escape", "back")]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from app import CyptorApp
        self.app: CyptorApp
        app = self.app

        self.i18n = app.i18n
        self.title = self.i18n.encryption.title

    def action_back(self) -> None:
        """返回上一页"""

        self.app.pop_screen()
