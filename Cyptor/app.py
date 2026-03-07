from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Label, Input, Static
from textual.containers import Grid, Horizontal, Center
from textual.screen import Screen
# from .l18n import *


class HomeScreen(Screen):
    """应用首页面"""

    # CSS样式
    CSS = """
    #mainContent {
        height: 100%;
        grid-size: 1 3;  /* 3行1列 */
        grid-rows: 1fr 1 1fr;  
    }
    .airPlace {
        background: cyan;
        height: 1fr;  /* 占满网格单元的高度 */
    }
    #chooseFileRow {
        width: 80%; /* 顶部外边距 */
    }
    #chooseFileRow Input {
        border: none; /* 移除边框 */
        height: 1;
        width: 1fr;
        padding: 0 0; /* 移除内边距 */
    }
    #chooseFileRow Button {
        height: 1;
        width: 3;
        border: none;
        padding: 0 0;
        min-width: 0;
    }
    """
    # 定义组件

    def compose(self) -> ComposeResult:
        yield Header()
        yield Grid(
            Static("", classes="airPlace"),
            Center(
                Horizontal(
                    Label("文件 "),
                    Input(placeholder="请输入文件路径"),
                    Button("📄"),
                    id="chooseFileRow"),
            ),
            Static("", classes="airPlace"),
            id="mainContent"
        )

        yield Footer()
        pass


class CyptorApp(App):
    """Cyptor应用"""

    TITLE = "Cyptor by Cyan3771"

    def on_mount(self) -> None:
        """应用启动时的回调函数"""

        self.push_screen(HomeScreen())


if __name__ == "__main__":
    app = CyptorApp()
    app.run()
