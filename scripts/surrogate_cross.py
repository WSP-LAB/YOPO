import os
import torch.nn as nn
import torch.utils.data
from torch.utils.data import Dataset, DataLoader, random_split
import torchvision
import csv, random
import pandas as pd
import numpy as np
from torchvision import transforms
from sklearn.metrics import precision_score, recall_score
from MyDataset import CustomDataset
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--csv-path', type=str)
parser.add_argument('--csv-name', type=str)
parser.add_argument('--save-fpath', type=str)
parser.add_argument('--model', type=str)
args = parser.parse_args()

# Hyper-parameters & Variables setting
num_epoch = 30
learning_rate = 5e-4
dropout_rate = 0.1
batch_size = 30

surrogate_data = pd.read_csv("/yopo-artifact/data/dataset/for_surrogate/final_query_30perc_100000_{}.csv".format(args.model))
feature_size = len(surrogate_data.columns) - 1
hidden_size1 = 1024
hidden_size2 = 512
hidden_size3 = 256

csv_path = args.csv_path
csv_name = args.csv_name
save_fpath = args.save_fpath

# Device setting
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("  Now using {} device".format(device))

# Load data
dataset = CustomDataset(csv_path + csv_name)
dataset_size = len(dataset)

train_size = int(dataset_size * 0.9)
test_size = dataset_size - train_size

train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True, drop_last=True)

# print(f"Training Data Size : {len(train_dataset)}")
# print(f"Testing Data Size : {len(test_dataset)}")

# Declares Surrogate model
class Surrogate(nn.Module):
    def __init__(self):
        super(Surrogate, self).__init__()
        self.linear1 = nn.Linear(feature_size, hidden_size1)
        self.linear2 = nn.Linear(hidden_size1, hidden_size2)
        self.linear3 = nn.Linear(hidden_size2, hidden_size3)
        self.linear4 = nn.Linear(hidden_size3, 2)
        self.dropout = nn.Dropout(0.1)
        self.leacky_relu = nn.LeakyReLU(0.2)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.leacky_relu(self.linear1(x))
        # x = self.dropout(x)
        x = self.leacky_relu(self.linear2(x))
        # x = self.dropout(x)
        x = self.leacky_relu(self.linear3(x))
        x = self.linear4(x)
        return x

# Initialize surrogate model
surrogate = Surrogate().to(device)

# Loss function & Optimizer setting
criterion = nn.CrossEntropyLoss().to(device)
optimizer = torch.optim.Adam(surrogate.parameters(), lr=learning_rate)

"""
Training phase
"""
for epoch in range(num_epoch):
    correct = 0
    for i, (features, label) in enumerate(train_dataloader):
        
        # reshape
        feat = features.to(device)
        lab = label.squeeze(dim=-1).to(torch.int64).to(device)
        
        # Initialize grad
        optimizer.zero_grad()
        
        # Prediction
        pred = surrogate(feat)

        # Compute loss
        loss = criterion(pred, lab)
    
        # Train surrogate model with backpropagation
        loss.backward()
        optimizer.step()
        
        # Count correct predictions
        predictions = torch.argmax(pred, dim=1)
        correct += torch.sum(predictions == lab).item()

    # Compute accuracy
    accuracy = 100 * correct / len(train_dataset)
    

"""
Testing phase
"""
correct = 0

# Fix gradient
with torch.no_grad():
    surrogate.eval()

    for x, y in test_dataloader:
        x = x.to(device)
        y = y.to(device)
        
        # Predict test dataset
        pred = surrogate(x)
        
        # Count correct predictions
        outputs = torch.argmax(pred, dim=1)
        y = torch.reshape(y, outputs.shape)
        correct += torch.sum(outputs == y)

    # print surrogate model's test performance
    accuracy = float(correct) / len(test_dataset)
    print("  Surrogate model acc. : {:.2f}%".format(accuracy * 100))

# Extract test dataset
features = []
labels = []
for batch in test_dataloader:
    batch_features, batch_labels = batch
    features.extend(batch_features.numpy())
    labels.extend(batch_labels.numpy())
labels = [int(label) for label in labels]

torch.save(surrogate.state_dict(), save_fpath)

print("  Done.")
