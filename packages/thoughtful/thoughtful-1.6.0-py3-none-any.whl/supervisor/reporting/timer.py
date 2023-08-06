from __future__ import annotations

import datetime
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimerResult:
    """
    The start time, end time, and duration of running a timer.
    """

    start: datetime.datetime
    end: datetime.datetime
    duration: datetime.timedelta


@dataclass
class Timer:
    """
    Times an action by calling `start()` and `end()`.
    """

    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    duration: Optional[datetime.timedelta] = None
    _perf_counter_start_value: Optional[float] = None

    def start(self) -> None:
        """
        Starts the timer.
        """
        self._perf_counter_start_value = time.perf_counter()
        self.start_time = datetime.datetime.now()

    def end(self) -> TimerResult:
        """
        Ends the timer and records the duration.

        Returns:
            TimerResult: How long the timer ran and when it started.
        """
        # Find end time
        end_perf_counter = time.perf_counter()
        self.end_time = datetime.datetime.now()

        # Find duration
        duration_seconds = end_perf_counter - self._perf_counter_start_value
        self.duration = datetime.timedelta(seconds=duration_seconds)

        return TimerResult(
            start=self.start_time, end=self.end_time, duration=self.duration
        )
