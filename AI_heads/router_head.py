#--------------------------------

# Imports
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import time
import torch
import pickle
import torch.nn as nn
from transformers import DistilBertModel, DistilBertTokenizerFast, DistilBertConfig
#--------------------------------

# Task classification using DistilBert
class DistilBertRouter(nn.Module):
    def __init__(self, num_labels=3, dropout_prob=0.1):
        super().__init__()
        # Load DistilBERT with default config
        self.config = DistilBertConfig()
        self.bert = DistilBertModel(self.config)

        # Classification head
        self.pre_classifier = nn.Linear(self.config.hidden_size, self.config.hidden_size)
        self.dropout = nn.Dropout(dropout_prob)
        self.classifier = nn.Linear(self.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask=None, labels=None):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = outputs.last_hidden_state
        pooled_output = hidden_state[:, 0]
        pooled_output = self.pre_classifier(pooled_output)
        pooled_output = nn.ReLU()(pooled_output)
        pooled_output = self.dropout(pooled_output)
        logits = self.classifier(pooled_output)

        loss = None
        if labels is not None:
            loss_fn = nn.CrossEntropyLoss()
            loss = loss_fn(logits, labels)

        return {"loss": loss, "logits": logits} if loss is not None else {"logits": logits}
#--------------------------------

# Temporary main
if __name__ == "__main__":
    print("Running code")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    """
    TEST INFERENCE TIME OF THE MODEL MOVED TO GPU
    """
    # Load the model and tokenizer
    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
    model = DistilBertRouter(num_labels=34, dropout_prob=0.1).to(device)
    model.load_state_dict(torch.load(
        "./AI_heads/distilbert_router_model.pth",
        weights_only=True)
        )
    model.to(device).eval()

    # Test input
    input_text = "Tell me something funny please"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    # Test and time the forward pass
    start = time.time()
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs["logits"]
    end = time.time()
    print(f"Inference time: {(end - start) * 1000:.2f} ms")

    # Map results back to descriptions
    with open("./AI_heads/label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    predicted_label_id = torch.argmax(logits, dim=1).item()
    predicted_class = label_encoder.inverse_transform([predicted_label_id])[0]
    print("Predicted class:", predicted_class)
