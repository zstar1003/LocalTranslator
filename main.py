import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QLabel,
    QComboBox,
    QProgressBar,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
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
        self.initUI()
        self.translation_thread = None

    def initUI(self):
        # 设置窗口
        self.setWindowTitle("PyQt6 翻译器")
        self.setGeometry(100, 100, 900, 500)

        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局 - 垂直布局，包含上部的左右布局和下部的进度条
        main_layout = QVBoxLayout(central_widget)
        
        # 创建左右布局
        content_layout = QHBoxLayout()
        
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
        
        # 中间控制按钮区域
        middle_layout = QVBoxLayout()
        middle_layout.addStretch(1)
        
        # 翻译按钮
        self.translate_button = QPushButton("翻译 →")
        self.translate_button.setFixedWidth(100)
        self.translate_button.clicked.connect(self.start_translation)
        middle_layout.addWidget(self.translate_button)
        
        # 清除按钮
        self.clear_button = QPushButton("清除")
        self.clear_button.setFixedWidth(100)
        self.clear_button.clicked.connect(self.clear_text)
        middle_layout.addWidget(self.clear_button)
        
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
        
        # 进度条放在最下面
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(QLabel("翻译进度:"))
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)
        
        main_layout.addLayout(progress_layout)

    def start_translation(self):
        # 获取输入文本
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "警告", "请输入要翻译的文本!")
            return

        # 获取目标语言代码
        target_lang = self.target_lang_combo.currentText().split("(")[1].strip(")")

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

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()
        self.progress_bar.setValue(0)


def main():
    app = QApplication(sys.argv)
    translator = TranslatorApp()
    translator.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
