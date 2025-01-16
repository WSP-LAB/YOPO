FEATURES_TO_PERTURBE = [
    "url_length",
    "brackettodot",
    "keyword_raw_present",
    "num_get_storage",
    "num_set_storage",
    "num_get_cookie",
    "num_requests_sent",
    "avg_ident",
    "avg_charperline",

    "ng_0_0_2",
    "ng_0_15_15",
    "ng_2_13_2",
    "ng_15_0_3",
    "ng_15_0_15",
    "ng_15_15_15",
]

FEATURES_TO_PERTURBE_NUMERIC = [
    "url_length",
    "brackettodot",
    "num_get_storage",
    "num_set_storage",
    "num_get_cookie",
    "num_requests_sent",
    "avg_ident",
    "avg_charperline",

    "ng_0_0_2",
    "ng_0_15_15",
    "ng_2_13_2",
    "ng_15_0_3",
    "ng_15_0_15",
    "ng_15_15_15",
]

FEATURES_TO_PERTURBE_BINARY = [
    "keyword_raw_present",
]

FEATURES_TO_PERTURBE_CAT = [
]

FEATURES_TO_PERTURBE_BINARY_ALL = [
    "keyword_raw_present_0",
    "keyword_raw_present_1",
]

FEATURES_TO_PERTURBE_CAT_ALL = [
]

FEATURES_TO_INCREASE_ONLY = [
    "num_get_storage",
    "num_set_storage",
    "num_get_cookie",
    "num_requests_sent",

    "ng_0_0_2",
    "ng_0_15_15",
    "ng_2_13_2",
    "ng_15_0_3",
    "ng_15_0_15",
    "ng_15_15_15",
]

FEATURES_CATEGORICAL = [
    "content_policy_type",
]

FEATURES_TO_EXCLUDE_ADFLUSH = [
    "visit_id", 
    "name",
    "top_level_url"
]


# Categorical, Binary features lists

# Binary
FEATURES_BINARY = [
    "is_third_party",
    "keyword_raw_present",
]

keyword_raw_present = [
    "keyword_raw_present_0",
    "keyword_raw_present_1"
]

is_third_party = [
    "is_third_party_0",
    "is_third_party_1"
]