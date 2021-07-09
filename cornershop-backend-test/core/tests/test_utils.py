from datetime import datetime
from pprint import pprint
from unittest import mock

from django.test import TestCase

from backend_test.envtools import getenv
from core.utils.date_utils import generate_day_range_for_date, is_between
from core.utils.slack_client import SlackRESTClient


class DateUtilsTests(TestCase):
    """Class to test the date utils helper functions"""

    def test_is_between(self):
        """Test that values that are between return True"""
        date = datetime.now()
        gte = date.replace(hour=0, minute=0, second=0)
        lte = date.replace(hour=23, minute=59, second=59)
        self.assertTrue(is_between(left_value=0, value=1, right_value=2))
        self.assertTrue(is_between(left_value="0", value="1", right_value="2"))
        self.assertTrue(is_between(left_value=gte, value=date, right_value=lte))

    def test_non_comparable_values(self):
        """Test that comparing values that do not support comparison returns None"""
        self.assertIsNone(is_between(left_value=0, value=1, right_value="2"))

    def test_generate_daterange(self):
        """Test that the date is in the range generated"""
        date = datetime.now()
        gte, lte = generate_day_range_for_date(date)
        self.assertTrue(is_between(left_value=gte, value=date, right_value=lte))


slack_client_base = "core.utils.slack_client."


class ResponseMock:
    def __init__(self, expected):
        self.__expected = expected

    @property
    def expected(self):
        return self.__expected

    @expected.setter
    def expected(self, expected):
        self.__expected = expected

    def json(self):
        return self.expected


class SlackClientTests(TestCase):
    """Class to test sending messages to slack"""

    def setUp(self):
        token = getenv("SLACK_BOT_TOKEN", default="No token")
        self.client = SlackRESTClient(token)

    def test_endpoint_is_null_initially(self):
        """Test the client has no endpoint set at initialization"""
        self.assertIsNone(self.client.current_endpoint)

    @mock.patch(slack_client_base + "requests.request")
    def test_request_fails_if_no_token(self, request_mock):
        """Test request fails if token is wrong"""
        mocked_res = ResponseMock({"ok": False, "error": "invalid_auth"})
        request_mock.return_value = mocked_res
        self.client.current_endpoint = "conversations.list"
        self.client._make_request("get")

        self.assertEqual(self.client.last_error, "invalid_auth")
        self.assertEqual(self.client.request_errors, 1)

    @mock.patch(slack_client_base + "requests.request")
    def test_response_when_no_token_is_used(self, request_mock):
        """Test the response is what was expected when no token is sent"""
        mocked_res = ResponseMock({"ok": False, "error": "invalid_auth"})
        request_mock.return_value = mocked_res

        client_res = self.client._make_request("get")
        request_mock.assert_called_once()
        self.assertEqual(client_res, mocked_res.json())

    @mock.patch(slack_client_base + "requests.request")
    def test_get_slack_conversation_id(self, request_mock):
        """Test that the correct conversation id is returned"""
        mocked_res = ResponseMock(
            {
                "ok": True,
                "channels": [
                    {
                        "id": "expected",
                        "name": "conversation_name",
                    }
                ],
            }
        )
        request_mock.return_value = mocked_res

        res = self.client.get_slack_conversation("conversation_name")
        self.assertEqual(res, "expected")

    @mock.patch(slack_client_base + "requests.request")
    def test_send_slack_message(self, request_mock):
        expected_response = {
            "ok": True,
            "channel": "id_channel",
            "message": {
                "text": "test",
            },
        }
        mocked_res = ResponseMock(expected_response)
        request_mock.return_value = mocked_res

        res = self.client.send_slack_message("id_channel", "test")

        self.assertEqual(res["channel"], "id_channel")
        self.assertIsInstance(res["message"], dict)
        self.assertEqual(res["message"]["text"], "test")
