from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label, Input, Static
from textual.containers import Grid, Horizontal, Center
from textual.screen import Screen
from config import VERSION
# from .l18n import *


class BaseButton(Button):
    """按钮基类"""
    CSS = """
    Button:hover {
        background: cyan;
    }
    Button:focus {
        background: #088;
    }
    """


class BaseScreen(Screen):
    """屏幕基类"""
    # 定义CSS样式
    CSS = """
    .Dock {
        background: #088;
    }
    """
    # 标题
    TITLE = f"Cyptor by Cyan3771 version {VERSION}"

    # 定义组件
    def compose(self) -> ComposeResult:
        yield Header(classes="Dock")

        yield Footer(show_command_palette=False, classes="Dock")


class HomeScreen(BaseScreen):
    """主屏幕"""


class CyptorApp(App):
    """Cyptor应用"""

    # 标题
    TITLE = f"Cyptor by Cyan3771 version {VERSION}"

    # 定义快捷键
    BINDINGS = [
        ("ctrl+q", "quit", "退出")
    ]

    def on_mount(self) -> None:
        """应用启动时的回调函数"""

        self.push_screen(HomeScreen())


if __name__ == "__main__":
    app = CyptorApp()
    app.run()
