from django.conf.urls import url
from libguide.views import LibGuideView


urlpatterns = [
    url(r'^$', LibGuideView.as_view()),
]
