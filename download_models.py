import os

from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "utrobinmv/t5_translate_en_ru_zh_small_1024"
MODEL_PATH = "./models"

os.mkdir(MODEL_PATH, exist_ok=True)

# 下载模型和分词器并保存到本地
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)

# 保存模型和分词器到指定目录
model.save_pretrained(MODEL_PATH)
tokenizer.save_pretrained(MODEL_PATH)
