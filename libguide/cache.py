from django.conf import settings
from rc_django.cache_implementation.memcache import MemcachedCache


class LibCurricsCache(MemcachedCache):
    def get_cache_expiration_time(self, service, url):
        if 'libcurrics' == service:
            return getattr(settings, 'LIBCURRICS_CACHE_EXPIRES', 60 * 60 * 4)
