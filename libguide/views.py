from blti.views import BLTILaunchView
from libguide.dao.library import campus_from_subaccount, get_subject_guide
from restclients_core.exceptions import DataFailureException
from urllib3.exceptions import MaxRetryError


class LibGuideView(BLTILaunchView):
    template_name = 'libguide/libguide.html'

    def get_context_data(self, **kwargs):
        blti_data = kwargs['blti_params']

        canvas_login_id = blti_data.get('custom_canvas_user_login_id')
        canvas_course_id = blti_data.get('custom_canvas_course_id')
        sis_course_id = blti_data.get('lis_course_offering_sourcedid',
                                      'course_%s' % canvas_course_id)
        subaccount_id = blti_data.get('custom_canvas_account_sis_id', '')
        campus = campus_from_subaccount(subaccount_id)

        try:
            subject_guide = get_subject_guide(sis_course_id, campus)
            return {'campus': campus, 'subject_guide': subject_guide}

        except (MaxRetryError, DataFailureException) as err:
            return {'error': (
                'UW Libraries Subject Guides are not available: %s' % (
                    getattr(err, 'msg', 'Service not available')))}
