"""
翻译器应用模块
包含主窗口和UI逻辑
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtGui import QFont

from translator.config import (
    APP_TITLE,
    APP_WIDTH,
    APP_HEIGHT,
    APP_MIN_WIDTH,
    APP_MIN_HEIGHT,
    LANGUAGES,
    TEXT_READY,
    TEXT_TRANSLATING,
    TEXT_TRANSLATION_COMPLETE,
    TEXT_TRANSLATION_FAILED,
    TEXT_PREPARING,
    TEXT_INPUT_PLACEHOLDER,
    TEXT_OUTPUT_PLACEHOLDER,
    TEXT_WARNING,
    TEXT_EMPTY_INPUT,
    TEXT_PROGRESS,
    TEXT_TRANSLATE,
    TEXT_CLEAR,
    TEXT_INPUT,
    TEXT_OUTPUT,
    TEXT_SOURCE_LANG,
    TEXT_TARGET_LANG,
    TEXT_THEME_TOOLTIP,
)
from translator.themes import apply_dark_theme, apply_light_theme
from translator.translation_thread import TranslationThread


class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = False  # 默认使用亮色主题
        self.initUI()
        self.translation_thread = None

    def initUI(self):
        # 设置窗口
        self.setWindowTitle(APP_TITLE)
        self.setGeometry(100, 100, APP_WIDTH, APP_HEIGHT)
        self.setMinimumSize(APP_MIN_WIDTH, APP_MIN_HEIGHT)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局 - 垂直布局，包含上部的左右布局和下部的进度条
        main_layout = QVBoxLayout(central_widget)

        # 创建左右布局
        content_layout = QHBoxLayout()
        content_layout.setSpacing(5)  # 减小左右容器之间的间距

        # 左侧布局 - 输入区域
        left_group = QGroupBox(TEXT_INPUT)
        left_layout = QVBoxLayout(left_group)

        # 源语言选择
        source_lang_layout = QHBoxLayout()
        self.source_lang_label = QLabel(TEXT_SOURCE_LANG)
        self.source_lang_combo = QComboBox()
        for lang, code in LANGUAGES.items():
            self.source_lang_combo.addItem(f"{lang} ({code})")
        source_lang_layout.addWidget(self.source_lang_label)
        source_lang_layout.addWidget(self.source_lang_combo)
        source_lang_layout.addStretch(1)
        left_layout.addLayout(source_lang_layout)

        # 输入文本区域
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(TEXT_INPUT_PLACEHOLDER)
        left_layout.addWidget(self.input_text)

        # 添加左侧布局到内容布局
        content_layout.addWidget(left_group)

        # 中间控制按钮区域 - 减小间距
        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(5)  # 减小垂直间距
        middle_layout.setContentsMargins(2, 2, 2, 2)  # 减小边距
        middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 垂直居中对齐

        # 主题切换按钮 - 放在最上方
        self.theme_button = QPushButton()
        self.theme_button.setFixedSize(28, 28)  # 减小尺寸
        self.theme_button.setToolTip(TEXT_THEME_TOOLTIP)
        self.theme_button.setObjectName("themeButton")  # 设置对象名，用于特定样式
        # 使用文本作为图标
        self.theme_button.setText("🌓")
        self.theme_button.clicked.connect(self.toggle_theme)

        # 添加主题按钮到中间布局
        theme_button_layout = QHBoxLayout()
        theme_button_layout.addWidget(
            self.theme_button, 0, Qt.AlignmentFlag.AlignCenter
        )
        middle_layout.addLayout(theme_button_layout)

        # 添加垂直弹性空间，使按钮垂直居中
        middle_layout.addStretch(1)

        # 翻译按钮
        self.translate_button = QPushButton(TEXT_TRANSLATE)
        self.translate_button.setFixedWidth(80)  # 减小宽度
        self.translate_button.setFixedHeight(32)  # 减小高度
        self.translate_button.clicked.connect(self.start_translation)
        middle_layout.addWidget(self.translate_button, 0, Qt.AlignmentFlag.AlignCenter)

        # 清除按钮
        self.clear_button = QPushButton(TEXT_CLEAR)
        self.clear_button.setFixedWidth(80)  # 减小宽度
        self.clear_button.setFixedHeight(32)  # 减小高度
        self.clear_button.clicked.connect(self.clear_text)
        middle_layout.addWidget(self.clear_button, 0, Qt.AlignmentFlag.AlignCenter)

        # 添加垂直弹性空间，使按钮垂直居中
        middle_layout.addStretch(1)
        content_layout.addLayout(middle_layout)

        # 右侧布局 - 输出区域
        right_group = QGroupBox(TEXT_OUTPUT)
        right_layout = QVBoxLayout(right_group)

        # 目标语言选择
        target_lang_layout = QHBoxLayout()
        self.target_lang_label = QLabel(TEXT_TARGET_LANG)
        self.target_lang_combo = QComboBox()
        # 默认目标语言与源语言不同
        for lang, code in LANGUAGES.items():
            self.target_lang_combo.addItem(f"{lang} ({code})")
        target_lang_layout.addWidget(self.target_lang_label)
        target_lang_layout.addWidget(self.target_lang_combo)
        target_lang_layout.addStretch(1)
        right_layout.addLayout(target_lang_layout)

        # 输出文本区域
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText(TEXT_OUTPUT_PLACEHOLDER)
        right_layout.addWidget(self.output_text)

        # 添加右侧布局到内容布局
        content_layout.addWidget(right_group)

        # 添加内容布局到主布局
        main_layout.addLayout(content_layout)

        # 进度条和状态信息放在最下面
        status_layout = QHBoxLayout()

        # 添加状态标签
        self.status_label = QLabel(TEXT_READY)
        status_layout.addWidget(self.status_label)

        status_layout.addStretch(1)

        # 进度条
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel(TEXT_PROGRESS))

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(200)
        progress_layout.addWidget(self.progress_bar)

        status_layout.addLayout(progress_layout)

        main_layout.addLayout(status_layout)

    def start_translation(self):
        # 获取输入文本
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, TEXT_WARNING, TEXT_EMPTY_INPUT)
            return

        # 获取目标语言代码
        target_lang = self.target_lang_combo.currentText().split("(")[1].strip(")")

        # 更新状态
        self.status_label.setText(TEXT_PREPARING)

        # 禁用翻译按钮，避免重复点击
        self.translate_button.setEnabled(False)
        self.progress_bar.setValue(0)

        # 创建并启动翻译线程
        self.translation_thread = TranslationThread(text, target_lang)
        self.translation_thread.translation_done.connect(self.update_translation)
        self.translation_thread.progress_update.connect(self.update_progress)
        self.translation_thread.finished.connect(
            lambda: self.translate_button.setEnabled(True)
        )
        self.translation_thread.start()

    def update_translation(self, text):
        self.output_text.setText(text)
        # 更新状态标签
        if text.startswith("翻译出错"):
            self.status_label.setText(TEXT_TRANSLATION_FAILED)
        else:
            self.status_label.setText(TEXT_TRANSLATION_COMPLETE)

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        # 根据进度更新状态标签
        if value == 0:
            self.status_label.setText(TEXT_TRANSLATION_FAILED)
        elif value < 100:
            self.status_label.setText(TEXT_TRANSLATING)
        else:
            self.status_label.setText(TEXT_TRANSLATION_COMPLETE)

    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText(TEXT_READY)

    def toggle_theme(self):
        """切换明暗主题"""
        self.is_dark_theme = not self.is_dark_theme

        # 根据当前主题状态应用相应的主题
        if self.is_dark_theme:
            apply_dark_theme(self.parent().parent())  # 应用到QApplication实例
            self.theme_button.setText("🌞")  # 太阳图标表示可以切换到亮色主题
        else:
            apply_light_theme(self.parent().parent())  # 应用到QApplication实例
            self.theme_button.setText("🌓")  # 月亮图标表示可以切换到暗色主题
