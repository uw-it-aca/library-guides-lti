from restclients.library.currics import (
    get_default_subject_guide, get_subject_guide_for_canvas_course_sis_id)
from restclients.exceptions import DataFailureException
from sis_provisioner.dao.course import valid_academic_course_sis_id
from sis_provisioner.exceptions import CoursePolicyException


def get_subject_guide(sis_course_id, campus):
    try:
        valid_academic_course_sis_id(sis_course_id)

        subject_guide = get_subject_guide_for_canvas_course_sis_id(
            sis_course_id)

        # Library service only returns Seattle campus default guide
        if (subject_guide.is_default_guide and
                subject_guide.default_guide_campus.lower() != campus):
            subject_guide = get_default_subject_guide(campus=campus)

        return subject_guide

    except (CoursePolicyException, DataFailureException):
        return get_default_subject_guide(campus=campus)


def campus_from_subaccount(subaccount_id):
    if subaccount_id is not None:
        if 'uwcourse:tacoma' in str(subaccount_id):
            return 'tacoma'
        elif 'uwcourse:bothell' in str(subaccount_id):
            return 'bothell'
    return 'seattle'
