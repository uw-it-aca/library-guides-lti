from blti.views import BLTILaunchView
from sis_provisioner.policy import CoursePolicy, CoursePolicyException
from restclients.library.currics import (
    get_subject_guide_for_canvas_course_sis_id, get_default_subject_guide)
from restclients.exceptions import DataFailureException


class LibGuideView(BLTILaunchView):
    template_name = 'libguide/libguide.html'

    def get_context_data(self, **kwargs):
        blti_data = kwargs['blti_params']

        canvas_login_id = blti_data.get('custom_canvas_user_login_id')
        canvas_course_id = blti_data.get('custom_canvas_course_id')
        sis_course_id = blti_data.get('lis_course_offering_sourcedid',
                                      'course_%s' % canvas_course_id)
        subaccount_id = blti_data.get('custom_canvas_account_sis_id', '')

        if 'uwcourse:tacoma' in subaccount_id:
            campus = 'tacoma'
        elif 'uwcourse:bothell' in subaccount_id:
            campus = 'bothell'
        else:
            campus = 'seattle'

        subject_guide = None
        try:
            CoursePolicy().valid_academic_course_sis_id(sis_course_id)

            try:
                subject_guide = get_subject_guide_for_canvas_course_sis_id(
                    sis_course_id)

                # Library service only returns Seattle campus default guide
                if (subject_guide.is_default_guide and
                        subject_guide.default_guide_campus.lower() != campus):
                    subject_guide = None

            except DataFailureException as err:
                pass

        except CoursePolicyException as err:
            pass

        if subject_guide is None:
            try:
                subject_guide = get_default_subject_guide(campus=campus)
            except DataFailureException as err:
                return {'error': (
                    'UW Libraries Subject Guides are not available: %s' % (
                        err.msg))}

        return {'campus': campus, 'subject_guide': subject_guide}
