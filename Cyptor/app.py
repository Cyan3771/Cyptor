from textual.app import App
from ui.screens.home import HomeScreen
from core.config import VERSION
# from .l18n import *


class CyptorApp(App):
    """Cyptor应用"""

    # 标题
    TITLE = "Cyptor by Cyan3771 version {}".format(VERSION)

    # 定义快捷键
    BINDINGS = [
        ("q", "quit", "退出")
    ]

    def on_mount(self) -> None:
        """应用启动时的回调函数"""

        self.push_screen(HomeScreen())


if __name__ == "__main__":
    app = CyptorApp()
    app.run()
