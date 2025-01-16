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

FEATURES_COST_DC = {
    "FEATURE_GRAPH_NODES" : COST_STRUCT_EASY_EASY,
    "FEATURE_GRAPH_EDGES" : COST_STRUCT_EASY_EASY,
    "FEATURE_INBOUND_OUTBOUND_CONNECTIONS" : COST_STRUCT_EASY_EASY,
    "FEATURE_OUTBOUND_CONNECTIONS" : COST_STRUCT_EASY_EASY,
    "FEATURE_FIRST_NUMBER_OF_SIBLINGS" : COST_STRUCT_EASY_EASY,
    "FEATURE_FIRST_PARENT_NUMBER_OF_SIBLINGS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_INBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_OUTBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_INBOUND_OUTBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_AVERAGE_DEGREE_CONNECTIVITY" : COST_STRUCT_HARD,
    "FEATURE_AVERAGE_DEGREE_CONNECTIVITY" : COST_STRUCT_HARD,
    "FEATURE_ASCENDANTS_AD_KEYWORD_0" : COST_STRUCT_HARD / 2,
    "FEATURE_ASCENDANTS_AD_KEYWORD_1" : COST_STRUCT_HARD / 2,
    "FEATURE_FIRST_PARENT_SIBLING_AD_ATTRIBUTE_0" : COST_STRUCT_HARD / 2,
    "FEATURE_FIRST_PARENT_SIBLING_AD_ATTRIBUTE_1" : COST_STRUCT_HARD / 2,

    "FEATURE_URL_LENGTH" : COST_CONTENT_EASY_EASY,
    "FEATURE_AD_KEYWORD_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_KEYWORD_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SPECIAL_CHAR_AD_KEYWORD_0" : COST_CONTENT_HARD / 2,
    "FEATURE_SPECIAL_CHAR_AD_KEYWORD_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SEMICOLON_PRESENT_0" : COST_CONTENT_EASY / 2,
    "FEATURE_SEMICOLON_PRESENT_1" : COST_CONTENT_EASY / 2,
    "FEATURE_BASE_DOMAIN_IN_QS_0" : COST_CONTENT_EASY / 2,
    "FEATURE_BASE_DOMAIN_IN_QS_1" : COST_CONTENT_EASY / 2,
    "FEATURE_AD_DIMENSIONS_IN_QS_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_DIMENSIONS_IN_QS_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SCREEN_DIMENSIONS_IN_QS_0" : COST_CONTENT_MID / 2,
    "FEATURE_SCREEN_DIMENSIONS_IN_QS_1" : COST_CONTENT_MID / 2,
    "FEATURE_AD_DIMENSIONS_IN_COMPLETE_URL_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_DIMENSIONS_IN_COMPLETE_URL_1" : COST_CONTENT_HARD / 2,
    "FEATURE_VALID_QS_0" : COST_CONTENT_MID / 2,
    "FEATURE_VALID_QS_1" : COST_CONTENT_MID / 2,
    #
    "FEATURE_FIRST_PARENT_ASYNC_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ASYNC_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_DEFER_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_DEFER_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_ADDED_BY_SCRIPT_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_ADDED_BY_SCRIPT_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT_1" : COST_CONTENT_MID / 2,
    #
    "FEATURE_CATEGORICAL" : COST_CONTENT_HARD / 2,
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

FEATURES_COST_HCC = {
    "FEATURE_GRAPH_NODES" : COST_STRUCT_EASY_EASY,
    "FEATURE_GRAPH_EDGES" : COST_STRUCT_EASY_EASY,
    "FEATURE_INBOUND_OUTBOUND_CONNECTIONS" : COST_STRUCT_EASY_EASY,
    "FEATURE_OUTBOUND_CONNECTIONS" : COST_STRUCT_EASY_EASY,
    "FEATURE_FIRST_NUMBER_OF_SIBLINGS" : COST_STRUCT_EASY_EASY,
    "FEATURE_FIRST_PARENT_NUMBER_OF_SIBLINGS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_INBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_OUTBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_INBOUND_OUTBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_AVERAGE_DEGREE_CONNECTIVITY" : COST_STRUCT_HARD,
    "FEATURE_AVERAGE_DEGREE_CONNECTIVITY" : COST_STRUCT_HARD,
    "FEATURE_ASCENDANTS_AD_KEYWORD_0" : COST_STRUCT_HARD / 2,
    "FEATURE_ASCENDANTS_AD_KEYWORD_1" : COST_STRUCT_HARD / 2,
    "FEATURE_FIRST_PARENT_SIBLING_AD_ATTRIBUTE_0" : COST_STRUCT_HARD / 2,
    "FEATURE_FIRST_PARENT_SIBLING_AD_ATTRIBUTE_1" : COST_STRUCT_HARD / 2,

    "FEATURE_URL_LENGTH" : COST_CONTENT_EASY_EASY,
    "FEATURE_AD_KEYWORD_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_KEYWORD_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SPECIAL_CHAR_AD_KEYWORD_0" : COST_CONTENT_HARD / 2,
    "FEATURE_SPECIAL_CHAR_AD_KEYWORD_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SEMICOLON_PRESENT_0" : COST_CONTENT_EASY / 2,
    "FEATURE_SEMICOLON_PRESENT_1" : COST_CONTENT_EASY / 2,
    "FEATURE_BASE_DOMAIN_IN_QS_0" : COST_CONTENT_EASY / 2,
    "FEATURE_BASE_DOMAIN_IN_QS_1" : COST_CONTENT_EASY / 2,
    "FEATURE_AD_DIMENSIONS_IN_QS_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_DIMENSIONS_IN_QS_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SCREEN_DIMENSIONS_IN_QS_0" : COST_CONTENT_MID / 2,
    "FEATURE_SCREEN_DIMENSIONS_IN_QS_1" : COST_CONTENT_MID / 2,
    "FEATURE_AD_DIMENSIONS_IN_COMPLETE_URL_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_DIMENSIONS_IN_COMPLETE_URL_1" : COST_CONTENT_HARD / 2,
    "FEATURE_VALID_QS_0" : COST_CONTENT_MID / 2,
    "FEATURE_VALID_QS_1" : COST_CONTENT_MID / 2,
    #
    "FEATURE_FIRST_PARENT_ASYNC_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ASYNC_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_DEFER_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_DEFER_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_ADDED_BY_SCRIPT_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_ADDED_BY_SCRIPT_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT_1" : COST_CONTENT_MID / 2,
    #
    "FEATURE_CATEGORICAL" : COST_CONTENT_HARD / 2,
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

FEATURES_COST_HSC = {
    "FEATURE_GRAPH_NODES" : COST_STRUCT_EASY_EASY,
    "FEATURE_GRAPH_EDGES" : COST_STRUCT_EASY_EASY,
    "FEATURE_INBOUND_OUTBOUND_CONNECTIONS" : COST_STRUCT_EASY_EASY,
    "FEATURE_OUTBOUND_CONNECTIONS" : COST_STRUCT_EASY_EASY,
    "FEATURE_FIRST_NUMBER_OF_SIBLINGS" : COST_STRUCT_EASY_EASY,
    "FEATURE_FIRST_PARENT_NUMBER_OF_SIBLINGS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_INBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_OUTBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_INBOUND_OUTBOUND_CONNECTIONS" : COST_STRUCT_MID,
    "FEATURE_FIRST_PARENT_AVERAGE_DEGREE_CONNECTIVITY" : COST_STRUCT_HARD,
    "FEATURE_AVERAGE_DEGREE_CONNECTIVITY" : COST_STRUCT_HARD,
    "FEATURE_ASCENDANTS_AD_KEYWORD_0" : COST_STRUCT_HARD / 2,
    "FEATURE_ASCENDANTS_AD_KEYWORD_1" : COST_STRUCT_HARD / 2,
    "FEATURE_FIRST_PARENT_SIBLING_AD_ATTRIBUTE_0" : COST_STRUCT_HARD / 2,
    "FEATURE_FIRST_PARENT_SIBLING_AD_ATTRIBUTE_1" : COST_STRUCT_HARD / 2,

    "FEATURE_URL_LENGTH" : COST_CONTENT_EASY_EASY,
    "FEATURE_AD_KEYWORD_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_KEYWORD_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SPECIAL_CHAR_AD_KEYWORD_0" : COST_CONTENT_HARD / 2,
    "FEATURE_SPECIAL_CHAR_AD_KEYWORD_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SEMICOLON_PRESENT_0" : COST_CONTENT_EASY / 2,
    "FEATURE_SEMICOLON_PRESENT_1" : COST_CONTENT_EASY / 2,
    "FEATURE_BASE_DOMAIN_IN_QS_0" : COST_CONTENT_EASY / 2,
    "FEATURE_BASE_DOMAIN_IN_QS_1" : COST_CONTENT_EASY / 2,
    "FEATURE_AD_DIMENSIONS_IN_QS_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_DIMENSIONS_IN_QS_1" : COST_CONTENT_HARD / 2,
    "FEATURE_SCREEN_DIMENSIONS_IN_QS_0" : COST_CONTENT_MID / 2,
    "FEATURE_SCREEN_DIMENSIONS_IN_QS_1" : COST_CONTENT_MID / 2,
    "FEATURE_AD_DIMENSIONS_IN_COMPLETE_URL_0" : COST_CONTENT_HARD / 2,
    "FEATURE_AD_DIMENSIONS_IN_COMPLETE_URL_1" : COST_CONTENT_HARD / 2,
    "FEATURE_VALID_QS_0" : COST_CONTENT_MID / 2,
    "FEATURE_VALID_QS_1" : COST_CONTENT_MID / 2,
    #
    "FEATURE_FIRST_PARENT_ASYNC_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ASYNC_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_DEFER_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_DEFER_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_ADDED_BY_SCRIPT_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_ADDED_BY_SCRIPT_1" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT_0" : COST_CONTENT_MID / 2,
    "FEATURE_FIRST_PARENT_ATTR_MODIFIED_BY_SCRIPT_1" : COST_CONTENT_MID / 2,
    #
    "FEATURE_CATEGORICAL" : COST_CONTENT_HARD / 2,
}