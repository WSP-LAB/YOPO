# DC
STRUCT_WEIGHT = 1
CONTENT_WEIGHT = 1

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

COST_FLOW_EASY = 1
COST_FLOW_MID = 2
COST_FLOW_HARD = 2

FEATURES_COST_WEBGRAPH_DC = {
    "num_nodes" : COST_STRUCT_EASY_EASY,
    "num_edges" : COST_STRUCT_EASY_EASY,
    "in_out_degree" : COST_STRUCT_EASY_EASY,
    "out_degree" : COST_STRUCT_EASY_EASY,
    "average_degree_connectivity" : COST_STRUCT_HARD,
    "ascendant_has_ad_keyword_0" : COST_STRUCT_HARD / 2,
    "ascendant_has_ad_keyword_1" : COST_STRUCT_HARD / 2,
    
    "num_get_storage" : COST_FLOW_MID,
    "num_get_cookie" : COST_FLOW_MID,
    "num_set_storage" : COST_FLOW_MID,
    "num_set_cookie" : COST_FLOW_MID,
    "indirect_all_out_degree" : COST_FLOW_EASY,
    "indirect_mean_out_weights" : COST_FLOW_MID,
    "indirect_mean_in_weights" : COST_FLOW_MID,
    "indirect_mean_out_weights" : COST_FLOW_MID,
    "num_requests_sent" : COST_FLOW_EASY,
    "num_requests_received" : COST_FLOW_EASY,
    "num_redirects_sent" : COST_FLOW_EASY,
    "num_redirects_rec" : COST_FLOW_EASY,
    "max_depth_redirect" : COST_FLOW_EASY,

    "url_length" : COST_CONTENT_EASY_EASY,
    "keyword_raw_present_0" : COST_CONTENT_HARD / 2,
    "keyword_raw_present_1" : COST_CONTENT_HARD / 2,
    "keyword_char_present_0" : COST_CONTENT_HARD / 2,
    "keyword_char_present_1" : COST_CONTENT_HARD / 2,
    "semicolon_in_query_0" : COST_CONTENT_EASY / 2,
    "semicolon_in_query_1" : COST_CONTENT_EASY / 2,
    "base_domain_in_query_0" : COST_CONTENT_EASY / 2,
    "base_domain_in_query_1" : COST_CONTENT_EASY / 2,
    "ad_size_in_qs_present_0" : COST_CONTENT_HARD / 2,
    "ad_size_in_qs_present_1" : COST_CONTENT_HARD / 2,
    "screen_size_present_0" : COST_CONTENT_MID / 2,
    "screen_size_present_1" : COST_CONTENT_MID / 2,
    "ad_size_present_0" : COST_CONTENT_HARD / 2,
    "ad_size_present_1" : COST_CONTENT_HARD / 2,
    "is_third_party_0" : COST_CONTENT_HARD /2,
    "is_third_party_1" : COST_CONTENT_HARD /2,
    "is_valid_qs_0" : COST_CONTENT_MID / 2,
    "is_valid_qs_1" : COST_CONTENT_MID / 2,
    
    "is_third_party_0" : COST_STRUCT_EASY,
    "is_third_party_1" : COST_STRUCT_EASY
}

# HCC
STRUCT_WEIGHT = 1
CONTENT_WEIGHT = 10

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

COST_FLOW_EASY = 1
COST_FLOW_MID = 2
COST_FLOW_HARD = 2

FEATURES_COST_WEBGRAPH_HCC = {
    "num_nodes" : COST_STRUCT_EASY_EASY,
    "num_edges" : COST_STRUCT_EASY_EASY,
    "in_out_degree" : COST_STRUCT_EASY_EASY,
    "out_degree" : COST_STRUCT_EASY_EASY,
    "average_degree_connectivity" : COST_STRUCT_HARD,
    "ascendant_has_ad_keyword_0" : COST_STRUCT_HARD / 2,
    "ascendant_has_ad_keyword_1" : COST_STRUCT_HARD / 2,
    
    "num_get_storage" : COST_FLOW_MID,
    "num_get_cookie" : COST_FLOW_MID,
    "num_set_storage" : COST_FLOW_MID,
    "num_set_cookie" : COST_FLOW_MID,
    "indirect_all_out_degree" : COST_FLOW_EASY,
    "indirect_mean_out_weights" : COST_FLOW_MID,
    "indirect_mean_in_weights" : COST_FLOW_MID,
    "indirect_mean_out_weights" : COST_FLOW_MID,
    "num_requests_sent" : COST_FLOW_EASY,
    "num_requests_received" : COST_FLOW_EASY,
    "num_redirects_sent" : COST_FLOW_EASY,
    "num_redirects_rec" : COST_FLOW_EASY,
    "max_depth_redirect" : COST_FLOW_EASY,

    "url_length" : COST_CONTENT_EASY_EASY,
    "keyword_raw_present_0" : COST_CONTENT_HARD / 2,
    "keyword_raw_present_1" : COST_CONTENT_HARD / 2,
    "keyword_char_present_0" : COST_CONTENT_HARD / 2,
    "keyword_char_present_1" : COST_CONTENT_HARD / 2,
    "semicolon_in_query_0" : COST_CONTENT_EASY / 2,
    "semicolon_in_query_1" : COST_CONTENT_EASY / 2,
    "base_domain_in_query_0" : COST_CONTENT_EASY / 2,
    "base_domain_in_query_1" : COST_CONTENT_EASY / 2,
    "ad_size_in_qs_present_0" : COST_CONTENT_HARD / 2,
    "ad_size_in_qs_present_1" : COST_CONTENT_HARD / 2,
    "screen_size_present_0" : COST_CONTENT_MID / 2,
    "screen_size_present_1" : COST_CONTENT_MID / 2,
    "ad_size_present_0" : COST_CONTENT_HARD / 2,
    "ad_size_present_1" : COST_CONTENT_HARD / 2,
    "is_third_party_0" : COST_CONTENT_HARD /2,
    "is_third_party_1" : COST_CONTENT_HARD /2,
    "is_valid_qs_0" : COST_CONTENT_MID / 2,
    "is_valid_qs_1" : COST_CONTENT_MID / 2,
    
    "is_third_party_0" : COST_STRUCT_EASY,
    "is_third_party_1" : COST_STRUCT_EASY
}

# HSC
STRUCT_WEIGHT = 10
CONTENT_WEIGHT = 1

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

COST_FLOW_EASY = 1
COST_FLOW_MID = 2
COST_FLOW_HARD = 2

FEATURES_COST_WEBGRAPH_HSC = {
    "num_nodes" : COST_STRUCT_EASY_EASY,
    "num_edges" : COST_STRUCT_EASY_EASY,
    "in_out_degree" : COST_STRUCT_EASY_EASY,
    "out_degree" : COST_STRUCT_EASY_EASY,
    "average_degree_connectivity" : COST_STRUCT_HARD,
    "ascendant_has_ad_keyword_0" : COST_STRUCT_HARD / 2,
    "ascendant_has_ad_keyword_1" : COST_STRUCT_HARD / 2,
    
    "num_get_storage" : COST_FLOW_MID,
    "num_get_cookie" : COST_FLOW_MID,
    "num_set_storage" : COST_FLOW_MID,
    "num_set_cookie" : COST_FLOW_MID,
    "indirect_all_out_degree" : COST_FLOW_EASY,
    "indirect_mean_out_weights" : COST_FLOW_MID,
    "indirect_mean_in_weights" : COST_FLOW_MID,
    "indirect_mean_out_weights" : COST_FLOW_MID,
    "num_requests_sent" : COST_FLOW_EASY,
    "num_requests_received" : COST_FLOW_EASY,
    "num_redirects_sent" : COST_FLOW_EASY,
    "num_redirects_rec" : COST_FLOW_EASY,
    "max_depth_redirect" : COST_FLOW_EASY,

    "url_length" : COST_CONTENT_EASY_EASY,
    "keyword_raw_present_0" : COST_CONTENT_HARD / 2,
    "keyword_raw_present_1" : COST_CONTENT_HARD / 2,
    "keyword_char_present_0" : COST_CONTENT_HARD / 2,
    "keyword_char_present_1" : COST_CONTENT_HARD / 2,
    "semicolon_in_query_0" : COST_CONTENT_EASY / 2,
    "semicolon_in_query_1" : COST_CONTENT_EASY / 2,
    "base_domain_in_query_0" : COST_CONTENT_EASY / 2,
    "base_domain_in_query_1" : COST_CONTENT_EASY / 2,
    "ad_size_in_qs_present_0" : COST_CONTENT_HARD / 2,
    "ad_size_in_qs_present_1" : COST_CONTENT_HARD / 2,
    "screen_size_present_0" : COST_CONTENT_MID / 2,
    "screen_size_present_1" : COST_CONTENT_MID / 2,
    "ad_size_present_0" : COST_CONTENT_HARD / 2,
    "ad_size_present_1" : COST_CONTENT_HARD / 2,
    "is_third_party_0" : COST_CONTENT_HARD /2,
    "is_third_party_1" : COST_CONTENT_HARD /2,
    "is_valid_qs_0" : COST_CONTENT_MID / 2,
    "is_valid_qs_1" : COST_CONTENT_MID / 2,
    
    "is_third_party_0" : COST_STRUCT_EASY,
    "is_third_party_1" : COST_STRUCT_EASY
}