# COMMON_THRESHOLD = 10000
# INTERSECT_LIMIT = 100
LOG_QUERIES = True
LOG_NOT_FOUND = True
SLOW_QUERIES = 100
EXTRA_FIELDS = [
    {"key": "citycode"},
]
FILTERS = ["type", "postcode", "citycode", "city"]
BLOCKED_PLUGINS = ["trigrams"]
QUERY_PROCESSORS_PYPATHS = [
    "addok.helpers.text.check_query_length",
    "addok_france.extract_address",
    "addok_france.clean_query",
    "addok_france.remove_leading_zeros",
]
SEARCH_RESULT_PROCESSORS_PYPATHS = [
    "addok.helpers.results.match_housenumber",
    "addok_france.make_labels",
    "addok.helpers.results.score_by_importance",
    "addok.helpers.results.score_by_autocomplete_distance",
    "addok.helpers.results.score_by_ngram_distance",
    "addok.helpers.results.score_by_geo_distance",
    "addok.helpers.results.adjust_scores",
]
PROCESSORS_PYPATHS = [
    "addok.helpers.text.tokenize",
    "addok.helpers.text.normalize",
    "addok_france.glue_ordinal",
    "addok_france.fold_ordinal",
    "addok_france.flag_housenumber",
    "addok.helpers.text.synonymize",
    "addok_fr.phonemicize",
]
# DOCUMENT_SERIALIZER_PYPATH = 'addok.helpers.serializers.MsgpackSerializer'
# DOCUMENT_STORE_PYPATH = 'addok.ds.RedisStore'
BATCH_CHUNK_SIZE = 1000
SQLITE_DB_PATH = "/home/ybon/Code/py/addok/addok.db"
# SQLITE_DB_PATH = '/run/media/ybon/EMTEC/addok.db'
# LOG_DIR = '/pouet'
PG_CONFIG = "dbname=addok"
MIN_EDGE_NGRAMS = 2


def target_city(helper):
    if len(helper.query) <= 4:
        helper.filters.append("f|type|municipality")


RESULTS_COLLECTORS_PYPATHS = [
    target_city,
    "addok.autocomplete.only_commons_but_geohash_try_autocomplete_collector",
    "addok.helpers.collectors.no_tokens_but_housenumbers_and_geohash",
    "addok.helpers.collectors.no_available_tokens_abort",
    "addok.helpers.collectors.only_commons",
    "addok.autocomplete.no_meaningful_but_common_try_autocomplete_collector",
    "addok.autocomplete.only_commons_try_autocomplete_collector",
    "addok.helpers.collectors.bucket_with_meaningful",
    "addok.helpers.collectors.reduce_with_other_commons",
    "addok.helpers.collectors.ensure_geohash_results_are_included_if_center_is_given",  # noqa
    "addok.fuzzy.fuzzy_collector",
    "addok.autocomplete.autocomplete_meaningful_collector",
    "addok.helpers.collectors.extend_results_extrapoling_relations",
    "addok.helpers.collectors.extend_results_reducing_tokens",
]
