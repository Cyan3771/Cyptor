from textual.app import App
from ui.screens.home import HomeScreen
from core.config import VERSION, loadConfig
from core.i18n import loadI18n


class CyptorApp(App):
    """Cyptor应用"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 加载配置和国际化资源
        self.config = loadConfig()
        self.i18n = loadI18n(self.config.get("language", "zh-CN"))

        self.title = self.i18n.app.title.format(VERSION)
        self.bind("q", "quit", description=self.i18n.quit)

    def on_mount(self) -> None:
        """应用启动时的回调函数"""
        self.push_screen(HomeScreen())


if __name__ == "__main__":
    app = CyptorApp()
    app.run()
