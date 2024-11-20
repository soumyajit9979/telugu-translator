from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("agentlans/text-summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("agentlans/text-summarization")

# Input paragraph
paragraph = """
Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions.
The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem-solving.
AI is being used in various fields such as healthcare, robotics, and data analytics.
The advancements in AI have the potential to revolutionize the way we work and live.
"""

# Preprocess the input text
inputs = tokenizer.encode(paragraph, return_tensors="pt", max_length=1024, truncation=True)

# Generate the summary
summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print("Summary:")
print(summary)
