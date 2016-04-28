from django.conf.urls import patterns, url, include
from libguides.views import LibGuideView


urlpatterns = patterns(
    '',
    url(r'^$', LibGuideView.as_view()),
)
