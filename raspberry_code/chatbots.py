#--------------------------------

# Imports
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
#--------------------------------

# Schizobot class
class Schizobot():
	def __init__(self):
		super().__init__()
		#--------------------------------

		#Load the model and tokenizer
		model_path = "../models/gpt2"
		self.model = AutoModelForCausalLM.from_pretrained(model_path)
		self.tokenizer = AutoTokenizer.from_pretrained(model_path)
		self.chat_history_ids = None
	#--------------------------------

	# Functions
	def get_reply(self, user_input):
		if self.tokenizer.pad_token is None:
			self.tokenizer.pad_token = self.tokenizer.eos_token

		# Tokenize input and get reply from model
		inputs = self.tokenizer(user_input, return_tensors="pt")
		outputs = self.model.generate(
			**inputs,
			pad_token_id=self.tokenizer.eos_token_id,
			)
		reply = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
		return reply
#--------------------------------
