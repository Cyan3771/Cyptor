LANG = {
    "zh": {
        "LanguageName": "中文",
    }
}


class AttrDict(dict):
    """支持属性式访问的字典类（核心类）"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 遍历所有键值对
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = AttrDict(value)  # 嵌套转换
            # 遍历列表内的字典
            elif isinstance(value, list):
                self[key] = [AttrDict(item) if isinstance(
                    item, dict) else item for item in value]

    def __getattr__(self, name):
        """重写属性获取"""
        return self[name]

    def __setattr__(self, name, value):
        """重写属性赋值"""
        # 处理嵌套赋值（如果值是字典，自动转 AttrDict）
        if isinstance(value, dict):
            value = AttrDict(value)
        self[name] = value
