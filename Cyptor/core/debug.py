import traceback


def get_full_error(exc: Exception) -> str:
    """获取完整的错误信息"""
    return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
