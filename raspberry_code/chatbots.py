#--------------------------------

# Imports
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pickle
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DistilBertTokenizerFast
from AI_heads.router_head import DistilBertRouter
#--------------------------------

# Routerbot interface
class Routerbot():
	def __init__(self):
		super().__init__()
		#--------------------------------
		self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

		# Load the model and tokenizer
		self.tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
		self.model = DistilBertRouter(num_labels=34, dropout_prob=0.1).to(self.device)
		self.model.load_state_dict(torch.load(
			"./AI_heads/distilbert_router_model.pth",
			weights_only=True)
			)
		self.model.to(self.device).eval()
	#--------------------------------

	# Functions
	def classify(self, user_input):
		inputs = self.tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)
		inputs = {k: v.to(self.device) for k, v in inputs.items()}

		with torch.no_grad():
			outputs = self.model(**inputs)
			logits = outputs["logits"]

		# Map results back to descriptions
		with open("./AI_heads/label_encoder.pkl", "rb") as f:
			label_encoder = pickle.load(f)
		predicted_label_id = torch.argmax(logits, dim=1).item()
		predicted_class = label_encoder.inverse_transform([predicted_label_id])[0]

		return predicted_class
#--------------------------------

# Schizobot interface
class Schizobot():
	def __init__(self):
		super().__init__()
		#--------------------------------

		#Load the model and tokenizer
		model_path = "./models/gpt2"
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
