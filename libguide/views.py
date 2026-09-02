# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from blti.views import BLTILaunchView
from django.conf import settings
from restclients_core.exceptions import DataFailureException

from libguide.dao.library import campus_from_subaccount, get_subject_guide


class LibGuideView(BLTILaunchView):
    template_name = 'libguide/libguide.html'

    def get_context_data(self, **kwargs):
        for sis_id, url, name in getattr(settings, 'LIBRARY_REDIRECTS', []):
            if self.blti.account_sis_id.startswith(sis_id):
                return {'redirect_url': url, 'redirect_name': name}

        if self.blti.course_sis_id:
            course_sis_id = self.blti.course_sis_id
        else:
            course_sis_id = f'course_{self.blti.canvas_course_id}'

        campus = campus_from_subaccount(self.blti.account_sis_id)

        try:
            subject_guide = get_subject_guide(course_sis_id, campus)
            return {'campus': campus, 'subject_guide': subject_guide}

        except DataFailureException as err:
            return {
                'error': f'UW Libraries Subject Guides are not available: {err.msg}'
            }
