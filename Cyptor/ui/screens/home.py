from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Center, Vertical
from ui.screens.base import BaseScreen


class HomeScreen(BaseScreen):
    """主屏幕"""

    # 定义CSS样式
    CSS = BaseScreen.CSS + """
    #welcome-label {
        text-align: center;
        text-style: bold;
        margin: 1;
    }
    .btn {
        width: 40;
        margin: 1;
    }
    #home-container {
        align: center middle;
        overflow-y: auto;    /* 滚动条 */
        overflow-x: hidden;

        scrollbar-background: #004444;
        scrollbar-color: #006666;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from app import CyptorApp
        self.app: CyptorApp
        app = self.app

        self.i18n = app.i18n

    # 定义组件

    def compose(self) -> ComposeResult:
        # 调用父类的compose方法
        yield from super().compose()

        # 主屏幕组件
        WelcomeLabel = Center(
            Label(self.i18n.home.welcome, id="welcome-label"))
        EncryptionBtn = Button(
            self.i18n.home.buttons.encrypt, id="encryption", classes="btn")
        DecryptionBtn = Button(
            self.i18n.home.buttons.decrypt, id="decryption", classes="btn")
        SettingsBtn = Button(self.i18n.home.buttons.settings,
                             id="settings", classes="btn")
        AboutBtn = Button(self.i18n.home.buttons.about,
                          id="about", classes="btn")

        ButtonsGroup = Center(
            EncryptionBtn, DecryptionBtn, SettingsBtn, AboutBtn)

        yield Vertical(
            WelcomeLabel,
            ButtonsGroup,
            id="home-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        button_id = event.button.id
        if button_id == "encryption":
            from ui.screens.encryption import EncryptionScreen
            self.app.push_screen(EncryptionScreen())
        """elif button_id == "decryption":
            from ui.screens.decryption import DecryptionScreen
            self.app.push_screen(DecryptionScreen())
        elif button_id == "settings":
            from ui.screens.settings import SettingsScreen
            self.app.push_screen(SettingsScreen())
        elif button_id == "about":
            from ui.screens.about import AboutScreen
            self.app.push_screen(AboutScreen())
"""
