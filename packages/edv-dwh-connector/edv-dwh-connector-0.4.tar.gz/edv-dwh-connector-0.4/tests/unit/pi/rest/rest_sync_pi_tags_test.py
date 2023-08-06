"""
Test case for RestSyncPITags.
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
import responses
from hamcrest import assert_that, is_, equal_to
from tests.fake_pi_tag import FakePITags
from edv_dwh_connector.pi.rest.rest_sync_pi_tags import RestSyncPITags
from edv_dwh_connector.pi_web_api_client import PiWebAPIClient

BASE_URL = "http://testserver:8078/piwebapi/"
PI_SERVER_ID = "F1DSmN2338899MpX8PREOtdbEZ56sypASVRZLVNSVi1QSS1ISTAx"
WEB_ID = "F1DSmN2338899MpX8PREOtdbEZ56sypASVRZLVNSVi1QSS1ISTAx"

with open(
    file='./tests/resources/tags_api_response.json',
    mode='r', encoding="utf-8"
) as file:
    mock_valid_tags_response_json = json.loads(file.read())


@responses.activate
def test_synchronize_tags() -> None:
    """Test that tags are synchronized"""
    mock_pi_server = responses.Response(
        method='GET',
        url=f"{BASE_URL}dataservers/{PI_SERVER_ID}/points",
        json=mock_valid_tags_response_json,
        status=200,
        content_type='application/json'
    )
    responses.add(mock_pi_server)
    origin = FakePITags()
    origin.add(
        "AI162010_SCLD",
        "AI162010 Carbon Scout Tank 4 pH Scaled Value",
        "pH", WEB_ID
    )
    tags = RestSyncPITags(
        PI_SERVER_ID,
        PiWebAPIClient(
            base_url=BASE_URL,
            use_basic=True,
            username="Administrator",
            password="Password",
            session_timeout=2.5
        ),
        ["AI160014A_SCLD", "AI162007_SCLD"],
        origin
    )
    assert_that(
        tags.has("AI160014A_SCLD"), is_(True),
        "PI tag 1 should be synchronized"
    )
    assert_that(
        tags.has("AI162007_SCLD"), is_(True),
        "PI tag 2 should be synchronized"
    )
    assert_that(
        len(tags.items()), equal_to(3),
        "PI tags count should match"
    )
