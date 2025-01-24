FEATURES_TO_PERTURBE = [
    "num_nodes",
    "num_edges",
    "url_length",
    "keyword_raw_present",
    "keyword_char_present",
    "semicolon_in_query",
    "base_domain_in_query",
    "ad_size_in_qs_present",
    "in_out_degree",
    "out_degree",
    "ascendant_has_ad_keyword",
    "screen_size_present",
    "ad_size_present",
    "average_degree_connectivity",
    "is_valid_qs",
    #
    "num_requests_sent",
    "num_requests_received",
    # "num_redirects_sent",
    # "num_redirects_rec",
    # "max_depth_redirect",
    
    "num_get_storage",
    "num_get_cookie",
    "num_set_storage",
    "num_set_cookie",
    "indirect_mean_in_weights",
    "indirect_mean_out_weights",
    
    # "num_script_predecessors",
    # "num_script_successors",
    
    # "indirect_in_degree",
    # "indirect_out_degree",
    # "indirect_ancestors",
    # "indirect_descendants",
    # "indirect_closeness_centrality",
    # "indirect_average_degree_connectivity",
    # "indirect_eccentricity",
    # "indirect_min_in_weights",
    # "indirect_max_in_weights",
    # "indirect_min_out_weights",
    # "indirect_max_out_weights",

    # "indirect_all_in_degree",
    "indirect_all_out_degree",
    # "indirect_all_ancestors",
    # "indirect_all_descendants",
    # "indirect_all_closeness_centrality",
    # "indirect_all_average_degree_connectivity",
    # "indirect_all_eccentricity",
    
    # "num_set_get_src",
    # "num_set_mod_src",
    # "num_set_url_src",
    # "num_get_url_src",
    # "num_set_get_dst",
    # "num_set_mod_dst",
    # "num_set_url_dst",is_third_partyis
    # "num_get_url_dst",
    
    # "is_third_party",
]

FEATURES_TO_PERTURBE_NUMERIC = [
    "num_nodes",
    "num_edges",
    "url_length",
    "in_out_degree",
    "out_degree",
    "average_degree_connectivity",
    #
    "num_requests_sent",
    "num_requests_received",
    # "num_redirects_sent",
    # "num_redirects_rec",
    # "max_depth_redirect",
    
    # "num_script_predecessors",
    # "num_script_successors",
    
    # "indirect_in_degree",
    # "indirect_out_degree",
    # "indirect_ancestors",
    # "indirect_descendants",
    # "indirect_closeness_centrality",
    # "indirect_average_degree_connectivity",
    # "indirect_eccentricity",
    # "indirect_min_in_weights",
    # "indirect_max_in_weights",
    # "indirect_min_out_weights",
    # "indirect_max_out_weights",
    
    # "indirect_all_in_degree",
    "indirect_all_out_degree",
    # "indirect_all_ancestors",
    # "indirect_all_descendants",
    # "indirect_all_closeness_centrality",
    # "indirect_all_average_degree_connectivity",
    # "indirect_all_eccentricity",
    
    "num_get_storage",
    "num_get_cookie",
    "num_set_storage",
    "num_set_cookie",
    "indirect_mean_in_weights",
    "indirect_mean_out_weights",
    
    # "num_set_get_src",
    # "num_set_mod_src",
    # "num_set_url_src",
    # "num_get_url_src",
    # "num_set_get_dst",
    # "num_set_mod_dst",
    # "num_set_url_dst",
    # "num_get_url_dst",
]

FEATURES_TO_PERTURBE_BINARY = [
    "keyword_raw_present",
    "keyword_char_present",
    "semicolon_in_query",
    "base_domain_in_query",
    "ad_size_in_qs_present",
    "ascendant_has_ad_keyword",
    "screen_size_present",
    "ad_size_present",
    "is_valid_qs",
    #
    # "is_third_party",
]

FEATURES_TO_PERTURBE_CAT = [
]

FEATURES_TO_PERTURBE_BINARY_ALL = [
    "keyword_raw_present_0",
    "keyword_raw_present_1",
    "keyword_char_present_0",
    "keyword_char_present_1",
    "semicolon_in_query_0",
    "semicolon_in_query_1",
    "base_domain_in_query_0",
    "base_domain_in_query_1",
    "ad_size_in_qs_present_0",
    "ad_size_in_qs_present_1",
    "ascendant_has_ad_keyword_0",
    "ascendant_has_ad_keyword_1",
    "screen_size_present_0",
    "screen_size_present_1",
    "ad_size_present_0",
    "ad_size_present_1",
    "is_valid_qs_0",
    "is_valid_qs_1",
    #
    # "is_third_party_0",
    # "is_third_party_1",
]

FEATURES_TO_PERTURBE_CAT_ALL = [
]

FEATURES_TO_INCREASE_ONLY = [
    "num_nodes",
    "num_edges",
    "in_out_degree",
    "out_degree",
    # "url_length"
    #
    "num_requests_sent",
    "num_requests_received",
    # "num_redirects_sent",
    # "num_redirects_rec",
    # "max_depth_redirect",
    
    # "num_script_predecessors",
    # "num_script_successors",
    
    # "indirect_in_degree",
    # "indirect_out_degree",
    # "indirect_ancestors",
    # "indirect_descendants",
    # "indirect_closeness_centrality",
    # "indirect_average_degree_connectivity",
    # "indirect_eccentricity",
    # "indirect_min_in_weights",
    # "indirect_max_in_weights",
    # "indirect_min_out_weights",
    # "indirect_max_out_weights",
    
    # "indirect_all_in_degree",
    "indirect_all_out_degree",
    # "indirect_all_ancestors",
    # "indirect_all_descendants",
    # "indirect_all_closeness_centrality",
    # "indirect_all_average_degree_connectivity",
    # "indirect_all_eccentricity",
    
    # "num_set_get_src",
    # "num_set_mod_src",
    # "num_set_url_src",
    # "num_get_url_src",
    # "num_set_get_dst",
    # "num_set_mod_dst",
    # "num_set_url_dst",
    # "num_get_url_dst",
    
    "num_get_storage",
    "num_get_cookie",
    "num_set_storage",
    "num_set_cookie",
    "indirect_mean_in_weights",
    "indirect_mean_out_weights",
]

FEATURES_CATEGORICAL = [
    "content_policy_type",
]

FEATURES_TO_EXCLUDE_WEBGRAPH = [
    "visit_id", 
    "name",
    "top_level_url"
]


# Categorical, Binary features lists

# Binary
FEATURES_BINARY = [
    "is_parent_script",
    "is_ancestor_script",
    "ascendant_has_ad_keyword",
    "is_eval_or_function",
    "descendant_of_eval_or_function",
    "ascendant_script_has_eval_or_function",
    "ascendant_script_has_fp_keyword",
    "is_subdomain",
    "is_valid_qs",
    "is_third_party",
    "base_domain_in_query",
    "semicolon_in_query",
    "screen_size_present",
    "ad_size_present",
    "ad_size_in_qs_present",
    "keyword_raw_present",
    "keyword_char_present",
]

is_parent_script = [
    "is_parent_script_0",
    "is_parent_script_1"
]

is_ancestor_script = [
    "is_ancestor_script_0",
    "is_ancestor_script_1"
]

ascendant_has_ad_keyword = [
    "ascendant_has_ad_keyword_0",
    "ascendant_has_ad_keyword_1"
]

is_eval_or_function = [
    "is_eval_or_function_0",
    "is_eval_or_function_1"
]

descendant_of_eval_or_function = [
    "descendant_of_eval_or_function_0",
    "descendant_of_eval_or_function_1"
]

ascendant_script_has_eval_or_function = [
    "ascendant_script_has_eval_or_function_0",
    "ascendant_script_has_eval_or_function_1"
]

ascendant_script_has_fp_keyword = [
    "ascendant_script_has_fp_keyword_0",
    "ascendant_script_has_fp_keyword_1"
]

is_subdomain = [
    "is_subdomain_0",
    "is_subdomain_1"
]

is_valid_qs = [
    "is_valid_qs_0",
    "is_valid_qs_1"
]

is_third_party = [
    "is_third_party_0",
    "is_third_party_1"
]

base_domain_in_query = [
    "base_domain_in_query_0",
    "base_domain_in_query_1"
]

semicolon_in_query = [
    "semicolon_in_query_0",
    "semicolon_in_query_1"
]
 
screen_size_present = [
    "screen_size_present_0,"
    "screen_size_present_1"
]
 
ad_size_present = [
    "ad_size_present_0",
    "ad_size_present_1"
]

FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT = [
    "ad_size_in_qs_present_0",
    "ad_size_in_qs_present_1"
]

keyword_raw_present = [
    "keyword_raw_present_0",
    "keyword_raw_present_1"
]

keyword_char_present = [
    "keyword_char_present_0",
    "keyword_char_present_1"
]

is_third_party = [
    "is_third_party_0",
    "is_third_party_1"
]
