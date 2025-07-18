from transformers import T5ForConditionalGeneration, T5Tokenizer

device = "cpu"  # or 'cpu' for translate on cpu

model_name = "utrobinmv/t5_translate_en_ru_zh_small_1024"

MODEL_PATH = "./models"
# LOCAL_MODEL_PATH = os.path.join(MODEL_PATH, "t5_translate_model")

model = T5ForConditionalGeneration.from_pretrained(MODEL_PATH)
model.to(device)
tokenizer = T5Tokenizer.from_pretrained(MODEL_PATH)

# model = T5ForConditionalGeneration.from_pretrained(model_name)

# tokenizer = T5Tokenizer.from_pretrained(model_name)

prefix = "translate to zh: "
src_text = (
    prefix
    + "Source: 10.1016/j.eiar.2022.106897 Original: To assess the economic aspects of PBs, the current literature employed various methods such as LCC, cost-benefit method, and total cost calculation (). LCC has been utilized to evaluate the costs related to every phase of a building life cycle and clarify the distribution of the costs within all phases (Samani et al., 2018). The cost-benefit method was used to evaluate the economic aspects of PBs, and the total cost calculation method was used to evaluate the economic aspects of PBs. Source: 无 Original: In the poresent study, the out-degree centrality of a node indicated the extent to which this stakeholder pointed out problematic interfaces for others, and in-degree centrality of a node means the extent to which other stakeholders pointed out that they experienced problematic interfaces with this stakeholder. Error: Poresent Source:https://www-sciencedirect-com.eproxy.lib.hku.hk/science/article/pii/S1544612324000400?via%3Dihub Original: Geographic Endowment, Business Enronment and Corporate Financal Asset Alocation——Empincal Eydence from a share listed Corporate Error: a lot of typos"
)

# translate Russian to Chinese
input_ids = tokenizer(src_text, return_tensors="pt")

generated_tokens = model.generate(**input_ids.to(device))

result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
print(result)
