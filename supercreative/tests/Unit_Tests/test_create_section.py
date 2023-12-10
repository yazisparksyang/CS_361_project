from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from supercreative.models import (Course, Section)
from supercreative.create_sections.section import create_section


class CreateSectionTest(TestCase):
    course = None

    def setUp(self):
        # variable values to use in the tests
        self.section_id = 801
        self.section_type = "lab"
        self.role = "administrator"

        # set up two mock courses
        self.course = Course.objects.create(course_name="Intro to Software Engineering", course_id=1,
                                            course_description="stuff", course_code="COMPSCI-361")

        self.course_two = Course.objects.create(course_name="System Programming", course_id=5,
                                                course_description="stuff", course_code="COMPSCI-337")

        # set up a mock section (to test for duplicates)
        self.section = Section.objects.create(section_id=803, course_id=self.course_two,
                                              section_type="discussion")

    def test_correct_section(self):
        # correctly create a section
        self.assertEqual(
            create_section(section_id=self.section_id, course=self.course, section_type=self.section_type),
            "section was successfully created",
            "create_section did return the correct message.")

        # get created course and check its values
        created_section = Section.objects.get(section_id=self.section_id)

        self.assertEqual(created_section.section_id, self.section_id, "create_section did not correctly set the "
                                                                      "section_id")

        self.assertEqual(created_section.section_type, self.section_type, "create_course did not "
                                                                          "correctly set the "
                                                                          "section_type")

    # course must exist
    def test_invalid_course(self):
        # attempt to create a section with various invalid courses
        self.assertEqual(create_section(self.section_id, 3465423, self.section_type),
                         "invalid input for course",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(self.section_id, None, self.section_type),
                         "invalid input for course",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(self.section_id, "wrong", self.section_type),
                         "invalid input for course",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(self.section_id, -1, self.section_type),
                         "invalid input for course",
                         "create_section did return the correct message.")

        # make sure the invalid sections weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Section.objects.get(section_id=self.section_id)

    # section id must be a unique integer
    def test_invalid_section_id(self):
        # attempt to create a course with various invalid section ids
        self.assertEqual(create_section(-1, self.course, self.section_type),
                         "sectionID must be an integer",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(None, self.course, self.section_type),
                         "sectionID must be an integer",
                         "create_section did return the correct message.")

        self.assertEqual(create_section("wrong", self.course, self.section_type),
                         "sectionID must be an integer",
                         "create_section did return the correct message.")

        # duplicate section_id
        self.assertEqual(create_section(self.section.section_id, self.course, self.section_type),
                         "section already exists",
                         "create_section did return the correct message.")

        # make sure the invalid sections weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Section.objects.get(course_id=self.course.course_id)

    # section type must be: lecture, lab, or discussion
    def test_invalid_section_type(self):
        # attempt to create a course with various invalid section types
        self.assertEqual(create_section(self.section_id, self.course, "wrong"),
                         "section type is not valid",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(self.section_id, self.course, None),
                         "section type is not valid",
                         "create_section did return the correct message.")

        self.assertEqual(create_section(self.section_id, self.course, ""),
                         "section type is not valid",
                         "create_section did return the correct message.")

        # make sure the invalid sections weren't created
        with self.assertRaises(ObjectDoesNotExist, msg="an exception should've been raised here"):
            Section.objects.get(section_id=self.section_id)
