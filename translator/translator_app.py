"""
翻译器应用模块
包含主窗口和UI逻辑
"""

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from translator.config import (
    APP_HEIGHT,
    APP_MIN_HEIGHT,
    APP_MIN_WIDTH,
    APP_TITLE,
    APP_WIDTH,
    LANGUAGES,
    MAX_INPUT_LENGTH,
    TEXT_CLEAR,
    TEXT_COPIED,
    TEXT_COPY_TOOLTIP,
    TEXT_EMPTY_INPUT,
    TEXT_INPUT,
    TEXT_INPUT_LENGTH_INFO,
    TEXT_INPUT_LENGTH_WARNING,
    TEXT_INPUT_PLACEHOLDER,
    TEXT_INPUT_TOO_LONG,
    TEXT_OUTPUT,
    TEXT_OUTPUT_PLACEHOLDER,
    TEXT_PREPARING,
    TEXT_PROGRESS,
    TEXT_READY,
    TEXT_SOURCE_LANG,
    TEXT_TARGET_LANG,
    TEXT_THEME_TOOLTIP,
    TEXT_TRANSLATE,
    TEXT_TRANSLATING,
    TEXT_TRANSLATION_COMPLETE,
    TEXT_TRANSLATION_FAILED,
    TEXT_WARNING,
)
from translator.themes import apply_dark_theme, apply_light_theme
from translator.translation_thread import TranslationThread


# 自定义ComboBox类，强制下拉菜单始终向下展开
class DownComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置下拉菜单的基本属性
        self.setMaxVisibleItems(5)  # 最多显示5个选项
        self.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

    def showPopup(self):
        from PyQt6.QtCore import QTimer

        # 调用父类方法显示下拉菜单
        super().showPopup()

        # 使用定时器延迟调整位置，确保下拉菜单已经完全创建
        QTimer.singleShot(0, self._adjust_popup_position)

    def _adjust_popup_position(self):
        """调整下拉菜单位置，确保始终在ComboBox下方显示"""
        popup = self.view()
        if not popup:
            return

        # 获取下拉菜单的容器窗口
        popup_window = popup.window()
        if not popup_window:
            return

        # 获取当前ComboBox在屏幕上的位置和尺寸
        global_pos = self.mapToGlobal(QPoint(0, 0))
        combo_height = self.height()
        combo_width = self.width()

        # 计算下拉菜单应该显示的位置（在ComboBox下方）
        popup_x = global_pos.x()
        popup_y = global_pos.y() + combo_height

        # 获取下拉菜单的当前尺寸
        popup_width = max(popup_window.width(), combo_width)
        popup_height = popup_window.height()

        # 强制设置下拉菜单的位置
        popup_window.move(popup_x, popup_y)
        popup_window.resize(popup_width, popup_height)


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

        # 设置窗口图标
        try:
            import os

            logo_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "ui", "logo.png"
            )
            if os.path.exists(logo_path):
                self.setWindowIcon(QIcon(logo_path))
        except Exception as e:
            print(f"无法加载logo: {e}")

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
        # 使用自定义的DownComboBox类，强制下拉菜单始终向下展开
        self.source_lang_combo = DownComboBox()
        for lang, code in LANGUAGES.items():
            self.source_lang_combo.addItem(f"{lang} ({code})")
        # 设置默认源语言为英文
        self.source_lang_combo.setCurrentText("英文 (en)")
        source_lang_layout.addWidget(self.source_lang_label)
        source_lang_layout.addWidget(self.source_lang_combo)
        source_lang_layout.addStretch(1)
        left_layout.addLayout(source_lang_layout)

        # 输入文本区域
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(TEXT_INPUT_PLACEHOLDER)
        self.input_text.textChanged.connect(self.update_character_count)
        left_layout.addWidget(self.input_text)

        # 字符计数标签
        self.char_count_label = QLabel(TEXT_INPUT_LENGTH_INFO.format(0))
        self.char_count_label.setStyleSheet("color: gray; font-size: 10px;")
        left_layout.addWidget(self.char_count_label)

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
        # 使用自定义的DownComboBox类，强制下拉菜单始终向下展开
        self.target_lang_combo = DownComboBox()
        # 默认目标语言与源语言不同
        for lang, code in LANGUAGES.items():
            self.target_lang_combo.addItem(f"{lang} ({code})")
        # 设置默认目标语言为中文
        self.target_lang_combo.setCurrentText("中文 (zh)")
        target_lang_layout.addWidget(self.target_lang_label)
        target_lang_layout.addWidget(self.target_lang_combo)
        target_lang_layout.addStretch(1)
        right_layout.addLayout(target_lang_layout)

        # 输出文本区域和复制按钮的容器
        output_container = QWidget()
        output_container_layout = QVBoxLayout(output_container)
        output_container_layout.setContentsMargins(0, 0, 0, 0)

        # 输出文本区域
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText(TEXT_OUTPUT_PLACEHOLDER)
        output_container_layout.addWidget(self.output_text)

        # 复制按钮 - 放在右下角
        copy_button_layout = QHBoxLayout()
        copy_button_layout.addStretch(1)

        self.copy_button = QToolButton()
        self.copy_button.setToolTip(TEXT_COPY_TOOLTIP)
        self.copy_button.setText("📋")  # 使用剪贴板图标
        self.copy_button.setFixedSize(28, 28)
        self.copy_button.setObjectName("copyButton")  # 设置对象名，用于特定样式
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        self.copy_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )  # 鼠标悬停时显示手型光标
        copy_button_layout.addWidget(self.copy_button)

        output_container_layout.addLayout(copy_button_layout)
        right_layout.addWidget(output_container)

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

    def update_character_count(self):
        """更新字符计数显示"""
        text = self.input_text.toPlainText()
        char_count = len(text)

        # 更新字符计数标签
        self.char_count_label.setText(TEXT_INPUT_LENGTH_INFO.format(char_count))

        # 根据字符数量改变标签颜色
        if char_count > MAX_INPUT_LENGTH:
            self.char_count_label.setStyleSheet(
                "color: red; font-size: 10px; font-weight: bold;"
            )
        elif char_count > MAX_INPUT_LENGTH * 0.8:  # 80%时显示警告色
            self.char_count_label.setStyleSheet("color: orange; font-size: 10px;")
        else:
            self.char_count_label.setStyleSheet("color: gray; font-size: 10px;")

    def start_translation(self):
        # 获取输入文本
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, TEXT_WARNING, TEXT_EMPTY_INPUT)
            return

        # 检查文本长度
        if len(text) > MAX_INPUT_LENGTH:
            reply = QMessageBox.question(
                self,
                TEXT_INPUT_TOO_LONG,
                TEXT_INPUT_LENGTH_WARNING + "\n\n是否继续翻译？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes,
            )
            if reply == QMessageBox.StandardButton.No:
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
        from PyQt6.QtWidgets import QApplication

        self.is_dark_theme = not self.is_dark_theme

        # 根据当前主题状态应用相应的主题
        if self.is_dark_theme:
            apply_dark_theme(QApplication.instance())  # 应用到QApplication实例
            self.theme_button.setText("🌞")  # 太阳图标表示可以切换到亮色主题
        else:
            apply_light_theme(QApplication.instance())  # 应用到QApplication实例
            self.theme_button.setText("🌓")  # 月亮图标表示可以切换到暗色主题

    def copy_to_clipboard(self):
        """复制翻译结果到剪贴板"""
        text = self.output_text.toPlainText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

            # 临时更改状态标签，显示已复制信息
            original_status = self.status_label.text()
            self.status_label.setText(TEXT_COPIED)

            # 使用计时器在1.5秒后恢复原始状态
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(1500, lambda: self.status_label.setText(original_status))
