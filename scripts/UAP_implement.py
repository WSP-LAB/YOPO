import numpy as np
from sklearn.preprocessing import LabelEncoder
import json
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import torchvision.utils
from torchvision import models
import torchvision.datasets as dsets
import torchvision.transforms as transforms
import csv
import pickle
import pandas as pd
import joblib
import argparse
from MyDataset import CustomDataset
import random
import feature_names_adgraph, feature_names_webgraph, feature_names_adflush, feature_names_pagegraph
from cost_dict_adgraph import FEATURES_COST_DC, FEATURES_COST_HCC, FEATURES_COST_HSC
from cost_dict_webgraph import FEATURES_COST_WEBGRAPH_DC, FEATURES_COST_WEBGRAPH_HCC, FEATURES_COST_WEBGRAPH_HSC
from cost_dict_adflush import FEATURES_COST_ADFLUSH_DC, FEATURES_COST_ADFLUSH_HCC, FEATURES_COST_ADFLUSH_HJC
from cost_dict_pagegraph import FEATURES_COST_PAGEGRAPH_DC, FEATURES_COST_PAGEGRAPH_HCC, FEATURES_COST_PAGEGRAPH_HSC

# Functions
def subtract_list(list1, blist2):
    return list(set(list1) - set(blist2))

# Make FEATURES_TO_PERTURBE_CAT_ALL list
def make_FEATURES_TO_PERTURBE_CAT_ALL(csv_file_path, feature_list):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
    
    for feature in feature_list:
        matching_columns = [col for col in header if col.startswith(feature)]
    return matching_columns, header

# Read Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--csv-path', type=str)
parser.add_argument('--csv-name-ad', type=str)
parser.add_argument('--out-name', type=str)
parser.add_argument('--delta-name', type=str)
parser.add_argument('--lagrangain', type=float)
parser.add_argument('--model-fpath', type=str)
parser.add_argument('--csv-target-name', type=str)
parser.add_argument('--sampling-size', type=int)
parser.add_argument('--epsilon', type=int)
parser.add_argument('--mode', type=str)
parser.add_argument('--cuda', type=str)
args = parser.parse_args()

csv_path = args.csv_path
csv_name_ad = args.csv_name_ad
out_name = args.out_name
delta_name = args.delta_name
lagrangain = args.lagrangain
model_fpath = args.model_fpath
csv_target_name = args.csv_target_name
sampling_size = args.sampling_size
epsilon = args.epsilon
mode = args.mode

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("  Now using {} device".format(device))

# Read column name and Get FEATURES_TO_PERTURBE_CAT_ALL
if mode == "adgraph":
    feat_exclude = ["DOMAIN_NAME", "NODE_ID", "FEATURE_KATZ_CENTRALITY", "FEATURE_FIRST_PARENT_KATZ_CENTRALITY", "FEATURE_SECOND_PARENT_KATZ_CENTRALITY"]
    FEATURES_TO_PERTURBE_CAT_ALL, col_name_all = make_FEATURES_TO_PERTURBE_CAT_ALL(f"/yopo-artifact/data/dataset/from_adgraph/features_nn.csv", feature_names_adgraph.FEATURES_CATEGORICAL)
elif mode == "webgraph":
    feat_exclude = ["top_level_url", "visit_id", "name"]
    FEATURES_TO_PERTURBE_CAT_ALL, col_name_all = make_FEATURES_TO_PERTURBE_CAT_ALL(f"/yopo-artifact/data/dataset/from_webgraph/features_nn.csv", feature_names_webgraph.FEATURES_CATEGORICAL)
elif mode == "adflush":
    feat_exclude = ["top_level_url", "visit_id", "name"]
    FEATURES_TO_PERTURBE_CAT_ALL, col_name_all = make_FEATURES_TO_PERTURBE_CAT_ALL(f"/yopo-artifact/data/dataset/from_adflush/features_nn.csv", feature_names_adflush.FEATURES_CATEGORICAL)
elif mode == "pagegraph":
    feat_exclude = ["NETWORK_REQUEST_URL", "FINAL_URL"]
    FEATURES_TO_PERTURBE_CAT_ALL, col_name_all = make_FEATURES_TO_PERTURBE_CAT_ALL(f"/yopo-artifact/data/dataset/from_pagegraph/features_nn.csv", feature_names_pagegraph.FEATURES_CATEGORICAL)
else:
    raise("Mode error!")

col_name = [item for item in col_name_all if item not in feat_exclude]

# Hyper-parameters & Variables setting
dropout_rate = 0.1
num_step = epsilon * 10
step_size = 0.1

surrogate_data = pd.read_csv("/yopo-artifact/data/dataset/for_surrogate/final_query_30perc_100000_{}.csv".format(args.mode))
feature_size = len(surrogate_data.columns) - 1

hidden_size1 = 1024
hidden_size2 = 512
hidden_size3 = 256

# Check min / max value
df_sample = pd.read_csv(csv_path + csv_name_ad)
max_values = []
min_values = []

# Iterate over each column
for column in df_sample.columns:
    # Find the maximum and minimum values for the column
    max_value = df_sample[column].max()
    min_value = df_sample[column].min()
    
    # Append the maximum and minimum values to the respective lists
    max_values.append(max_value)
    min_values.append(min_value)
    
max_values.pop()
min_values.pop()
diff_values = [(x - y) for x, y in zip(max_values, min_values)]
if mode == "adgraph":
    feats_to_pert_numeric = [col_name.index(col) for col in feature_names_adgraph.FEATURES_TO_PERTURBE_NUMERIC]
elif mode == "webgraph":
    feats_to_pert_numeric = [col_name.index(col) for col in feature_names_webgraph.FEATURES_TO_PERTURBE_NUMERIC]
elif mode == "adflush":
    feats_to_pert_numeric = [col_name.index(col) for col in feature_names_adflush.FEATURES_TO_PERTURBE_NUMERIC]
elif mode == "pagegraph":
    feats_to_pert_numeric = [col_name.index(col) for col in feature_names_pagegraph.FEATURES_TO_PERTURBE_NUMERIC]

for i in range(len(diff_values)):
    if i not in feats_to_pert_numeric:
        diff_values[i] = epsilon
# print("Diff values:", diff_values)
# Load data
dataset = CustomDataset(csv_path + csv_name_ad)

# Subset_dataset = CustomDataset(*[t[outp == 1] for t in dataset])
dataset_size = len(dataset)
train_size = min(int(sampling_size), len(dataset))
print("  UAP size : {}".format(train_size))
print("  Lagrangian multiplier (lambda) size : {}".format(lagrangain))

train_dataset, _ = random_split(dataset, [train_size, dataset_size - train_size])
train_dataloader = DataLoader(train_dataset, batch_size=train_size, shuffle=True, drop_last=True)

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
        x = self.dropout(x)
        x = self.leacky_relu(self.linear2(x))
        x = self.dropout(x)
        x = self.leacky_relu(self.linear3(x))
        x = self.linear4(x)
        return x

# Initialize surrogate model
model = Surrogate().to(device)
print("  Loading surrogate model from {}".format(model_fpath))
model.load_state_dict(torch.load(model_fpath))
model.eval()

total = train_size
correct = 0
for x, y in train_dataloader:
    x = x.to(device)
    y = y.to(device)
    
    # Predict train dataset
    pred = model(x)
    
    # Count correct predictions
    outputs = torch.argmax(pred, dim=1)
    y = torch.reshape(y, outputs.shape)
    correct += torch.sum(outputs == y)

# print('Accuracy of trainset before attack: %f %%' % (100 * float(correct) / total))
 
# Attack
def UAP_attack(_model, features, labels, lagrangain, eps=epsilon, step_size=step_size, num_steps=num_step):
    p = torch.zeros_like(features[1])
    print("  p's shape :", p.shape)
    
    features = features.to(device)
    labels = labels.to(device)
    print("  features's shape :", features.shape)

    loss_fn = nn.CrossEntropyLoss(reduction="mean")
    optimizer = optim.Adam([p.requires_grad_()], lr=step_size)

    for i in range(num_steps):
        if i == num_steps - 1:
            final_step = True
        else:
            final_step = False

        p_exp = p.repeat(train_size, 1)
        injected_feat = inject_feature(features, p_exp)
        outputs = _model(injected_feat)
        cost = compute_cost(injected_feat, features)
        loss = cost - (lagrangain * loss_fn(outputs, labels).to(device))
        optimizer.zero_grad()
        loss.backward()
        
        with torch.no_grad():
            p.grad.sign_()
            p.data.sub_(p.grad * step_size)
            p.data.clamp_(min=-torch.tensor(diff_values).to(device), max=torch.tensor(diff_values).to(device))
            p = pert_constraints(p, final_step)
            # print(p)
        p.grad.zero_()

    # log the cost
    result_dir = "/yopo-artifact/result/costs.txt"
    with open(result_dir, "a") as f_log:
        f_log.write(f"{out_name}, {str(cost)}\n")
    
    return p


def pert_constraints(pert, final):
    feats_to_not_pert = []
    feats_all = list(range(feature_size))
    
    if mode == "adgraph":
        feats_to_pert_numeric = [col_name.index(col) for col in feature_names_adgraph.FEATURES_TO_PERTURBE_NUMERIC]
        feats_to_pert_binary = [col_name.index(col) for col in feature_names_adgraph.FEATURES_TO_PERTURBE_BINARY_ALL]
        feats_to_pert_cat = [col_name.index(col) for col in FEATURES_TO_PERTURBE_CAT_ALL]
    elif mode == "webgraph":
        feats_to_pert_numeric = [col_name.index(col) for col in feature_names_webgraph.FEATURES_TO_PERTURBE_NUMERIC]
        feats_to_pert_binary = [col_name.index(col) for col in feature_names_webgraph.FEATURES_TO_PERTURBE_BINARY_ALL]
        feats_to_pert_cat = [col_name.index(col) for col in FEATURES_TO_PERTURBE_CAT_ALL]
    elif mode == "adflush":
        feats_to_pert_numeric = [col_name.index(col) for col in feature_names_adflush.FEATURES_TO_PERTURBE_NUMERIC]
        feats_to_pert_binary = [col_name.index(col) for col in feature_names_adflush.FEATURES_TO_PERTURBE_BINARY_ALL]
        feats_to_pert_cat = [col_name.index(col) for col in FEATURES_TO_PERTURBE_CAT_ALL]
    elif mode == "pagegraph":
        feats_to_pert_numeric = [col_name.index(col) for col in feature_names_pagegraph.FEATURES_TO_PERTURBE_NUMERIC]
        feats_to_pert_binary = [col_name.index(col) for col in feature_names_pagegraph.FEATURES_TO_PERTURBE_BINARY_ALL]
        feats_to_pert_cat = [col_name.index(col) for col in FEATURES_TO_PERTURBE_CAT_ALL]

    feats_to_pert = feats_to_pert_numeric + feats_to_pert_binary + feats_to_pert_cat
    feats_to_not_pert += subtract_list(feats_all, feats_to_pert)
    
    # for numeric features
    if mode == "adgraph":
        feats_to_increase = [col_name.index(col) for col in feature_names_adgraph.FEATURES_TO_INCREASE_ONLY]
    elif mode == "webgraph":
        feats_to_increase = [col_name.index(col) for col in feature_names_webgraph.FEATURES_TO_INCREASE_ONLY]
    elif mode == "adflush":
        feats_to_increase = [col_name.index(col) for col in feature_names_adflush.FEATURES_TO_INCREASE_ONLY]
    elif mode == "pagegraph":
        feats_to_increase = [col_name.index(col) for col in feature_names_pagegraph.FEATURES_TO_INCREASE_ONLY]
    for increase in feats_to_increase:
        if pert[increase] < 0:
            pert[increase] = 0
    pert[feats_to_not_pert] = 0
    
    # for binary features
    if mode == "adgraph":
        if final:
            for col in feature_names_adgraph.FEATURES_TO_PERTURBE_BINARY:
                col_0 = col + "_0"
                col_1 = col + "_1"
                col_0_idx = col_name.index(col_0)
                col_1_idx = col_name.index(col_1)
                if pert[col_0_idx].item() >= pert[col_1_idx].item():
                    pert[col_0_idx] = 1
                    pert[col_1_idx] = 0
                elif pert[col_0_idx].item() < pert[col_1_idx].item():
                    pert[col_0_idx] = 0
                    pert[col_1_idx] = 1
    elif mode == "webgraph":
        if final:
            for col in feature_names_webgraph.FEATURES_TO_PERTURBE_BINARY:
                col_0 = col + "_0"
                col_1 = col + "_1"
                col_0_idx = col_name.index(col_0)
                col_1_idx = col_name.index(col_1)
                if pert[col_0_idx].item() >= pert[col_1_idx].item():
                    pert[col_0_idx] = 1
                    pert[col_1_idx] = 0
                elif pert[col_0_idx].item() < pert[col_1_idx].item():
                    pert[col_0_idx] = 0
                    pert[col_1_idx] = 1

    elif mode == "adflush":
        if final:
            for col in feature_names_adflush.FEATURES_TO_PERTURBE_BINARY:
                col_0 = col + "_0"
                col_1 = col + "_1"
                col_0_idx = col_name.index(col_0)
                col_1_idx = col_name.index(col_1)
                if pert[col_0_idx].item() >= pert[col_1_idx].item():
                    pert[col_0_idx] = 1
                    pert[col_1_idx] = 0
                elif pert[col_0_idx].item() < pert[col_1_idx].item():
                    pert[col_0_idx] = 0
                    pert[col_1_idx] = 1    

    elif mode == "pagegraph":
        if final:
            for col in feature_names_pagegraph.FEATURES_TO_PERTURBE_BINARY:
                col_0 = col + "_0"
                col_1 = col + "_1"
                col_0_idx = col_name.index(col_0)
                col_1_idx = col_name.index(col_1)
                if pert[col_0_idx].item() >= pert[col_1_idx].item():
                    pert[col_0_idx] = 1
                    pert[col_1_idx] = 0
                elif pert[col_0_idx].item() < pert[col_1_idx].item():
                    pert[col_0_idx] = 0
                    pert[col_1_idx] = 1

    if final:
        # handle categorical features for final step of optimization
        # select one having largest value.

        # Only adgraph has perturbed categorical features.
        if mode == "adgraph":
            for col in feature_names_adgraph.FEATURES_TO_PERTURBE_CAT:
                col_names = [s for s in col_name if s.startswith(col)]
                col_indices = [col_name.index(tag) for tag in col_names]

                pert_clone = pert.clone()
                for i in range(len(pert_clone)):
                    if i not in col_indices:
                        pert_clone[i] = 0
                # assign value "1" for largest perturbation.
                max_value = max(pert_clone[i] for i in col_indices)
                max_indices = [i for i, value in enumerate(pert_clone) if value == max_value]
                # print("Max value: {}".format(max_value))
                # print("Max indices: {}".format(max_indices))
                selected_index = random.choice(max_indices)
                indices_except_selected = subtract_list(col_indices, [selected_index])
                
                pert[selected_index] = 1
                pert[indices_except_selected] = 0

    return pert


def inject_feature(feature, pert):
    result = feature.clone()
    result_tmp = feature.clone()
    if mode == "adgraph":
        feats_to_pert_numeric = [col_name.index(col) for col in feature_names_adgraph.FEATURES_TO_PERTURBE_NUMERIC]
        feats_to_pert_binary = [col_name.index(col) for col in feature_names_adgraph.FEATURES_TO_PERTURBE_BINARY_ALL]
        feats_to_pert_1 = [col_name.index(col) for col in FEATURES_TO_PERTURBE_CAT_ALL]
        
        for num_idx in feats_to_pert_numeric:
            result[:, num_idx] += pert[:, num_idx]
        
        # for binary features
        for bin_idx in feats_to_pert_binary:
            result[:, bin_idx] += pert[:, bin_idx]
            result_tmp[:, bin_idx] = result[:, bin_idx]
            
        for i in range(0, len(feats_to_pert_binary), 2):
            idx_first_bin = feats_to_pert_binary[i]
            bin_value_0 = result[:, idx_first_bin]
            bin_value_1 = result[:, idx_first_bin + 1]
            
            bin_values = torch.stack([bin_value_0, bin_value_1], dim=1)
            bin_softmax_values = torch.nn.functional.softmax(bin_values, dim=1)
            result[:, idx_first_bin] = bin_softmax_values[:, 0]
            result[:, idx_first_bin + 1] = bin_softmax_values[:, 1]
        
        # for categorical features
        softmax_probs1 = torch.zeros(feature_size).to(device)
        softmax_probs1[feats_to_pert_1] = torch.softmax(pert[0, feats_to_pert_1], dim=0)

        for cat_idx in feats_to_pert_1:
            result[:, cat_idx] = softmax_probs1[cat_idx]

    elif mode == "webgraph":
        feats_to_pert_numeric = [col_name.index(col) for col in feature_names_webgraph.FEATURES_TO_PERTURBE_NUMERIC]
        feats_to_pert_binary = [col_name.index(col) for col in feature_names_webgraph.FEATURES_TO_PERTURBE_BINARY_ALL]
        
        for num_idx in feats_to_pert_numeric:
            result[:, num_idx] += pert[:, num_idx]
        
        # for binary features
        for bin_idx in feats_to_pert_binary:
            result[:, bin_idx] += pert[:, bin_idx]
        
        for i in range(0, len(feats_to_pert_binary), 2):
            idx_first_bin = feats_to_pert_binary[i]
            bin_value_0 = result[:, idx_first_bin]
            bin_value_1 = result[:, idx_first_bin + 1]
            bin_values = torch.stack([bin_value_0, bin_value_1], dim=1)
            bin_softmax_values = torch.nn.functional.softmax(bin_values, dim=1)
            
            result[:, idx_first_bin] = bin_softmax_values[:, 0]
            result[:, idx_first_bin + 1] = bin_softmax_values[:, 1]

    elif mode == "adflush":
        feats_to_pert_numeric = [col_name.index(col) for col in feature_names_adflush.FEATURES_TO_PERTURBE_NUMERIC]
        feats_to_pert_binary = [col_name.index(col) for col in feature_names_adflush.FEATURES_TO_PERTURBE_BINARY_ALL]
        
        for num_idx in feats_to_pert_numeric:
            result[:, num_idx] += pert[:, num_idx]
        
        # for binary features
        for bin_idx in feats_to_pert_binary:
            result[:, bin_idx] += pert[:, bin_idx]
        
        for i in range(0, len(feats_to_pert_binary), 2):
            idx_first_bin = feats_to_pert_binary[i]
            bin_value_0 = result[:, idx_first_bin]
            bin_value_1 = result[:, idx_first_bin + 1]
            bin_values = torch.stack([bin_value_0, bin_value_1], dim=1)
            bin_softmax_values = torch.nn.functional.softmax(bin_values, dim=1)
            
            result[:, idx_first_bin] = bin_softmax_values[:, 0]
            result[:, idx_first_bin + 1] = bin_softmax_values[:, 1]

    elif mode == "pagegraph":
        feats_to_pert_numeric = [col_name.index(col) for col in feature_names_pagegraph.FEATURES_TO_PERTURBE_NUMERIC]
        feats_to_pert_binary = [col_name.index(col) for col in feature_names_pagegraph.FEATURES_TO_PERTURBE_BINARY_ALL]
        
        for num_idx in feats_to_pert_numeric:
            result[:, num_idx] += pert[:, num_idx]
        
        # for binary features
        for bin_idx in feats_to_pert_binary:
            result[:, bin_idx] += pert[:, bin_idx]
        
        for i in range(0, len(feats_to_pert_binary), 2):
            idx_first_bin = feats_to_pert_binary[i]
            bin_value_0 = result[:, idx_first_bin]
            bin_value_1 = result[:, idx_first_bin + 1]
            bin_values = torch.stack([bin_value_0, bin_value_1], dim=1)
            bin_softmax_values = torch.nn.functional.softmax(bin_values, dim=1)
            
            result[:, idx_first_bin] = bin_softmax_values[:, 0]
            result[:, idx_first_bin + 1] = bin_softmax_values[:, 1]

    return result


def compute_cost(injected_features, orig_features):
    cost = 0
    diff_features = injected_features - orig_features
    
    if mode == "adgraph":
        if "_DC_" in out_name:
            selected_features_cost = FEATURES_COST_DC
        elif "_HCC_" in out_name:
            selected_features_cost = FEATURES_COST_HCC
        elif "_HSC_" in out_name:
            selected_features_cost = FEATURES_COST_HSC
        else:
            raise ValueError("Unknown mode!")

        for pert_numeric in feature_names_adgraph.FEATURES_TO_PERTURBE_NUMERIC:
            cost += selected_features_cost[pert_numeric] * diff_features[:, col_name.index(pert_numeric)].abs().sum()      
        for pert_bin in feature_names_adgraph.FEATURES_TO_PERTURBE_BINARY_ALL:
            cost += selected_features_cost[pert_bin] * diff_features[:, col_name.index(pert_bin)].abs().sum()
        for pert_cat in FEATURES_TO_PERTURBE_CAT_ALL:
            cost += selected_features_cost["FEATURE_CATEGORICAL"] * diff_features[:, col_name.index(pert_cat)].abs().sum()
    
    elif mode == "webgraph":
        if "_DC_" in out_name:
            selected_features_cost = FEATURES_COST_WEBGRAPH_DC
        elif "_HCC_" in out_name:
            selected_features_cost = FEATURES_COST_WEBGRAPH_HCC
        elif "_HSC_" in out_name:
            selected_features_cost = FEATURES_COST_WEBGRAPH_HSC
        else:
            raise ValueError("Unknown mode!")

        for pert_numeric in feature_names_webgraph.FEATURES_TO_PERTURBE_NUMERIC:
            cost += selected_features_cost[pert_numeric] * diff_features[:, col_name.index(pert_numeric)].abs().sum()
        for pert_bin in feature_names_webgraph.FEATURES_TO_PERTURBE_BINARY_ALL:
            cost += selected_features_cost[pert_bin] * diff_features[:, col_name.index(pert_bin)].abs().sum()

    elif mode == "adflush":
        if "_DC_" in out_name:
            selected_features_cost = FEATURES_COST_ADFLUSH_DC
        elif "_HCC_" in out_name:
            selected_features_cost = FEATURES_COST_ADFLUSH_HCC
        elif "_HSC_" in out_name:
            selected_features_cost = FEATURES_COST_ADFLUSH_HJC
        else:
            raise ValueError("Unknown mode!")

        for pert_numeric in feature_names_adflush.FEATURES_TO_PERTURBE_NUMERIC:
            cost += selected_features_cost[pert_numeric] * diff_features[:, col_name.index(pert_numeric)].abs().sum()
        for pert_bin in feature_names_adflush.FEATURES_TO_PERTURBE_BINARY_ALL:
            cost += selected_features_cost[pert_bin] * diff_features[:, col_name.index(pert_bin)].abs().sum()

    elif mode == "pagegraph":
        if "_DC_" in out_name:
            selected_features_cost = FEATURES_COST_PAGEGRAPH_DC
        elif "_HCC_" in out_name:
            selected_features_cost = FEATURES_COST_PAGEGRAPH_HCC
        elif "_HSC_" in out_name:
            selected_features_cost = FEATURES_COST_PAGEGRAPH_HJC
        else:
            raise ValueError("Unknown mode!")
            
        for pert_numeric in feature_names_pagegraph.FEATURES_TO_PERTURBE_NUMERIC:
            cost += selected_features_cost[pert_numeric] * diff_features[:, col_name.index(pert_numeric)].abs().sum()
        for pert_bin in feature_names_pagegraph.FEATURES_TO_PERTURBE_BINARY_ALL:
            cost += selected_features_cost[pert_bin] * diff_features[:, col_name.index(pert_bin)].abs().sum()

    return cost / train_size

model.eval()
total = train_size
correct = 0

for features, labels in train_dataloader:
    labels = labels.long().squeeze(dim=-1)
    features = features.to(device)
    pert = UAP_attack(model, features, labels, lagrangain)

# Save as csv (pert)
pert_np = pd.DataFrame(pert.to('cpu').detach().numpy().reshape(1, -1), columns=col_name[:-1])
pert_np.to_csv(csv_path + delta_name, index=False)

# Reverse one-hot encoding binary features in pert
df_pert = pd.read_csv(csv_path + delta_name)

if mode == "adgraph":
    for bin_feat in feature_names_adgraph.FEATURES_BINARY:
        df_pert[bin_feat] = int(df_pert[bin_feat + "_1"])
        df_pert.drop([bin_feat + "_0", bin_feat + "_1"], axis=1, inplace=True)
    
    # Reverse label encoding in pert
    for col in feature_names_adgraph.FEATURES_TO_PERTURBE_CAT:
        col_names = [s for s in col_name if s.startswith(col)]
        col_indices = [col_name.index(tag) for tag in col_names]
        # col_indices = [df_pert.columns.get_loc(tag) for tag in getattr(feature_names_adgraph, col)]
        max_index = max(col_indices, key=lambda i: df_pert.iloc[0, i])
        df_pert.iloc[0, max_index] = 1
        for_drop = [i for i in col_indices if i != max_index]
        df_pert.drop(df_pert.columns[for_drop], axis=1, inplace=True)

elif mode == "webgraph":
    for bin_feat in feature_names_webgraph.FEATURES_BINARY:
        df_pert[bin_feat] = int(df_pert[bin_feat + "_1"])
        df_pert.drop([bin_feat + "_0", bin_feat + "_1"], axis=1, inplace=True)

elif mode == "adflush":
    for bin_feat in feature_names_adflush.FEATURES_BINARY:
        df_pert[bin_feat] = int(df_pert[bin_feat + "_1"])
        df_pert.drop([bin_feat + "_0", bin_feat + "_1"], axis=1, inplace=True)

elif mode == "pagegraph":
    for bin_feat in feature_names_pagegraph.FEATURES_BINARY:
        df_pert[bin_feat] = int(df_pert[bin_feat + "_1"])
        df_pert.drop([bin_feat + "_0", bin_feat + "_1"], axis=1, inplace=True)

if mode == "adgraph":
    # Handling unpertable categorical columns in pert
    cols_to_decode = ['FEATURE_NODE_CATEGORY', 'FEATURE_FIRST_PARENT_SIBLING_TAG_NAME' 'FEATURE_SECOND_PARENT_TAG_NAME', 'FEATURE_SECOND_PARENT_SIBLING_TAG_NAME']
    prefixes = [col + '_' for col in cols_to_decode]
    for prefix in prefixes:
        encoded_cols = [col for col in df_pert.columns if col.startswith(prefix)]
        df_pert.drop(encoded_cols, axis=1, inplace=True)
elif mode == "webgraph":
    # Handling unpertable categorical columns in pert
    cols_to_decode = ['content_policy_type']
    prefixes = [col + '_' for col in cols_to_decode]
    for prefix in prefixes:
        encoded_cols = [col for col in df_pert.columns if col.startswith(prefix)]
        df_pert.drop(encoded_cols, axis=1, inplace=True)
elif mode == "adflush":
    # Handling unpertable categorical columns in pert
    cols_to_decode = ['content_policy_type']
    prefixes = [col + '_' for col in cols_to_decode]
    for prefix in prefixes:
        encoded_cols = [col for col in df_pert.columns if col.startswith(prefix)]
        df_pert.drop(encoded_cols, axis=1, inplace=True)
elif mode == "pagegraph":
    # Handling unpertable categorical columns in pert
    cols_to_decode = ['FEATURE_RESOURCE_TYPE']
    prefixes = [col + '_' for col in cols_to_decode]
    for prefix in prefixes:
        encoded_cols = [col for col in df_pert.columns if col.startswith(prefix)]
        df_pert.drop(encoded_cols, axis=1, inplace=True)
else:
    # Handling unpertable categorical columns in pert
    cols_to_decode = []
    prefixes = [col + '_' for col in cols_to_decode]
    for prefix in prefixes:
        encoded_cols = [col for col in df_pert.columns if col.startswith(prefix)]
        df_pert.drop(encoded_cols, axis=1, inplace=True)

if mode == "adgraph":
    # Drop unpertable features
    columns_to_drop = df_pert.columns.difference(feature_names_adgraph.FEATURES_TO_PERTURBE)
    columns_to_drop = [col for col in columns_to_drop if not col.startswith("FEATURE_FIRST_PARENT_TAG_NAME_")]
    df_pert.drop(columns_to_drop, axis=1, inplace=True)

    df_pert.to_csv(csv_path + delta_name, index=False)

    # change categorical features to label encoding
    columns_cat_first_tag_name = [col for col in df_pert.columns if col.startswith("FEATURE_FIRST_PARENT_TAG_NAME_")]
    columns_cat_first_tag_name = columns_cat_first_tag_name[0]
    columns_to_encode = [columns_cat_first_tag_name]
    columns_to_encode_basic = ["FEATURE_FIRST_PARENT_TAG_NAME"]

    label_encoders = {}
    for column in columns_to_encode_basic:
        encoder = joblib.load(f'/yopo-artifact/scripts/crawler/adgraph/encoding_adgraph/{column}_encoder.joblib')
        label_encoders[column] = encoder

    for (column, column_basic) in zip(columns_to_encode, columns_to_encode_basic):
        label_encoder = label_encoders[column_basic]
        df_pert[column] = column.split("_TAG_NAME_")[-1]
        df_pert[column] = label_encoder.transform(df_pert[column])

        # change column name
        df_pert = df_pert.rename(columns={column: column_basic})


    # Inject perturbation to target csv file
    df_target = pd.read_csv(csv_path + csv_target_name)
    df_pert_dup = pd.concat([df_pert] * 2000, ignore_index=True)
    df_pert_dup_for_adv = pd.concat([df_pert] * 68292, ignore_index=True)

    # Read common features
    common_features_bin = feature_names_adgraph.FEATURES_TO_PERTURBE_BINARY
    common_features_num = feature_names_adgraph.FEATURES_TO_PERTURBE_NUMERIC
    common_features_cat = feature_names_adgraph.FEATURES_TO_PERTURBE_CAT
    remaining_features = list(set(df_target.columns) - set(df_pert_dup.columns))

elif mode == "webgraph":
    # Drop unpertable features
    columns_to_drop = df_pert.columns.difference(feature_names_webgraph.FEATURES_TO_PERTURBE)
    df_pert.drop(columns_to_drop, axis=1, inplace=True)
    df_pert.to_csv(csv_path + delta_name, index=False)

    # Inject perturbation to target csv file
    df_target = pd.read_csv(csv_path + csv_target_name)
    df_pert_dup = pd.concat([df_pert] * 2000, ignore_index=True)
    df_pert_dup_for_adv = pd.concat([df_pert] * 150870, ignore_index=True)

    # Read common features
    common_features_bin = feature_names_webgraph.FEATURES_TO_PERTURBE_BINARY
    common_features_num = feature_names_webgraph.FEATURES_TO_PERTURBE_NUMERIC
    common_features_cat = feature_names_webgraph.FEATURES_TO_PERTURBE_CAT
    remaining_features = list(set(df_target.columns) - set(df_pert_dup.columns))

elif mode == "adflush":
    # Drop unpertable features
    columns_to_drop = df_pert.columns.difference(feature_names_adflush.FEATURES_TO_PERTURBE)
    df_pert.drop(columns_to_drop, axis=1, inplace=True)
    df_pert.to_csv(csv_path + delta_name, index=False)

    # Inject perturbation to target csv file
    df_target = pd.read_csv(csv_path + csv_target_name)
    df_pert_dup = pd.concat([df_pert] * 2000, ignore_index=True)
    df_pert_dup_for_adv = pd.concat([df_pert] * 150870, ignore_index=True)

    # Read common features
    common_features_bin = feature_names_adflush.FEATURES_TO_PERTURBE_BINARY
    common_features_num = feature_names_adflush.FEATURES_TO_PERTURBE_NUMERIC
    common_features_cat = feature_names_adflush.FEATURES_TO_PERTURBE_CAT
    remaining_features = list(set(df_target.columns) - set(df_pert_dup.columns))
    
elif mode == "pagegraph":
    # Drop unpertable features
    columns_to_drop = df_pert.columns.difference(feature_names_pagegraph.FEATURES_TO_PERTURBE)
    df_pert.drop(columns_to_drop, axis=1, inplace=True)
    df_pert.to_csv(csv_path + delta_name, index=False)

    # Inject perturbation to target csv file
    df_target = pd.read_csv(csv_path + csv_target_name)
    df_pert_dup = pd.concat([df_pert] * 2000, ignore_index=True)
    df_pert_dup_for_adv = pd.concat([df_pert] * 150870, ignore_index=True)

    # Read common features
    common_features_bin = feature_names_pagegraph.FEATURES_TO_PERTURBE_BINARY
    common_features_num = feature_names_pagegraph.FEATURES_TO_PERTURBE_NUMERIC
    common_features_cat = feature_names_pagegraph.FEATURES_TO_PERTURBE_CAT
    remaining_features = list(set(df_target.columns) - set(df_pert_dup.columns))

df_injected = pd.DataFrame()
df_injected[common_features_num] = df_target[common_features_num] + df_pert_dup[common_features_num]
df_injected[common_features_bin] = df_pert_dup[common_features_bin]
df_injected[common_features_cat] = df_pert_dup[common_features_cat]
df_injected[remaining_features] = df_target[remaining_features]
df_injected["CLASS"] = 1

# Reordering features
df_target = pd.read_csv(csv_path + csv_target_name)
df_injected = df_injected.reindex(columns=df_target.columns)

# Save the updated CSV file
df_injected.to_csv(csv_path + "bin_reverse_encoded_" + out_name, index=False)

print('  Done.')
