from django.conf import settings
from django.template import Context, loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from blti import BLTI, BLTIException
from libguide.models import CurriculumGuide


# CourseList
@csrf_exempt
def LibGuide(request, template='libguide/libguide.html'):
    blti_data = {"context_label": "NO COURSE"}
    validation_error = None
    sis_course_id = 'None'
    canvas_course_id = 'None'
    status_code = 200
    params = {}

    try:
        blti = BLTI()
        if (hasattr(settings, 'NO_AUTH') and settings.NO_AUTH and
                'testme' in request.GET):
            course_id = request.GET.get('courseid', '2013-autumn-BIOL-101-A')
            blti_data = {
                'custom_canvas_user_login_id': 'testuser',
                'custom_canvas_course_id': '66666666',
                'lis_course_offering_sourcedid': course_id,
            }
        else:
            blti_data = blti.validate(request)

        params['blti'] = blti_data

        canvas_login_id = blti_data.get('custom_canvas_user_login_id')
        canvas_course_id = blti_data.get('custom_canvas_course_id')
        sis_course_id = blti_data.get('lis_course_offering_sourcedid',
                                      'course_%s' % canvas_course_id)
        blti.set_session(request, user_id=canvas_login_id)

        params['sis_course_id'] = sis_course_id
        params['canvas_course_id'] = canvas_course_id

        try:
            (year, quarter, curric, course_num) = sis_course_id.split('-', 3)
            libguide = CurriculumGuide.objects.select_related().get(
                curriculum__curriculum_abbr=curric)

            params['curriculum'] = libguide.curriculum
            params['subject_guide'] = libguide.subject_guide

        except:
            libguide = CurriculumGuide()

    except BLTIException, err:
        params['validation_error'] = str(err)
        template = 'lti_fail.html'
        status_code = 401
    except Exception, err:
        params['validation_error'] = str(err)
        template = 'lti_fail.html'
        status_code = 400

    t = loader.get_template(template)
    c = Context(params)
    c.update(csrf(request))
    return HttpResponse(t.render(c), status=status_code)
