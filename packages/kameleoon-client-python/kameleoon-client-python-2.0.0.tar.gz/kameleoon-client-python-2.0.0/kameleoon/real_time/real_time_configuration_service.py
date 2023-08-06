""" Kameleoon Real Time Configuration Service """
from datetime import datetime as dt
import json
from multiprocessing import get_logger
from typing import Any, Callable, Dict, Optional
import sseclient
import urllib3
from kameleoon.helpers.multi_threading import run_in_threads_if_required

from kameleoon.real_time.real_time_event import RealTimeEvent

KAMELEOON_REAL_TIME_CONFIGURATION_THREAD = "KameleoonRealTimeConfigurationThread"
CONFIGURATION_UPDATE_EVENT = 'configuration-update-event'

class RealTimeConfigurationService:
    """
    RealTimeConfigurationService uses for fetching updates of configuration
    (experiments and feature flags) in real time 
    """

    def __init__(
            self,
            url: str,
            update_handler: Callable[[RealTimeEvent], None],
            logger=None):
        """
        For RealTimeConfigurationService must be provided an url 
        from where it can read the updates
        """
        self.url = url
        self.update_handler = update_handler
        self.need_close = False
        self.headers = {'Accept': 'text/event-stream',
                        'Cache-Control': 'no-cache', 
                        'Connection': 'Keep-Alive'}
        self.logger = logger or get_logger()
        self.http: Optional[urllib3.PoolManager] = None
        self._create_sse_client()

    def _create_sse_client(self) -> None:
        if not self.need_close:
            run_in_threads_if_required(
                        background_thread=True,
                        func=self._run_sse_client,
                        args=[],
                        thread_name=KAMELEOON_REAL_TIME_CONFIGURATION_THREAD)

    def _run_sse_client(self):
        self.logger.debug("Create SSE client")
        response = self._with_urllib3(self.url, self.headers)
        client = sseclient.SSEClient(response)
        try: 
            for message in client.events():
                if self.need_close:
                    break
                if message.event == CONFIGURATION_UPDATE_EVENT:
                    event_dict = json.loads(message.data)
                    self.update_handler(RealTimeEvent(event_dict))
        except Exception as ex:
            self.logger.error(ex)
            self._create_sse_client()

    def close(self) -> None:
        self.need_close = True
        if self.http is not None:
            self.http.clear()

    def _with_urllib3(
            self,
            url: str,
            headers: Dict[str, Any]):
        """Get a streaming response for the given event feed using urllib3."""
        self.http = urllib3.PoolManager()
        return self.http.request('GET', url, preload_content=False, headers=headers)