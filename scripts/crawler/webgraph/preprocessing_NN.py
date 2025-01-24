import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import feature_names_webgraph

BASE_DIR = "/yopo-artifact/data"

# Load CSV file into a DataFrame
df = pd.read_csv(BASE_DIR + "/dataset/from_webgraph/features_raw_except_target.csv")

cols_to_encode_cat_bin = feature_names_webgraph.FEATURES_CATEGORICAL + feature_names_webgraph.FEATURES_BINARY

# For One-hot encoding for categorical features
df_encoded = pd.get_dummies(df, columns=cols_to_encode_cat_bin)

# Add One-hot encoded features
df_final = pd.concat([df_encoded.drop('CLASS', axis=1), df_encoded['CLASS']], axis=1)

# change AD to 1, NonAD to 0
df_final['CLASS'] = df_final['CLASS'].replace({True: 1, False:0})

# Save
df_final.to_csv(BASE_DIR + "/dataset/from_webgraph/features_nn.csv", index=False)
