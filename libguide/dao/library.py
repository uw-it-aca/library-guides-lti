# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_libraries.subject_guides import (
    get_default_subject_guide, get_subject_guide_for_canvas_course_sis_id)
from uw_canvas.models import CanvasCourse
from restclients_core.exceptions import DataFailureException


def get_subject_guide(sis_course_id, campus):
    if not CanvasCourse(sis_course_id=sis_course_id).is_academic_sis_id():
        return get_default_subject_guide(campus=campus)

    try:
        subject_guide = get_subject_guide_for_canvas_course_sis_id(
            sis_course_id)

        # Library service only returns Seattle campus default guide
        if (subject_guide.is_default_guide and
                subject_guide.default_guide_campus.lower() != campus):
            subject_guide = get_default_subject_guide(campus=campus)

        return subject_guide

    except DataFailureException:
        return get_default_subject_guide(campus=campus)


def campus_from_subaccount(subaccount_id):
    if subaccount_id is not None:
        if 'uwcourse:tacoma' in str(subaccount_id):
            return 'tacoma'
        elif 'uwcourse:bothell' in str(subaccount_id):
            return 'bothell'
    return 'seattle'
