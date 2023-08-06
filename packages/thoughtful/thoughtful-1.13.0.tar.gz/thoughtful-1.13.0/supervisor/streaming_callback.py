from __future__ import annotations

import logging
from typing import Optional

from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests import Session

from supervisor.manifest import Manifest
from supervisor.reporting.step_report import StepReport
from supervisor.reporting.streaming_payloads import BotManifestStreamingPayload
from supervisor.reporting.streaming_payloads import StepReportStreamingPayload
from supervisor.reporting.streaming_payloads import StreamingPayload

logger = logging.getLogger(__name__)


class StreamingCallback(Session):
    def __init__(self, job_id: str, callback_url: str, aws_auth: AWSRequestsAuth):
        super().__init__()
        self.job_id = job_id
        self.callback_url = callback_url
        self.auth = aws_auth

    @classmethod
    def from_env_defaults(
        cls, auth: AWSRequestsAuth, job_id: str, callback_url: str
    ) -> Optional[StreamingCallback]:
        if job_id and callback_url:
            return cls(job_id=job_id, callback_url=callback_url, aws_auth=auth)
        logger.warning("Missing job id or callback url values")

    def post(self, payload: StreamingPayload, **kwargs):
        logger.info(f"Posting to {self.callback_url} {StreamingPayload}")
        try:
            response = super().post(
                self.callback_url, json=payload.__json__(), timeout=10, **kwargs
            )
            if not response.ok:
                logger.warning(
                    f"Invalid response {response.status_code}: {response.text}"
                )
            logger.info(f"Received {response.status_code}: {response.text}")
            return response
        except Exception:
            logger.exception("Could not post step payload to endpoint")

    def post_step_update(self, report: StepReport):
        return self.post(StepReportStreamingPayload(report, self.job_id))

    def post_manifest(self, manifest: Manifest):
        return self.post(BotManifestStreamingPayload(manifest, self.job_id))
