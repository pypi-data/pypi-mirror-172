from dataclasses import dataclass

from supervisor.reporting.status import Status


@dataclass
class Record:
    record_id: str
    status: Status

    def __json__(self):
        return {
            "id": self.record_id,
            "status": self.status.value,
        }
