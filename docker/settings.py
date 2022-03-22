from .base_settings import *

INSTALLED_APPS += [
    'libguide.apps.LibraryGuideConfig',
    'compressor',
]

COMPRESS_ROOT = '/static/'
COMPRESS_PRECOMPILERS = (('text/less', 'lessc {infile} {outfile}'),)
COMPRESS_OFFLINE = True
STATICFILES_FINDERS += ('compressor.finders.CompressorFinder',)

if os.getenv('ENV', 'localdev') == 'localdev':
    DEBUG = True
    RESTCLIENTS_DAO_CACHE_CLASS = None
else:
    RESTCLIENTS_DAO_CACHE_CLASS = 'libguide.cache.LibCurricsCache'

LIBCURRICS_CACHE_EXPIRES = 60 * 60 * 4

LIBRARY_REDIRECTS = {
    # canvas_account_id: redirect_url
    '102361': 'https://liblawuw.libguides.com/er.php?b=c',
}
