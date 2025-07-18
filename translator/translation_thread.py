"""
翻译线程模块
处理翻译任务，避免UI卡顿
"""

import os

from PyQt6.QtCore import QThread, pyqtSignal
from transformers import T5ForConditionalGeneration, T5Tokenizer

from translator.config import MODEL_PATH, MODEL_NAME, USE_LOCAL_MODEL, MAX_INPUT_LENGTH
from translator.text_formatter import TextFormatter


class TranslationThread(QThread):
    """线程类用于执行翻译任务，避免UI卡顿"""

    translation_done = pyqtSignal(str)
    progress_update = pyqtSignal(int)

    def __init__(self, text, target_lang):
        super().__init__()
        self.text = text
        self.target_lang = target_lang
        self.formatter = TextFormatter()

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
            # 限制输入文本长度，避免超出模型处理能力
            if len(self.text) > MAX_INPUT_LENGTH:
                processed_text = self.text[:MAX_INPUT_LENGTH] + "..."
                print(f"输入文本过长，已截断到{MAX_INPUT_LENGTH}字符")
            else:
                processed_text = self.text

            # 对特殊组合词进行处理，避免被拆分
            import re

            processed_text = re.sub(r"(\w+)-(\w+)", r'"\1-\2"', processed_text)

            prefix = f"translate to {self.target_lang}: "
            src_text = prefix + processed_text

            # 添加调试信息
            print(f"输入文本长度: {len(src_text)}")
            print(f"输入文本: {src_text[:200]}...")  # 只打印前200个字符

            # 分词和生成翻译
            input_ids = tokenizer(
                src_text, return_tensors="pt", max_length=512, truncation=True
            )
            print(f"输入token数量: {input_ids['input_ids'].shape[1]}")
            self.progress_update.emit(80)

            # 使用模型默认参数，避免过度配置
            generated_tokens = model.generate(**input_ids)
            self.progress_update.emit(90)

            # 解码结果
            result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            translated_text = result[0] if result else "翻译失败"

            # 添加调试信息
            print(f"生成的token数量: {generated_tokens.shape[1]}")
            print(
                f"新生成的token数量: {generated_tokens.shape[1] - input_ids['input_ids'].shape[1]}"
            )
            print(f"原始翻译结果: {translated_text}")
            print(f"翻译结果长度: {len(translated_text)}")

            # 移除输入前缀（如果存在）
            if translated_text.startswith(prefix):
                translated_text = translated_text[len(prefix) :].strip()
                print(f"移除前缀后: {translated_text}")

            # 禁用格式恢复，直接使用翻译结果
            # if translated_text != "翻译失败":
            #     formatted_translation = self.formatter.restore_format(translated_text)
            #     print(f"恢复格式后: {formatted_translation}")
            # else:
            #     formatted_translation = translated_text

            # 发送翻译完成信号
            self.progress_update.emit(100)
            self.translation_done.emit(translated_text)

        except Exception as e:
            self.translation_done.emit(f"翻译出错: {str(e)}")
            self.progress_update.emit(0)
