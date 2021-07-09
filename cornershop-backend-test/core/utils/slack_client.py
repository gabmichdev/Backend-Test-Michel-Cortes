from functools import wraps
from typing import Union

import requests

from backend_test.envtools import getenv


def validate_slack_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self: SlackRESTClient = args[0]
        json_data = func(*args, **kwargs)
        if json_data["ok"] is False:
            self.last_error = json_data["error"]
            self._increase_error_count()
        return json_data

    return wrapper


def set_endpoint(endpoint_name):
    def set_endpoint_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self: SlackRESTClient = args[0]
            self.current_endpoint = endpoint_name
            return func(*args, **kwargs)

        return wrapper

    return set_endpoint_wrapper


class SlackRESTClient:
    def __init__(self, token=None):
        self.__token = token
        self.__base_url = getenv("SLACK_BASE_URL", default="https://slack.com/api/")
        self.__request_errors = 0
        self.__last_error = None
        self._auth_headers = {"Authorization": "Bearer {}"}
        self._current_endpoint = None
        self._url = None

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token

    @property
    def request_errors(self):
        return self.__request_errors

    @property
    def last_error(self):
        return self.__last_error

    @last_error.setter
    def last_error(self, last_error):
        self.__last_error = last_error

    @property
    def current_endpoint(self):
        return self._current_endpoint

    @current_endpoint.setter
    def current_endpoint(self, current_endpoint):
        self._current_endpoint = current_endpoint

    @property
    def auth_headers(self):
        return self._auth_headers

    def _increase_error_count(self):
        self.__request_errors += 1

    def _build_url(self):
        if self._current_endpoint is not None:
            self._url = f"{self.__base_url}{self._current_endpoint}"

    @validate_slack_request
    def _make_request(
        self,
        method: str,
        params: dict = None,
        headers: dict = None,
        json_data: dict = None,
    ) -> dict:
        """Makes request to the Slack REST API

        Args:
            method (str): HTTP verb.
            json_data (dict | None): Json data to send.
            params (dict | None): Query string parameters to send.

        Returns:
            dict: Raw json data returned.
        """
        headers = headers or {}
        if not isinstance(headers, dict):
            raise Exception("Headers must be a dictionary")
        params = params or {}
        if not isinstance(params, dict):
            raise Exception("Params must be a dictionary")
        json_data = json_data or {}
        if not isinstance(json_data, dict):
            raise Exception("Json must be a dictionary")
        self.auth_headers["Authorization"] = self._auth_headers["Authorization"].format(
            self.token
        )
        headers.update(self.auth_headers)
        self._build_url()
        request_config = {"headers": headers, "json": json_data, "params": params}
        try:
            return requests.request(method, self._url, **request_config).json()
        except requests.RequestException as e:
            return {"ok": False, "error": str(e)}

    @set_endpoint("conversations.list")
    def get_slack_conversation(self, conversation_name: str) -> Union[str, None]:
        """Gets a slack conversation id from the conversation name.

        Args:
            conversation_name (str): Name of the channel or conversation`.

        Returns:
            Union[str, None]: Id of the conversation or None if not found.
        """
        id_conversation = None
        try:
            json_data = self._make_request("get")
            if json_data.get("channels"):
                channels = json_data["channels"]
                id_conversation = next(
                    channel["id"]
                    for channel in channels
                    if channel["name"] == conversation_name
                )
            return id_conversation
        except Exception:
            return

    @set_endpoint("chat.postMessage")
    def send_slack_message(self, id_conversation: str, message: str) -> None:
        """Sends a message to a specific conversation.

        Args:
            id_conversation (str): Conversation or channel identifier.
            message (str): Message to be send_todays_menu_to_slack
        """
        payload = {"channel": id_conversation, "text": message}
        return self._make_request("post", json_data=payload)
