# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from blti.views import BLTILaunchView
from libguide.dao.library import campus_from_subaccount, get_subject_guide
from restclients_core.exceptions import DataFailureException


class LibGuideView(BLTILaunchView):
    template_name = 'libguide/libguide.html'

    def get_context_data(self, **kwargs):
        if self.blti.course_sis_id:
            course_sis_id = self.blti.course_sis_id
        else:
            course_sis_id = 'course_{}'.format(self.blti.canvas_course_id)

        campus = campus_from_subaccount(self.blti.account_sis_id)

        try:
            subject_guide = get_subject_guide(course_sis_id, campus)
            return {'campus': campus, 'subject_guide': subject_guide}

        except DataFailureException as err:
            return {'error': (
                'UW Libraries Subject Guides are not available: {}'.format(
                    err.msg))}
