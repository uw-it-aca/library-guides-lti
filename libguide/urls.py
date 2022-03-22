# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.urls import re_path
from libguide.views import LibGuideView

urlpatterns = [
    re_path(r'^$', LibGuideView.as_view()),
]
