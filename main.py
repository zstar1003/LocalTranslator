"""
AI 智能翻译器主入口文件
支持中文、英文、俄文之间的互译
"""

import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from translator.config import DEFAULT_FONT, DEFAULT_FONT_SIZE
from translator.themes import apply_light_theme
from translator.translator_app import TranslatorApp


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 设置全局字体
    font = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
    app.setFont(font)

    translator = TranslatorApp()

    # 默认应用亮色主题
    apply_light_theme(app)
    translator.theme_button.setText("🌓")  # 月亮图标表示可以切换到暗色主题

    translator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
