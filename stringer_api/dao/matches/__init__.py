from stringer_api import cache
from .. import site_navigation, orders
import enrich
import prune_path


@cache.cached(timeout=3600, key_prefix='enriched_betfair_navigation')
def get():
    raw_match_paths = site_navigation.get_raw_match_paths()
    enriched_matches = enrich.do(raw_match_paths)
    singles_matches = filter(lambda x: x['singles'], enriched_matches)
    pruned_matches = prune_path.do(singles_matches)

    return pruned_matches
