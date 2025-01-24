import torch
import os 
import pandas as pd 
import numpy as np
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, make_scorer
from sklearn.utils import resample
from joblib import dump, load
import pickle

csv_path = "/yopo-artifact/data/dataset/"
csv_name = "from_webgraph/features_rf.csv"
to_exclude = ["top_level_url", "visit_id", "name"]
# os.getcwd()
data = pd.read_csv(csv_path + csv_name)
#data = data.sample(frac=1) #row shuffle
# print(type(data))
# print(data.head())

nCar = data.shape[0]
nVar = data.shape[1]
print('nCar: %d' % nCar, 'nVar: %d' % nVar )

X = data.drop("CLASS", axis=1)
# X = data.drop(to_exclude, axis=1)
y = data["CLASS"]

count_class_0, count_class_1 = data['CLASS'].value_counts()
print("-----")
print("NonAD (before dropping) : {}".format(count_class_0))
print("AD (before dropping) : {}".format(count_class_1))

if count_class_0 > count_class_1 * 2.3:
    count_class_0_to_keep = int(count_class_1 * 2.3)
    class_0_indices = data[data['CLASS'] == 0].index
    random_indices = np.random.choice(class_0_indices, size=count_class_0_to_keep, replace=False)
    class_0_sample = data.loc[random_indices]
    data_sampled = pd.concat([class_0_sample, data[data['CLASS'] == 1]])

else:
    count_class_1_to_keep = int(count_class_0 * 0.4286)
    class_1_indices = data[data['CLASS'] == 1].index
    random_indices = np.random.choice(class_1_indices, size=count_class_1_to_keep, replace=False)
    class_1_sample = data.loc[random_indices]
    data_sampled = pd.concat([class_1_sample, data[data['CLASS'] == 0]])

data_sampled = data_sampled.reset_index(drop=True)

X = data_sampled.drop("CLASS", axis=1)
y = data_sampled["CLASS"]
# X = data_sampled.drop(to_exclude, axis=1)

count_class_0, count_class_1 = data_sampled['CLASS'].value_counts()
print("-----")
print("NonAD (after dropping) : {}".format(count_class_0))
print("AD (after dropping) : {}".format(count_class_1))
print("Ratio : {:.0f} : {:.0f}".format(count_class_0 / (count_class_0 + count_class_1) * 100, count_class_1 / (count_class_0 + count_class_1) * 100))


clf = RandomForestClassifier(n_estimators=100, random_state=41)

# Define the stratified cross-validation object
skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=41)

best_accuracy = 0.0
best_clf = None

accuracy_history = []
precision_history = []
recall_history = []

# For each fold
for fold, (train_index, test_index) in enumerate(skf.split(X, y)):
    print("Training - fold", fold)
    
    fold_train_y = y[train_index]
    fold_test_y = y[test_index]
    for class_label in np.unique(y):
        train_count = np.count_nonzero(fold_train_y == class_label)
        test_count = np.count_nonzero(fold_test_y == class_label)

    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y.iloc[train_index], y.iloc[test_index]
    
    X_train = X_train.drop(to_exclude, axis=1)
    X_test = X_test.drop(to_exclude, axis=1)
   
    # Train
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    
    accuracy_history.append(accuracy_score(y_test, y_pred))
    precision_history.append(precision_score(y_test, y_pred))
    recall_history.append(recall_score(y_test, y_pred))
    
    if accuracy_score(y_test, y_pred) > best_accuracy:
        best_accuracy = accuracy_score(y_test, y_pred)
        best_clf = clf

print("Average accuracy:", np.mean(accuracy_history))
print("Average precision:", np.mean(precision_history))
print("Average recall:", np.mean(recall_history))

# Save
os.makedirs(os.path.dirname('/yopo-artifact/data/dataset/from_webgraph/saved_model_webgraph/rf_model_30perc.pt'), exist_ok=True)
if best_clf is not None:
    with open('/yopo-artifact/data/dataset/from_webgraph/saved_model_webgraph/rf_model_30perc.pt', 'wb') as f:
        pickle.dump(best_clf, f)
