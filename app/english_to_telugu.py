from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
model_checkpoint = "aryaumesh/english-to-telugu"

tokenizer = MBart50TokenizerFast.from_pretrained(model_checkpoint)
model = MBartForConditionalGeneration.from_pretrained(model_checkpoint)

text = "This is a test case." # Sentence to translate
inputs = tokenizer(text, return_tensors="pt")

outputs = model.generate(**inputs)
print(tokenizer.decode(outputs[0], skip_special_tokens=True)) # ఈ ఒక పరీక్ష కేసు ఉంది.
