# -*- coding: utf-8 -*-
"""Test simple questions app
"""
from datetime import datetime
import unittest

from libs.shared.pram import BaseTestCase
from libs.entering_and_transitioning_app import (
    InvalidConditionError,
    validate_time,
    validate_unique_thread,
    validate_conditions,
)


class TestValidator(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.datefmt = "%Y-%m-%d"  # defaults to midnight utc on given date

    def test_errors_on_non_sundays(self):
        for d in range(1, 7):
            # 1-6 July 2019 are Monday through Saturday
            time = datetime.strptime(f"2019-07-0{d}", self.datefmt)
            with self.assertRaises(InvalidConditionError):
                validate_time(time=time)

        # 7 July 2019 is a Sunday
        time = datetime.strptime(f"2019-07-07", self.datefmt)
        try:
            validate_time(time=time)
        except Exception:
            self.fail()

    def test_handles_offset_timezones(self):
        # Not a Sunday in UTC time
        time = datetime.strptime(f"2019-07-07 00:00:00 +0100", "%Y-%m-%d %H:%M:%S %z")
        with self.assertRaises(InvalidConditionError):
            validate_time(time=time)

    def test_does_not_duplicate_thread(self):
        self.submission.created_utc = datetime.utcnow().timestamp()
        with self.assertRaises(InvalidConditionError):
            validate_unique_thread(last_thread=self.submission)

    def test_validate_conditions_checks_all_conditions(self):
        monday = datetime.strptime("2019-07-01", "%Y-%m-%d")
        self.submission.created_utc = monday.timestamp()
        time = datetime.strptime("2019-07-07", "%Y-%m-%d")

        validate_conditions(last_thread=self.submission, time=time)


if __name__ == "__main__":
    unittest.main()
