"""
翻译线程模块
处理翻译任务，避免UI卡顿
"""

import os

from PyQt6.QtCore import QThread, pyqtSignal
from transformers import T5ForConditionalGeneration, T5Tokenizer

from translator.config import MODEL_PATH, MODEL_NAME, USE_LOCAL_MODEL


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

            # 加载模型和分词器 - 优先使用本地模型
            if USE_LOCAL_MODEL:
                self.progress_update.emit(20)
                # 直接从本地模型目录加载
                model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
                self.progress_update.emit(50)
                tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)
            else:
                # 如果本地模型不存在，则从在线加载
                model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
                self.progress_update.emit(50)
                tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)

                # 保存模型到本地以便下次使用
                try:
                    os.makedirs(MODEL_PATH, exist_ok=True)
                    model.save_pretrained(MODEL_PATH)
                    tokenizer.save_pretrained(MODEL_PATH)
                except Exception as e:
                    print(f"保存模型到本地时出错: {str(e)}")

            self.progress_update.emit(70)

            # 准备输入
            # 对特殊组合词进行处理，避免被拆分
            processed_text = self.text
            # 将连字符组合词用引号包围，避免被拆分
            import re

            processed_text = re.sub(r"(\w+)-(\w+)", r'"\1-\2"', processed_text)

            prefix = f"translate to {self.target_lang}: "
            src_text = prefix + processed_text

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
