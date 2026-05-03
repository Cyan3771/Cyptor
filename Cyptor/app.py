from textual.app import App
from ui.screens.home import HomeScreen
from core.config import VERSION, loadConfig, DEFAULT_CONFIG
from core.i18n import loadI18n, LocaleNode
from core.debug import CannotReadConfigError, CannotWriteConfigError, CannotReadLocaleError, CannotInitConfigError


class CyptorApp(App):
    """Cyptor应用"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 加载配置和国际化资源
        try:
            self.config = loadConfig()
        except CannotReadConfigError as e:
            self.notify("Error while loading config file, using default config: \n" +
                        str(e), severity="error")
            self.config = DEFAULT_CONFIG
        except CannotInitConfigError as e:
            self.notify("Error while initializing config file: \n" +
                        str(e), severity="error")
            self.config = DEFAULT_CONFIG
        except Exception as e:
            self.notify("Unknown error while loading config file, using default config: \n" +
                        str(e), severity="error")
            self.config = DEFAULT_CONFIG
        try:
            self.i18n = loadI18n(self.config.get("language", "zh-CN"))
        except CannotReadLocaleError as e:
            self.notify("Error while loading locale file: \n" +
                        str(e), severity="error")
            self.i18n = LocaleNode({})
        except Exception as e:
            self.notify("Unknown error while loading locale file: \n" +
                        str(e), severity="error")
            self.i18n = LocaleNode({})

        self.title = self.i18n.common.app.title.format(VERSION)
        self.bind("q", "quit", description=self.i18n.common.quit)

    def on_mount(self) -> None:
        """应用启动时的回调函数"""
        self.push_screen(HomeScreen())


if __name__ == "__main__":
    app = CyptorApp()
    app.run()
