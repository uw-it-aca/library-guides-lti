# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django.conf import settings
from django.http import HttpResponseRedirect
from blti.views import BLTILaunchView
from libguide.dao.library import campus_from_subaccount, get_subject_guide
from restclients_core.exceptions import DataFailureException


class LibGuideView(BLTILaunchView):
    template_name = 'libguide/libguide.html'

    def post(self, request, *args, **kwargs):
        account_id = self.blti.canvas_account_id
        if account_id in getattr(settings, 'LIBRARY_REDIRECTS', {}):
            return HttpResponseRedirect(settings.LIBRARY_REDIRECTS[account_id])

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

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
