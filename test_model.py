from transformers import T5ForConditionalGeneration, T5Tokenizer

device = "cpu"  # or 'cpu' for translate on cpu

model_name = "utrobinmv/t5_translate_en_ru_zh_small_1024"
model = T5ForConditionalGeneration.from_pretrained(model_name)
model.to(device)
tokenizer = T5Tokenizer.from_pretrained(model_name)

prefix = "translate to en: "
src_text = prefix + "开发的目的就是向用户提供个性化的同步翻译。"

# translate Russian to Chinese
input_ids = tokenizer(src_text, return_tensors="pt")

generated_tokens = model.generate(**input_ids.to(device))

result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
print(result)
