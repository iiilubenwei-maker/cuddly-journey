"""6张图的提示词模板。

你后面可以把最终提示词填到这 6 个函数里。
现在函数先保持空模板，程序会在函数返回空字符串时使用 image_generator.py 里的基础兜底提示词，保证项目能直接运行。
"""


def hero_prompt(product: dict) -> str:
    return ""


def size_prompt(product: dict) -> str:
    return ""


def detail_prompt(product: dict) -> str:
    return ""


def build_prompt(product: dict) -> str:
    return ""


def mood_prompt(product: dict) -> str:
    return ""


def display_prompt(product: dict) -> str:
    return ""
