from .base_urls import *
from django.urls import include, re_path


urlpatterns += [
    re_path(r'^', include('libguide.urls')),
    re_path(r'^blti/', include('blti.urls')),
]
