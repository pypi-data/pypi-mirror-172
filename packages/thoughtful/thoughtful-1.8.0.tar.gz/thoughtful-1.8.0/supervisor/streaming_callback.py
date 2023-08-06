from __future__ import annotations

import logging
import os
from typing import Optional

from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests import Session

import supervisor
from supervisor.reporting.step_report import StepReport

logger = logging.getLogger(__name__)


class StreamingCallback(Session):
    def __init__(self, job_id: str, callback_url: str, aws_auth: AWSRequestsAuth):
        super().__init__()
        self.job_id = job_id
        self.callback_url = callback_url
        self.auth = aws_auth

    @classmethod
    def from_env_defaults(cls, auth: AWSRequestsAuth) -> Optional[StreamingCallback]:
        job_id = os.environ.get("RC_PROCESS_RUN_ID")
        callback_url = os.environ.get("SUPERVISOR_CALLBACK_URL")
        if job_id and callback_url:
            return cls(job_id, callback_url, auth)
        else:
            logger.warning("Missing job id or callback url environment variables")
            return None

    def post_step_update(self, report: StepReport):
        _json = {
            "job_id": self.job_id,
            "client": supervisor.__name__,
            "version": supervisor.__version__,
            "action": "step_report",
            "payload": report.__json__(),
        }
        logger.info(f"Posting to {self.callback_url} {_json}")
        try:
            response = self.post(self.callback_url, json=_json, timeout=10)
            if not response.ok:
                logger.warning(
                    f"Invalid response {response.status_code}: {response.text}"
                )
            logger.info(f"Received {response.status_code}: {response.text}")
            return response
        except Exception:
            logger.exception("Could not post step payload to endpoint")
