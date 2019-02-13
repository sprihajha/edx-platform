"""
Tests for permissions defined in courseware.rules
"""
import ddt

from django.test import TestCase

from course_modes.tests.factories import CourseModeFactory

from opaque_keys.edx.locator import CourseLocator
from student.models import CourseEnrollment
from student.tests.factories import UserFactory


@ddt.ddt
class PermissionTests(TestCase):
    """
    Tests for permissions defined in courseware.rules
    """
    def setUp(self):
        super(PermissionTests, self).setUp()
        self.user = UserFactory()

        self.course_id = CourseLocator('MITx', '000', 'Perm_course')
        CourseModeFactory(mode_slug='verified', course_id=self.course_id)
        CourseModeFactory(mode_slug='masters', course_id=self.course_id)

    def tearDown(self):
        super(PermissionTests, self).tearDown()
        self.user.delete()

    @ddt.data(
        (None, False),
        ('audit', False),
        ('verified', True),
        ('masters', True),
    )
    @ddt.unpack
    def test_proctoring_perm(self, mode, should_have_perm):
        """
        Test that the user has the edx_proctoring.can_take_proctored_exam permission
        """
        if mode is not None:
            CourseEnrollment.enroll(self.user, self.course_id, mode=mode)
        else:
            CourseEnrollment.unenroll(self.user, self.course_id)
        has_perm = self.user.has_perm('edx_proctoring.can_take_proctored_exam', {'course_id': unicode(self.course_id)})
        assert has_perm == should_have_perm
