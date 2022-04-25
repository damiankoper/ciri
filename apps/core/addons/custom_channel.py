import logging
from asyncio import Queue, CancelledError
from sanic.request import Request
from typing import Text, Dict, Any
from rasa.core.channels.rest import RestInput


logger = logging.getLogger(__name__)


class CustomIO(RestInput):
    """A custom http input channel.

    This implementation is the basis for a custom implementation of a chat
    frontend. You can customize this to send messages to Rasa and
    retrieve responses from the assistant."""

    @classmethod
    def name(cls) -> Text:
        return "customio"

    def get_metadata(self, request: Request) -> Dict[Text, Any]:
        return {"metadata": "bbb"}
