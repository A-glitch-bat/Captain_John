#--------------------------------

# Imports
import json
import torch
from tqdm import tqdm
from router_head import DistilBertRouter
from sklearn.preprocessing import LabelEncoder
from transformers import DistilBertTokenizerFast
from torch.utils.data import Dataset, DataLoader, random_split
#--------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Running code")

# Dataset class
class IntentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=64):
        self.encodings = tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors='pt')
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: val[idx] for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

# Load data from json file
with open("./cleaned_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Split into texts and labels
texts = [example[0] for example in raw_data]
labels = [example[1] for example in raw_data]
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)
num_classes = len(label_encoder.classes_); print("Number of classes:", num_classes)

# Dataset
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
dataset = IntentDataset(texts, encoded_labels, tokenizer)
train_size = int(0.9 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# Dataloader
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=16)

# Load the model
model = DistilBertRouter(num_labels=num_classes, dropout_prob=0.1).to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# Training loop
best_accuracy = 0.0

for epoch in range(10):
    model.train()  # set model to training mode
    total_loss = 0
    loop = tqdm(train_loader, leave=True)

    for batch in loop:
        optimizer.zero_grad()
        batch = {k: v.to(device) for k, v in batch.items()}
        outputs = model(**batch)
        loss = outputs["loss"]
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        loop.set_description(f"Epoch {epoch+1}")
        loop.set_postfix(loss=loss.item())

    avg_train_loss = total_loss / len(train_loader)

    # Validation loop
    model.eval()  # set model to evaluation mode
    val_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for batch in val_loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.get("loss", None)
            if loss is not None:
                val_loss += loss.item()

            logits = outputs["logits"]
            predictions = torch.argmax(logits, dim=-1)
            correct += (predictions == batch["labels"]).sum().item()
            total += batch["labels"].size(0)

    avg_val_loss = val_loss / len(val_loader)
    val_accuracy = correct / total

    print(f"Epoch {epoch+1} finished. Avg loss: {avg_train_loss:.4f}, val. loss: {avg_val_loss:.4f}, accuracy: {val_accuracy:.4f}")

    if val_accuracy > best_accuracy:
        best_accuracy = val_accuracy
        torch.save(model.state_dict(), "distilbert_router_model.pth")
        print(f"Saved new best model at epoch {epoch+1} with accuracy {best_accuracy:.4f}")
