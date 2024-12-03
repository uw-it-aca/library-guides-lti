# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.urls import re_path
from libguide.views import LibGuideView

urlpatterns = [
    re_path(r'^$', LibGuideView.as_view(), name="lti-launch"),
]
