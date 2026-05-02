from textual.app import ComposeResult
from textual.widgets import Header, Footer
from textual.screen import Screen
from core.config import VERSION


class BaseScreen(Screen):
    """屏幕基类"""
    # 定义CSS样式
    CSS = """
    .dock {
        background: #008888;
    }
    Button:hover {
        background: #00AAAA;
    }
    Button:focus {
        background: #006666;
    }
    Button {
        border-top: tall #00FFFF;
    }
    
    """
    # 标题
    TITLE = f"Cyptor by Cyan3771 version {VERSION}"

    # 定义组件
    def compose(self) -> ComposeResult:
        yield Header(classes="dock")

        yield Footer(show_command_palette=False, classes="dock")
