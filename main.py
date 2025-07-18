import sys

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPalette
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
    QVBoxLayout,
    QWidget,
)
from transformers import T5ForConditionalGeneration, T5Tokenizer


class TranslationThread(QThread):
    """线程类用于执行翻译任务，避免UI卡顿"""

    translation_done = pyqtSignal(str)
    progress_update = pyqtSignal(int)

    def __init__(self, text, target_lang):
        super().__init__()
        self.text = text
        self.target_lang = target_lang

    def run(self):
        try:
            # 更新进度条 - 开始加载模型
            self.progress_update.emit(10)

            # 加载模型和分词器
            model_name = "utrobinmv/t5_translate_en_ru_zh_small_1024"
            model = T5ForConditionalGeneration.from_pretrained(model_name)
            self.progress_update.emit(50)

            tokenizer = T5Tokenizer.from_pretrained(model_name)
            self.progress_update.emit(70)

            # 准备输入
            prefix = f"translate to {self.target_lang}: "
            src_text = prefix + self.text

            # 分词和生成翻译
            input_ids = tokenizer(src_text, return_tensors="pt")
            self.progress_update.emit(80)

            generated_tokens = model.generate(**input_ids)
            self.progress_update.emit(90)

            # 解码结果
            result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            translated_text = result[0] if result else "翻译失败"

            # 发送翻译完成信号
            self.progress_update.emit(100)
            self.translation_done.emit(translated_text)

        except Exception as e:
            self.translation_done.emit(f"翻译出错: {str(e)}")
            self.progress_update.emit(0)


class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = False  # 默认使用亮色主题
        self.initUI()
        self.translation_thread = None

    def initUI(self):
        # 设置窗口
        self.setWindowTitle("AI 智能翻译器")
        self.setGeometry(100, 100, 900, 500)
        self.setMinimumSize(800, 450)  # 设置最小窗口尺寸

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局 - 垂直布局，包含上部的左右布局和下部的进度条
        main_layout = QVBoxLayout(central_widget)

        # 创建左右布局
        content_layout = QHBoxLayout()
        content_layout.setSpacing(5)  # 进一步减小左右容器之间的间距

        # 左侧布局 - 输入区域
        left_group = QGroupBox("输入")
        left_layout = QVBoxLayout(left_group)

        # 源语言选择
        source_lang_layout = QHBoxLayout()
        self.source_lang_label = QLabel("源语言:")
        self.source_lang_combo = QComboBox()
        self.source_lang_combo.addItems(["中文 (zh)", "英文 (en)", "俄文 (ru)"])
        source_lang_layout.addWidget(self.source_lang_label)
        source_lang_layout.addWidget(self.source_lang_combo)
        source_lang_layout.addStretch(1)
        left_layout.addLayout(source_lang_layout)

        # 输入文本区域
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("请在此输入要翻译的文本...")
        left_layout.addWidget(self.input_text)

        # 添加左侧布局到内容布局
        content_layout.addWidget(left_group)

        # 中间控制按钮区域 - 减小间距
        middle_layout = QVBoxLayout()
        middle_layout.setSpacing(5)  # 进一步减小垂直间距
        middle_layout.setContentsMargins(2, 2, 2, 2)  # 进一步减小边距
        middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 垂直居中对齐

        # 主题切换按钮 - 放在最上方
        self.theme_button = QPushButton()
        self.theme_button.setFixedSize(28, 28)  # 进一步减小尺寸
        self.theme_button.setToolTip("切换主题")
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
        self.translate_button = QPushButton("翻译")
        self.translate_button.setFixedWidth(80)  # 进一步减小宽度
        self.translate_button.setFixedHeight(32)  # 进一步减小高度
        self.translate_button.clicked.connect(self.start_translation)
        middle_layout.addWidget(self.translate_button, 0, Qt.AlignmentFlag.AlignCenter)

        # 清除按钮
        self.clear_button = QPushButton("清除")
        self.clear_button.setFixedWidth(80)  # 进一步减小宽度
        self.clear_button.setFixedHeight(32)  # 进一步减小高度
        self.clear_button.clicked.connect(self.clear_text)
        middle_layout.addWidget(self.clear_button, 0, Qt.AlignmentFlag.AlignCenter)

        # 添加垂直弹性空间，使按钮垂直居中
        middle_layout.addStretch(1)
        content_layout.addLayout(middle_layout)

        # 右侧布局 - 输出区域
        right_group = QGroupBox("翻译结果")
        right_layout = QVBoxLayout(right_group)

        # 目标语言选择
        target_lang_layout = QHBoxLayout()
        self.target_lang_label = QLabel("目标语言:")
        self.target_lang_combo = QComboBox()
        self.target_lang_combo.addItems(["英文 (en)", "中文 (zh)", "俄文 (ru)"])
        target_lang_layout.addWidget(self.target_lang_label)
        target_lang_layout.addWidget(self.target_lang_combo)
        target_lang_layout.addStretch(1)
        right_layout.addLayout(target_lang_layout)

        # 输出文本区域
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("翻译结果将显示在这里...")
        right_layout.addWidget(self.output_text)

        # 添加右侧布局到内容布局
        content_layout.addWidget(right_group)

        # 添加内容布局到主布局
        main_layout.addLayout(content_layout)

        # 进度条和状态信息放在最下面
        status_layout = QHBoxLayout()

        # 添加状态标签
        self.status_label = QLabel("就绪")
        status_layout.addWidget(self.status_label)

        status_layout.addStretch(1)

        # 进度条
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("翻译进度:"))

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
            QMessageBox.warning(self, "警告", "请输入要翻译的文本!")
            return

        # 获取目标语言代码
        target_lang = self.target_lang_combo.currentText().split("(")[1].strip(")")

        # 更新状态
        self.status_label.setText("准备翻译...")

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
            self.status_label.setText("翻译失败")
        else:
            self.status_label.setText("翻译完成")

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        # 根据进度更新状态标签
        if value == 0:
            self.status_label.setText("翻译失败")
        elif value < 100:
            self.status_label.setText("正在翻译...")
        else:
            self.status_label.setText("翻译完成")

    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("就绪")

    def toggle_theme(self):
        """切换明暗主题"""
        self.is_dark_theme = not self.is_dark_theme

        # 根据当前主题状态应用相应的主题
        if self.is_dark_theme:
            apply_dark_theme(QApplication.instance())
            self.theme_button.setText("🌞")  # 太阳图标表示可以切换到亮色主题
        else:
            apply_light_theme(QApplication.instance())
            self.theme_button.setText("🌓")  # 月亮图标表示可以切换到暗色主题


def apply_dark_theme(app):
    """应用深色主题样式"""
    app.setStyle("Fusion")

    # 创建深色调色板
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))

    # 应用调色板
    app.setPalette(dark_palette)

    # 设置样式表
    app.setStyleSheet("""
        QGroupBox {
            border: 1px solid #3A3A3A;
            border-radius: 8px;
            margin-top: 12px;
            font-weight: bold;
            font-size: 14px;
            background-color: #2D2D2D;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: #2A82DA;
        }
        QPushButton {
            background-color: #2A82DA;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #3A92EA;
        }
        QPushButton:pressed {
            background-color: #1A72CA;
        }
        QPushButton:disabled {
            background-color: #555555;
        }
        /* 主题切换按钮特殊样式 */
        QPushButton#themeButton {
            background-color: transparent;
            border: 1px solid #3A3A3A;
            border-radius: 15px;
            padding: 0px;
            font-size: 16px;
        }
        QPushButton#themeButton:hover {
            background-color: rgba(42, 130, 218, 0.2);
        }
        QPushButton#themeButton:pressed {
            background-color: rgba(42, 130, 218, 0.3);
        }
        QTextEdit {
            border: 1px solid #3A3A3A;
            border-radius: 6px;
            padding: 8px;
            background-color: #2D2D2D;
            color: #FFFFFF;
            selection-background-color: #2A82DA;
        }
        QComboBox {
            border: 1px solid #3A3A3A;
            border-radius: 6px;
            padding: 6px;
            background-color: #2D2D2D;
            min-height: 24px;
        }
        QComboBox::drop-down {
            border: none;
            width: 24px;
        }
        QLabel {
            color: #DDDDDD;
        }
        QProgressBar {
            border: 1px solid #3A3A3A;
            border-radius: 6px;
            text-align: center;
            height: 20px;
            background-color: #222222;
            color: white;
        }
        QProgressBar::chunk {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1A72CA, stop:1 #3A92EA);
            border-radius: 5px;
        }
        QStatusBar {
            background-color: #222222;
            color: #DDDDDD;
        }
    """)


def apply_light_theme(app):
    """应用明亮主题样式"""
    app.setStyle("Fusion")

    # 创建明亮调色板
    light_palette = QPalette()
    light_palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(233, 233, 233))
    light_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
    light_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    light_palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
    light_palette.setColor(QPalette.ColorRole.Link, QColor(0, 102, 204))
    light_palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    light_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    # 应用调色板
    app.setPalette(light_palette)

    # 设置样式表
    app.setStyleSheet("""
        QGroupBox {
            border: 1px solid #CCCCCC;
            border-radius: 8px;
            margin-top: 12px;
            font-weight: bold;
            font-size: 14px;
            background-color: #F5F5F5;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 8px 0 8px;
            color: #0078D7;
        }
        QPushButton {
            background-color: #0078D7;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1C84DC;
        }
        QPushButton:pressed {
            background-color: #0067C0;
        }
        QPushButton:disabled {
            background-color: #CCCCCC;
        }
        /* 主题切换按钮特殊样式 */
        QPushButton#themeButton {
            background-color: transparent;
            border: 1px solid #CCCCCC;
            border-radius: 15px;
            padding: 0px;
            font-size: 16px;
            color: #333333;
        }
        QPushButton#themeButton:hover {
            background-color: rgba(0, 120, 215, 0.1);
        }
        QPushButton#themeButton:pressed {
            background-color: rgba(0, 120, 215, 0.2);
        }
        QTextEdit {
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 8px;
            background-color: white;
            color: black;
            selection-background-color: #0078D7;
        }
        QComboBox {
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            padding: 6px;
            background-color: white;
            min-height: 24px;
        }
        QComboBox::drop-down {
            border: none;
            width: 24px;
        }
        QLabel {
            color: #333333;
        }
        QProgressBar {
            border: 1px solid #CCCCCC;
            border-radius: 6px;
            text-align: center;
            height: 20px;
            background-color: #F0F0F0;
            color: black;
        }
        QProgressBar::chunk {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0067C0, stop:1 #1C84DC);
            border-radius: 5px;
        }
        QStatusBar {
            background-color: #F0F0F0;
            color: #333333;
        }
    """)


def main():
    app = QApplication(sys.argv)

    # 设置全局字体
    font = QFont("Microsoft YaHei UI", 10)
    app.setFont(font)

    translator = TranslatorApp()

    # 默认应用亮色主题
    apply_light_theme(app)
    translator.theme_button.setText("🌓")  # 月亮图标表示可以切换到暗色主题

    translator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
