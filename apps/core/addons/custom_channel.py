import logging
from asyncio import Queue, CancelledError
from sanic.request import Request
from typing import Text, Dict, Any
from rasa.core.channels.rest import RestInput


logger = logging.getLogger(__name__)


class CustomIO(RestInput):
    def get_metadata(self, request: Request) -> Dict[Text, Any]:
        return request.json.get("metadata", None)
