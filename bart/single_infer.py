
from transformers import PLBartTokenizer, PLBartForConditionalGeneration, PLBartConfig

#model = PLBartForConditionalGeneration.from_pretrained("uclanlp/plbart-base")
tokenizer = PLBartTokenizer.from_pretrained("uclanlp/plbart-base")
config = PLBartConfig.from_pretrained("uclanlp/plbart-base")

file = os.path.join('codenet/java2java/checkpoint-best-ppl', 'pytorch_model.bin')
model = PLBartForConditionalGeneration.from_pretrained(file, config = config)



