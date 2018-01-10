from blti.views import BLTILaunchView
from libguide.dao.library import campus_from_subaccount, get_subject_guide
from restclients_core.exceptions import DataFailureException
from urllib3.exceptions import MaxRetryError


class LibGuideView(BLTILaunchView):
    template_name = 'libguide/libguide.html'

    def get_context_data(self, **kwargs):
        if self.blti.course_sis_id:
            course_sis_id = self.blti.course_sis_id
        else:
            course_sis_id = 'course_%s' % self.blti.canvas_course_id

        campus = campus_from_subaccount(self.blti.account_sis_id)

        try:
            subject_guide = get_subject_guide(course_sis_id, campus)
            return {'campus': campus, 'subject_guide': subject_guide}

        except (MaxRetryError, DataFailureException) as err:
            return {'error': (
                'UW Libraries Subject Guides are not available: %s' % (
                    getattr(err, 'msg', 'Service not available')))}
