# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase
from libguide.dao.library import campus_from_subaccount, get_subject_guide
from uw_libraries.util import fdao_subject_guide_override
import mock


@fdao_subject_guide_override
class LibraryDAOTest(TestCase):
    def test_campus_from_subaccount(self):
        self.assertEquals(
            campus_from_subaccount('uwcourse:tacoma'), 'tacoma')
        self.assertEquals(
            campus_from_subaccount('uwcourse:bothell:nursing'), 'bothell')
        self.assertEquals(
            campus_from_subaccount('uwcourse:seattle:medicine'), 'seattle')
        self.assertEquals(
            campus_from_subaccount(''), 'seattle')
        self.assertEquals(
            campus_from_subaccount(43567), 'seattle')
        self.assertEquals(
            campus_from_subaccount(None), 'seattle')

    @mock.patch('libguide.dao.library.get_default_subject_guide')
    def test_get_default_subject_guide(self, mock_fn):
        r = get_subject_guide('course_12345', 'tacoma')
        mock_fn.assert_called_with(campus='tacoma')

        # 404, fails over to default guide
        r = get_subject_guide('2015-autumn-GEN STU-201-A', 'bothell')
        mock_fn.assert_called_with(campus='bothell')

    @mock.patch(
        'libguide.dao.library.get_subject_guide_for_canvas_course_sis_id')
    def test_get_subject_guide(self, mock_fn):
        sis_course_id = '2017-spring-ESS-101-A'

        r = get_subject_guide(sis_course_id, 'tacoma')
        mock_fn.assert_called_with(sis_course_id)
