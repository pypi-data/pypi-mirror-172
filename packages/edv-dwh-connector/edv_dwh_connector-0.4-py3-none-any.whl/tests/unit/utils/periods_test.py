"""
Test case for periods.
.. since: 0.3
"""
# -*- coding: utf-8 -*-
# Copyright (c) 2022 Endeavour Mining
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to read
# the Software only. Permissions is hereby NOT GRANTED to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import datetime
from hamcrest import assert_that, is_, calling, raises
from edv_dwh_connector.utils.periods import DayIntervals,\
    SimplePeriod


def are_equal_to(actual: list, expected: list) -> bool:
    """
    Checks that periods are equal.
    :param actual: Actual periods
    :param expected: Periods expected
    :return: Are equal or not
    """
    if len(actual) == len(expected)\
            and (len(expected) == 0 or len(expected) > 0):
        matches = True
    else:
        matches = False
        print(
            f"Length of periods doesn't match :"
            f" actual -> {len(actual)}, expected -> {len(expected)}"
        )
    if matches:
        for idx, act in enumerate(actual):
            if not (
                # pylint: disable=line-too-long
                act.start() == expected[idx].start() and act.end() == expected[idx].end()  # noqa: E501
            ):
                print(
                    f"Periods [{act.start()}, {act.end()}]"
                    f" and [{expected[idx].start()}, {expected[idx].end()}]"
                    " don't match"
                )
                matches = False
                break
    return matches


def test_generates_day_intervals_on_long_period() -> None:
    """
    Tests that we generate day intervals on period upper than a day.
    """
    periods = DayIntervals(
        datetime(2022, 10, 10, 5, 0, 0),
        datetime(2022, 10, 15, 5, 0, 0)
    )
    expected = [
        SimplePeriod(
            datetime(2022, 10, 10, 5, 0, 0), datetime(2022, 10, 11, 5, 0, 0)
        ),
        SimplePeriod(
            datetime(2022, 10, 11, 5, 0, 0), datetime(2022, 10, 12, 5, 0, 0)
        ),
        SimplePeriod(
            datetime(2022, 10, 12, 5, 0, 0), datetime(2022, 10, 13, 5, 0, 0)
        ),
        SimplePeriod(
            datetime(2022, 10, 13, 5, 0, 0), datetime(2022, 10, 14, 5, 0, 0)
        ),
        SimplePeriod(
            datetime(2022, 10, 14, 5, 0, 0), datetime(2022, 10, 15, 5, 0, 0)
        )
    ]
    assert_that(
        are_equal_to(periods.items(), expected), is_(True),
        "Intervals generated on long period should match"
    )


def test_generates_day_intervals_on_short_period() -> None:
    """
    Tests that we generate day intervals on period less than a day.
    """
    periods = DayIntervals(
        datetime(2022, 10, 10, 5, 0, 0),
        datetime(2022, 10, 10, 12, 0, 0)
    )
    expected = [
        SimplePeriod(
            datetime(2022, 10, 10, 5, 0, 0), datetime(2022, 10, 10, 12, 0, 0)
        )
    ]
    assert_that(
        are_equal_to(periods.items(), expected), is_(True),
        "Intervals generated on short period should match"
    )


def test_generates_day_intervals_on_same_dates() -> None:
    """
    Tests that we generate day intervals on period of same date.
    """
    periods = DayIntervals(
        datetime(2022, 10, 10, 5, 0, 0),
        datetime(2022, 10, 10, 5, 0, 0)
    )
    expected = [
        SimplePeriod(
            datetime(2022, 10, 10, 5, 0, 0), datetime(2022, 10, 10, 5, 0, 0)
        )
    ]
    assert_that(
        are_equal_to(periods.items(), expected), is_(True),
        "Intervals generated on same dates should match"
    )


def generate_intervals(start: datetime, end: datetime) -> None:
    """
    Generates intervals.
    :param start: Start date
    :param end: End date
    """
    DayIntervals(start, end).items()


def test_generates_day_intervals_on_wrong_period() -> None:
    """
    Tests that we generate day intervals on wrong period.
    """
    assert_that(
        calling(generate_intervals).with_args(
            datetime(2022, 10, 10, 5, 0, 0),
            datetime(2022, 10, 9, 5, 0, 0)
        ),
        raises(
            ValueError,
            "Bad range, dates are equals or start date"
            " is greater than end date"
        ),
        "Should not generate intervals on wrong period"
    )
