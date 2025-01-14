# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from memcached_clients import RestclientPymemcacheClient


class LibCurricsCache(RestclientPymemcacheClient):
    def get_cache_expiration_time(self, service, url, status=None):
        if 'libcurrics' == service:
            return getattr(settings, 'LIBCURRICS_CACHE_EXPIRES', 60 * 60 * 4)
