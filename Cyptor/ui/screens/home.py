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

    # 定义组件
    def compose(self) -> ComposeResult:
        # 调用父类的compose方法
        yield from super().compose()

        # 主屏幕组件
        WelcomeLabel = Center(Label("欢迎使用Cyptor！", id="welcome-label"))
        EncryptionBtn = Button("🔒 加密文件", id="encryption", classes="btn")
        DecryptionBtn = Button("🔓 解密文件", id="decryption", classes="btn")
        SettingsBtn = Button("⚙️ 设置", id="settings", classes="btn")
        AboutBtn = Button("ℹ️ 关于", id="about", classes="btn")

        ButtonsGroup = Center(
            EncryptionBtn, DecryptionBtn, SettingsBtn, AboutBtn)

        yield Vertical(
            WelcomeLabel,
            ButtonsGroup,
            id="home-container"
        )
