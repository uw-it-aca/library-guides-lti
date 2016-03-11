from django.conf import settings
from django.template import Context, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from blti import BLTI, BLTIException
from sis_provisioner.policy import CoursePolicy, CoursePolicyException
from restclients.library.currics import (
    get_subject_guide_for_canvas_course_sis_id)
from restclients.exceptions import DataFailureException


@csrf_exempt
def LibGuide(request, template='libguide/libguide.html'):
    blti_data = {"context_label": "NO COURSE"}
    validation_error = None
    status_code = 200
    generic_guide_url = '2000-autumn-NONE-000-A'
    params = {}

    try:
        blti = BLTI()
        blti_data = blti.validate(request)

        params['blti'] = blti_data

        canvas_login_id = blti_data.get('custom_canvas_user_login_id')
        canvas_course_id = blti_data.get('custom_canvas_course_id')
        sis_course_id = blti_data.get('lis_course_offering_sourcedid',
                                      'course_%s' % canvas_course_id)
        subaccount_id = blti_data.get('custom_canvas_account_sis_id')
        blti.set_session(request, user_id=canvas_login_id)

        params['subaccount_id'] = subaccount_id
        params['sis_course_id'] = sis_course_id
        params['canvas_course_id'] = canvas_course_id

        try:
            CoursePolicy().valid_academic_course_sis_id(sis_course_id)
        except CoursePolicyException as err:
            sis_course_id = generic_guide_url

        try:
            subject_guide = get_subject_guide_for_canvas_course_sis_id(
                sis_course_id)
        except DataFailureException as err:
            if err.status == 404:
                subject_guide = get_subject_guide_for_canvas_course_sis_id(
                    generic_guide_url)
            else:
                raise

        # Boolean is nice here
        subject_guide.has_discipline = True if (
            subject_guide.discipline != 'your discipline') else False

        params['subject_guide'] = subject_guide

    except BLTIException as err:
        params['validation_error'] = err
        template = 'blti/error.html'
        status_code = 401
    except DataFailureException as err:
        params['validation_error'] = (
            'UW Libraries Subject Guides are not available: %s' % err.msg)
        template = 'blti/error.html'
        status_code = err.status
    except Exception as err:
        params['validation_error'] = err
        template = 'blti/error.html'
        status_code = 400

    t = loader.get_template(template)
    c = Context(params)
    c.update(csrf(request))
    return HttpResponse(t.render(c), status=status_code)
