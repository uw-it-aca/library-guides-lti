from django.conf.urls import patterns, url, include
from libguide.views import LibGuideView


urlpatterns = patterns(
    '',
    url(r'^$', LibGuideView.as_view()),
)
