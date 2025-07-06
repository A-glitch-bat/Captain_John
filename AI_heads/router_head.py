#--------------------------------

# Imports
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import torch.nn as nn
from transformers import DistilBertModel, DistilBertConfig
#--------------------------------

# Task classification using DistilBert
class DistilBertRouter(nn.Module):
    def __init__(self, num_labels=3, dropout_prob=0.1):
        super().__init__()
        # Load DistilBERT with default config
        self.config = DistilBertConfig.from_pretrained("distilbert-base-uncased")
        self.bert = DistilBertModel.from_pretrained("distilbert-base-uncased", config=self.config)

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

""" TEST INFERENCE TIME OF THE MODEL MOVED TO GPU
import time
# Input
    text = "Generate a bar chart from this Excel data"
    inputs = tokenizer(text, return_tensors="pt")

    model = model.to(device).eval()
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Warm-up
    for _ in range(3):
        _ = model(**inputs)

    # Time the forward pass
    start = time.time()
    with torch.no_grad():
        _ = model(**inputs)
    end = time.time()
    print(f"Inference time: {(end - start) * 1000:.2f} ms")
"""

# Temporary main
if __name__ == "__main__":
    print("This is the main.")
