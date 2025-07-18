"""
翻译器配置文件
包含常量和配置项
"""

import os

# 应用配置
APP_TITLE = "AI 智能翻译器"
APP_WIDTH = 900
APP_HEIGHT = 500
APP_MIN_WIDTH = 800
APP_MIN_HEIGHT = 450

# 翻译模型配置
MODEL_NAME = "utrobinmv/t5_translate_en_ru_zh_small_1024"
# 本地模型路径
MODEL_PATH = "./models"
USE_LOCAL_MODEL = os.path.exists(MODEL_PATH)

# 支持的语言
LANGUAGES = {"中文": "zh", "英文": "en", "俄文": "ru"}

# 默认字体
DEFAULT_FONT = "Microsoft YaHei UI"
DEFAULT_FONT_SIZE = 10

# 界面文本
TEXT_READY = "就绪"
TEXT_TRANSLATING = "正在翻译..."
TEXT_TRANSLATION_COMPLETE = "翻译完成"
TEXT_TRANSLATION_FAILED = "翻译失败"
TEXT_PREPARING = "准备翻译..."
TEXT_INPUT_PLACEHOLDER = "请在此输入要翻译的文本..."
TEXT_OUTPUT_PLACEHOLDER = "翻译结果将显示在这里..."
TEXT_WARNING = "警告"
TEXT_EMPTY_INPUT = "请输入要翻译的文本!"
TEXT_PROGRESS = "翻译进度:"
TEXT_TRANSLATE = "翻译"
TEXT_CLEAR = "清除"
TEXT_INPUT = "输入"
TEXT_OUTPUT = "翻译结果"
TEXT_SOURCE_LANG = "源语言:"
TEXT_TARGET_LANG = "目标语言:"
TEXT_THEME_TOOLTIP = "切换主题"
TEXT_COPY = "复制"
TEXT_COPY_TOOLTIP = "复制到剪贴板"
TEXT_COPIED = "已复制到剪贴板"
