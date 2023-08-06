"""
Test case for RestSyncPIMeasures.
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

import json
from datetime import datetime
from hamcrest import assert_that, is_, equal_to
import responses
from tests.fake_pi_tag import FakePITag
from tests.fake_pi_measure import FakePIMeasures
from edv_dwh_connector.pi.rest.rest_sync_pi_measures import RestSyncPIMeasures
from edv_dwh_connector.pi_web_api_client import PiWebAPIClient
from edv_dwh_connector.utils.periods import SingleInPeriods

BASE_URL = "http://testserver:8078/piwebapi/"
WEB_ID = "F1DPmN2MpX8PREOtdbEZ56sypAQwIAAASVRZLVNSVi1QSS1ISTAxXEFJMTYwMDE0QV9TQ0xE"  # noqa: E501

with open(
    file='./tests/resources/tag_data_api_response.json',
    mode='r', encoding="utf-8"
) as file:
    mock_valid_tag_data_response_json = json.loads(file.read())


def all_data_belong_to_period(
    data: list, start: datetime, end: datetime
) -> bool:
    """
    Checks that all data belong to period.
    :param data: List of data
    :param start: Start date
    :param end: End date
    :return: All data belong or not
    """
    matches = True
    for dat in data:
        if not start <= dat.date() <= end:
            matches = False
            break
    return matches


@responses.activate
def test_synchronize_tags() -> None:
    """Test that tag data are synchronized"""
    mock_response = responses.Response(
        method='GET',
        url=f"{BASE_URL}streamsets/recorded?webId={WEB_ID}"
        "&startTime=2022-01-01T00:00:00.000Z"
        "&endTime=2022-01-05T00:00:00.000Z",
        json=mock_valid_tag_data_response_json,
        status=200,
        content_type='application/json'
    )
    responses.add(mock_response)
    tag = FakePITag(
        1, "AI160014A_SCLD",
        "CIL Free Cyanide Analyser pH Indicator Tank 1 Scaled Value", "pH",
        WEB_ID
    )
    origin = FakePIMeasures(tag)
    start = datetime(2022, 1, 1)
    end = datetime(2022, 1, 5)
    measures = RestSyncPIMeasures(
        PiWebAPIClient(
            base_url=BASE_URL,
            use_basic=True,
            username="Administrator01",
            password="Password02",
            session_timeout=2.5
        ),
        tag, SingleInPeriods(start, end), origin
    )
    data = measures.items(start, end)
    assert_that(
        all_data_belong_to_period(data, start, end), is_(True),
        "Tag data should belong to period"
    )
    assert_that(
        len(data), equal_to(980),  # Real total is 984. There is 4 wrong data.
        "Tag data count should match"
    )
