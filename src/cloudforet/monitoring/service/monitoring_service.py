import logging
import os

from spaceone.core.service import *

from cloudforet.monitoring.manager.monitoring_manager import MonitoringManager

_LOGGER = logging.getLogger(__name__)


@authentication_handler
@authorization_handler
@event_handler
class MonitoringService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(["options", "secret_data", "query", "start", "end"])
    @change_timestamp_value(["start", "end"], timestamp_format="iso8601")
    def list_logs(self, params):
        """Get quick list of resources

        Args:
            params (dict) {
                'options': 'dict',
                'schema': 'str',
                'secret_data': 'dict',
                'query': 'dict',
                'keyword': 'str',
                'start': 'timestamp',
                'end': 'timestamp',
                'sort': 'dict',
                'limit': 'int'
            }

        Returns: list of resources
        """

        proxy_env = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        if proxy_env:
            _LOGGER.info(
                f"** Using proxy in environment variable HTTPS_PROXY/https_proxy: {proxy_env}"
            )  # src/cloudforet/monitoring/libs/google_cloud_connector.py _create_http_client

        mon_manager = self.locator.get_manager(MonitoringManager)
        for logs in mon_manager.list_logs(params):
            yield logs
