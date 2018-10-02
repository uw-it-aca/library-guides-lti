from django.urls import re_path
from libguide.views import LibGuideView

urlpatterns = [
    re_path(r'^$', LibGuideView.as_view()),
]
