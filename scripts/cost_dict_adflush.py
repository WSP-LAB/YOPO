# DC
STRUCT_WEIGHT = 1
CONTENT_WEIGHT = 1
JAVASCRIPT_WEIGHT = 1

COST_STRUCT_EASY_EASY = 0.1 * STRUCT_WEIGHT
COST_STRUCT_EASY = 1 * STRUCT_WEIGHT
COST_STRUCT_MID_EASY = 2 * STRUCT_WEIGHT
COST_STRUCT_MID = 2 * STRUCT_WEIGHT
COST_STRUCT_HARD = 3 * STRUCT_WEIGHT

COST_CONTENT_EASY_EASY = 0.2 * CONTENT_WEIGHT
COST_CONTENT_EASY = 1 * CONTENT_WEIGHT
COST_CONTENT_MID_EASY = 0.2 * CONTENT_WEIGHT
COST_CONTENT_MID = 2 * CONTENT_WEIGHT
COST_CONTENT_HARD = 3 * CONTENT_WEIGHT

COST_JS_EASY = 1 * JAVASCRIPT_WEIGHT
COST_JS_MID = 2 * JAVASCRIPT_WEIGHT
COST_JS_HARD = 3 * JAVASCRIPT_WEIGHT

COST_FLOW_EASY = 1
COST_FLOW_MID = 2
COST_FLOW_HARD = 2

FEATURES_COST_ADFLUSH_DC = {
    "num_nodes" : COST_STRUCT_EASY_EASY,
    "num_edges" : COST_STRUCT_EASY_EASY,
    "in_out_degree" : COST_STRUCT_EASY_EASY,
    "average_degree_connectivity" : COST_STRUCT_HARD,
    "ascendant_has_ad_keyword_0" : COST_STRUCT_HARD / 2,
    "ascendant_has_ad_keyword_1" : COST_STRUCT_HARD / 2,

    "url_length" : COST_CONTENT_MID_EASY,
    "keyword_raw_present_0" : COST_CONTENT_HARD / 2,
    "keyword_raw_present_1" : COST_CONTENT_HARD / 2,
    "is_third_party_0" : COST_CONTENT_HARD /2,
    "is_third_party_1" : COST_CONTENT_HARD /2,

    "brackettodot" : COST_JS_EASY,
    "num_get_storage" : COST_FLOW_MID,
    "num_set_storage" : COST_FLOW_MID,
    "num_get_cookie" : COST_FLOW_MID,
    "num_requests_sent" : COST_FLOW_EASY,
    "avg_ident" : COST_JS_MID,
    "avg_charperline" : COST_JS_MID,

    "ng_0_0_2" : COST_JS_EASY,
    "ng_0_15_15" : COST_JS_EASY,
    "ng_2_13_2" : COST_JS_EASY,
    "ng_15_0_3" : COST_JS_EASY,
    "ng_15_0_15" : COST_JS_EASY,
    "ng_15_15_15" : COST_JS_EASY,
    
}

# HJC
STRUCT_WEIGHT = 1
CONTENT_WEIGHT = 1
JAVASCRIPT_WEIGHT = 10

COST_STRUCT_EASY_EASY = 0.1 * STRUCT_WEIGHT
COST_STRUCT_EASY = 1 * STRUCT_WEIGHT
COST_STRUCT_MID_EASY = 2 * STRUCT_WEIGHT
COST_STRUCT_MID = 2 * STRUCT_WEIGHT
COST_STRUCT_HARD = 3 * STRUCT_WEIGHT

COST_CONTENT_EASY_EASY = 0.2 * CONTENT_WEIGHT
COST_CONTENT_EASY = 1 * CONTENT_WEIGHT
COST_CONTENT_MID_EASY = 0.2 * CONTENT_WEIGHT
COST_CONTENT_MID = 2 * CONTENT_WEIGHT
COST_CONTENT_HARD = 3 * CONTENT_WEIGHT

COST_JS_EASY = 1 * JAVASCRIPT_WEIGHT
COST_JS_MID = 2 * JAVASCRIPT_WEIGHT
COST_JS_HARD = 3 * JAVASCRIPT_WEIGHT

COST_FLOW_EASY = 1
COST_FLOW_MID = 2
COST_FLOW_HARD = 2

FEATURES_COST_ADFLUSH_HJC = {
    "num_nodes" : COST_STRUCT_EASY_EASY,
    "num_edges" : COST_STRUCT_EASY_EASY,
    "in_out_degree" : COST_STRUCT_EASY_EASY,
    "average_degree_connectivity" : COST_STRUCT_HARD,
    "ascendant_has_ad_keyword_0" : COST_STRUCT_HARD / 2,
    "ascendant_has_ad_keyword_1" : COST_STRUCT_HARD / 2,

    "url_length" : COST_CONTENT_MID_EASY,
    "keyword_raw_present_0" : COST_CONTENT_HARD / 2,
    "keyword_raw_present_1" : COST_CONTENT_HARD / 2,
    "is_third_party_0" : COST_CONTENT_HARD /2,
    "is_third_party_1" : COST_CONTENT_HARD /2,

    "brackettodot" : COST_JS_EASY,
    "num_get_storage" : COST_FLOW_MID,
    "num_set_storage" : COST_FLOW_MID,
    "num_get_cookie" : COST_FLOW_MID,
    "num_requests_sent" : COST_FLOW_EASY,
    "avg_ident" : COST_JS_MID,
    "avg_charperline" : COST_JS_MID,

    "ng_0_0_2" : COST_JS_EASY,
    "ng_0_15_15" : COST_JS_EASY,
    "ng_2_13_2" : COST_JS_EASY,
    "ng_15_0_3" : COST_JS_EASY,
    "ng_15_0_15" : COST_JS_EASY,
    "ng_15_15_15" : COST_JS_EASY,
    
}


# HCC

STRUCT_WEIGHT = 1
CONTENT_WEIGHT = 10
JAVASCRIPT_WEIGHT = 1

COST_STRUCT_EASY_EASY = 0.1 * STRUCT_WEIGHT
COST_STRUCT_EASY = 1 * STRUCT_WEIGHT
COST_STRUCT_MID_EASY = 2 * STRUCT_WEIGHT
COST_STRUCT_MID = 2 * STRUCT_WEIGHT
COST_STRUCT_HARD = 3 * STRUCT_WEIGHT

COST_CONTENT_EASY_EASY = 0.2 * CONTENT_WEIGHT
COST_CONTENT_EASY = 1 * CONTENT_WEIGHT
COST_CONTENT_MID_EASY = 0.2 * CONTENT_WEIGHT
COST_CONTENT_MID = 2 * CONTENT_WEIGHT
COST_CONTENT_HARD = 3 * CONTENT_WEIGHT

COST_JS_EASY = 1 * JAVASCRIPT_WEIGHT
COST_JS_MID = 2 * JAVASCRIPT_WEIGHT
COST_JS_HARD = 3 * JAVASCRIPT_WEIGHT

COST_FLOW_EASY = 1
COST_FLOW_MID = 2
COST_FLOW_HARD = 2

FEATURES_COST_ADFLUSH_HCC = {
    "num_nodes" : COST_STRUCT_EASY_EASY,
    "num_edges" : COST_STRUCT_EASY_EASY,
    "in_out_degree" : COST_STRUCT_EASY_EASY,
    "average_degree_connectivity" : COST_STRUCT_HARD,
    "ascendant_has_ad_keyword_0" : COST_STRUCT_HARD / 2,
    "ascendant_has_ad_keyword_1" : COST_STRUCT_HARD / 2,

    "url_length" : COST_CONTENT_MID_EASY,
    "keyword_raw_present_0" : COST_CONTENT_HARD / 2,
    "keyword_raw_present_1" : COST_CONTENT_HARD / 2,
    "is_third_party_0" : COST_CONTENT_HARD /2,
    "is_third_party_1" : COST_CONTENT_HARD /2,

    "brackettodot" : COST_JS_EASY,
    "num_get_storage" : COST_FLOW_MID,
    "num_set_storage" : COST_FLOW_MID,
    "num_get_cookie" : COST_FLOW_MID,
    "num_requests_sent" : COST_FLOW_EASY,
    "avg_ident" : COST_JS_MID,
    "avg_charperline" : COST_JS_MID,

    "ng_0_0_2" : COST_JS_EASY,
    "ng_0_15_15" : COST_JS_EASY,
    "ng_2_13_2" : COST_JS_EASY,
    "ng_15_0_3" : COST_JS_EASY,
    "ng_15_0_15" : COST_JS_EASY,
    "ng_15_15_15" : COST_JS_EASY,
    
}