from textual.app import ComposeResult
from textual.widgets import Button, Label, Input, Select, Static
from textual.containers import Center, Vertical, Horizontal
from ui.screens.base import BaseScreen
from core.crypto.manager import CryptoManager
from textual_fspicker import FileOpen


class EncryptionScreen(BaseScreen):
    """加密屏幕"""
    BINDINGS = [("escape", "back")]

    CSS = BaseScreen.CSS + """
    #encryption-container {
        align: center top;
        overflow-y: auto;
        overflow-x: hidden;

        scrollbar-background: #004444;
        scrollbar-color: #006666;
    }
    #file-chooser-container {
        margin-top: 2;
        width: 80%;
    }
    #file-input {
        width: 1fr;
    }
    #file-button{
        border: none;
        padding: 0 0;
        width: 3;
        min-width: 3;
        height: 1;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from app import CyptorApp
        self.app: CyptorApp
        app = self.app

        self.i18n = app.i18n
        self.title = self.i18n.encryption.title

    # 定义组件
    def compose(self) -> ComposeResult:
        yield from super().compose()

        with Vertical(id="encryption-container"):
            with Horizontal(id="file-chooser-container"):
                yield Label(self.i18n.common.file.select, id="file-label")
                yield Input(id="file-input")
                yield Button(label="📄", tooltip=self.i18n.common.file.button.tooltip, id="file-button")

    # 按钮点击事件
    def on_button_pressed(self, event):
        if event.button.id == "file-button":
            self.app.push_screen(
                FileOpen(".", title=self.i18n.common.file.select),
                callback=self._file_chosen,
            )

    # 文件选择回调
    def _file_chosen(self, chosen):
        if chosen is None:
            return
        fileInput = self.query_one("#file-input", Input)  # 获取输入框组件
        fileInput.value = str(chosen)

    def action_back(self) -> None:
        """返回上一页"""

        self.app.pop_screen()
