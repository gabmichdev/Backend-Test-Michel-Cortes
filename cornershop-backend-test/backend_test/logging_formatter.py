import json
import logging
from importlib import import_module
from typing import Any, Dict, Type, Union

from fluent.handler import FluentRecordFormatter


class VerboseFluentRecordFormatter(FluentRecordFormatter):
    def __init__(
        self,
        *,
        raise_on_format_error: bool = False,
        encoder_class: Union[str, Type[json.JSONEncoder]] = json.JSONEncoder,
        encoder_options: Dict[str, Any] = None,
        **kwargs: Any,
    ) -> None:
        self.raise_on_format_error = raise_on_format_error
        self.encoder_class = encoder_class
        self.encoder_options = encoder_options or {}
        super().__init__(**kwargs)

    @property
    def encoder_class(self) -> Type[json.JSONEncoder]:
        return self._encoder_class

    @encoder_class.setter
    def encoder_class(self, encoder_class: Union[str, Type[json.JSONEncoder]]) -> None:
        if isinstance(encoder_class, str):
            project_name_underscore, class_name = encoder_class.rsplit(".", 1)
            module = import_module(project_name_underscore)
            self._encoder_class = getattr(module, class_name)
        elif issubclass(encoder_class, json.JSONEncoder):
            self._encoder_class = encoder_class
        else:
            raise TypeError(f"Cannot set encoder class {str(encoder_class)}")

    @property
    def encoder(self) -> json.JSONEncoder:
        if not hasattr(self, "_encoder"):
            self._encoder = self.encoder_class(**self.encoder_options)
        return self._encoder

    def json_encode(self, obj: Any) -> Dict:
        return json.loads(self.encoder.encode(obj))

    def _format_msg_default(self, record, msg):
        return {"message": record.getMessage()}

    def _structuring(self, data, record):
        msg = record.msg

        if isinstance(msg, dict):
            self._add_dic(data, self.json_encode(msg))
            if "message" not in data:
                data["message"] = ""
        elif isinstance(msg, str):
            self._add_dic(data, self._format_msg_default(record, msg))
        else:
            self._add_dic(data, {"message": self.json_encode(msg)})

    def format(self, record):
        try:
            data = super().format(record)

            if "data" in record.__dict__:
                data["data"] = self.json_encode(record.__dict__["data"])

        except (ValueError, TypeError):
            sentry_logger = logging.getLogger("sentry")
            sentry_logger.exception("Unserializable data was given to logger")

            if self.raise_on_format_error:
                raise

            record.hostname = self.hostname
            data = self._formatter(record)
            data[
                "message"
            ] = "Logger ({}) is receiving non serializable data, please check sentry.".format(
                record.name
            )

        return data
