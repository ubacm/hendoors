import json
from unittest import mock

from django.test import TestCase

from hendoors.votes import utils


class TestUtils(TestCase):

    # Over-simplified
    TEST_MARKS_EXTERNAL = [
        {'slack_id': 'USER1', 'score': 1.0},
        {'slack_id': 'USER2', 'score': 2},
        {'slack_id': 'USER3', 'score': 3.0},
    ]
    TEST_MARKS = {
        'USER1': 1,
        'USER2': 2,
        'USER3': 3,
    }

    @mock.patch('urllib.request.urlopen')
    def test_get_scores(self, mocked_urlopen):
        instance = mock.MagicMock()
        response = json.dumps(self.TEST_MARKS_EXTERNAL).encode()
        instance.read.return_value = response
        instance.__enter__.return_value = instance
        mocked_urlopen.return_value = instance
        self.assertDictEqual(self.TEST_MARKS, utils.load_marks())

    @mock.patch('hendoors.votes.utils.load_marks')
    def test_get_score_present(self, mocked_get_scores):
        mocked_get_scores.return_value = self.TEST_MARKS
        self.assertEqual(1, utils.get_marks_by_id('USER1'))
        self.assertEqual(2, utils.get_marks_by_id('USER2'))
        self.assertEqual(3, utils.get_marks_by_id('USER3'))

    @mock.patch('hendoors.votes.utils.load_marks')
    def test_get_score_missing(self, mocked_get_scores):
        mocked_get_scores.return_value = self.TEST_MARKS
        self.assertEqual(0, utils.get_marks_by_id('MISSING'))
