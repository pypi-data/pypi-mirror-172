import pytest
from pytest_httpserver import HTTPServer

from incydr import AlertQuery
from incydr import Client
from incydr._alerts.models.response import AlertDetails
from incydr._alerts.models.response import AlertQueryPage
from incydr._alerts.models.response import AlertSummary

TEST_ALERTS_RESPONSE = {
    "type$": "ALERT_QUERY_RESPONSE",
    "alerts": [
        {
            "type$": "ALERT_SUMMARY",
            "tenantId": "abcd-1234",
            "type": "FED_COMPOSITE",
            "name": "Source Alert",
            "description": "",
            "actor": "user@example.com",
            "actorId": "8675309",
            "target": "N/A",
            "severity": "HIGH",
            "riskSeverity": "CRITICAL",
            "ruleId": "51aa0c99-66e7-44d0-bf2f-c91487796794",
            "watchlists": [
                {
                    "type$": "WATCHLIST",
                    "id": "b366e314-df8c-4c61-a963-7c0d5df31f1e",
                    "name": "SDK_TEST",
                    "type": "WATCHLIST_TYPE_UNSPECIFIED",
                    "isSignificant": True,
                }
            ],
            "id": "d020eee5-0a2d-4255-9f09-83aa7015dabc",
            "createdAt": "2022-09-15T20:48:25.5198280Z",
            "state": "OPEN",
        },
        {
            "type$": "ALERT_SUMMARY",
            "tenantId": "abcd-1234",
            "type": "FED_COMPOSITE",
            "name": "Test Alerts",
            "description": "",
            "actor": "user@example.com",
            "actorId": "8675309",
            "target": "N/A",
            "severity": "HIGH",
            "riskSeverity": "CRITICAL",
            "ruleId": "9fdfec5b-afe1-4531-a8a3-61e1aa2edb91",
            "watchlists": [
                {
                    "type$": "WATCHLIST",
                    "id": "b366e314-df8c-4c61-a963-7c0d5df31f1e",
                    "name": "SDK_TEST",
                    "type": "WATCHLIST_TYPE_UNSPECIFIED",
                    "isSignificant": False,
                }
            ],
            "id": "259a5d1a-8cbb-45e2-af94-28a3a55f2902",
            "createdAt": "2022-09-15T20:48:25.5756820Z",
            "state": "OPEN",
        },
    ],
    "totalCount": 2,
    "problems": [],
}

TEST_ALERT_DETAILS_RESPONSE = {
    "type$": "ALERT_DETAILS_RESPONSE",
    "alerts": [
        {
            "type$": "ALERT_DETAILS",
            "tenantId": "abcd-1234",
            "type": "FED_COMPOSITE",
            "name": "Test Alerts",
            "description": "Test Description",
            "actor": "user@example.com",
            "actorId": "1050590243935435820",
            "target": "N/A",
            "severity": "LOW",
            "riskSeverity": "LOW",
            "ruleId": "9fdfec5b-afe1-4531-a8a3-61e1aa2edb91",
            "id": "7239dede-da58-4214-8bc0-275e0ba8fda5",
            "createdAt": "2022-08-11T20:30:29.7890180Z",
            "state": "OPEN",
            "observations": [
                {
                    "type$": "OBSERVATION",
                    "id": "ee8560eb-99f2-4dc1-9e04-e7d5553dad46-FedEndpointExfiltration",
                    "observedAt": "2022-08-11T19:40:00.0000000Z",
                    "type": "FedEndpointExfiltration",
                    "data": '{"type$":"OBSERVED_ENDPOINT_ACTIVITY","id":"ee8560eb-99f2-4dc1-9e04-e7d5553dad46-FedEndpointExfiltration","sources":["Endpoint"],"exposureTypes":["ApplicationRead"],"exposureTypeIsSignificant":true,"firstActivityAt":"2022-08-11T19:40:00.0000000Z","lastActivityAt":"2022-08-11T19:50:00.0000000Z","fileCount":1,"totalFileSize":50661,"fileCategories":[{"type$":"OBSERVED_FILE_CATEGORY","category":"Spreadsheet","fileCount":1,"totalFileSize":50661,"isSignificant":true}],"fileCategoryIsSignificant":false,"files":[{"type$":"OBSERVED_FILE","eventId":"0_abcd-1234_1070535026524210892_1072902336271326107_0_EPS_DARWIN","path":"/Users/user/Downloads/","name":"quarterly_results.csv","category":"Spreadsheet","size":50661,"riskSeverityInfo":{"type$":"RISK_SEVERITY_INFO","score":3,"severity":"LOW","matchedRiskIndicators":[{"type$":"RISK_INDICATOR","name":"Spreadsheet","weight":0},{"type$":"RISK_INDICATOR","name":"Remote","weight":0},{"type$":"RISK_INDICATOR","name":"Slack upload","weight":3}]},"observedAt":"2022-08-11T19:43:06.8700000Z"}],"riskSeverityIsSignificant":true,"riskSeveritySummary":[{"type$":"RISK_SEVERITY_SUMMARY","severity":"LOW","numEvents":1,"summarizedRiskIndicators":[{"type$":"SUMMARIZED_RISK_INDICATOR","name":"Remote","numEvents":1},{"type$":"SUMMARIZED_RISK_INDICATOR","name":"Slack upload","numEvents":1},{"type$":"SUMMARIZED_RISK_INDICATOR","name":"Spreadsheet","numEvents":1}]}],"syncToServices":[],"sendingIpAddresses":["65.29.159.48"],"isRemoteActivity":true,"appReadDetails":[{"type$":"APP_READ_DETAILS","destinationCategory":"Messaging","destinationName":"Slack"}],"destinationIsSignificant":false}',
                }
            ],
        },
        {
            "type$": "ALERT_DETAILS",
            "tenantId": "abcd-1234",
            "type": "FED_COMPOSITE",
            "name": "Test Alerts",
            "description": "",
            "actor": "user@example.com",
            "actorId": "1050590243935435820",
            "target": "N/A",
            "severity": "HIGH",
            "riskSeverity": "CRITICAL",
            "ruleId": "9fdfec5b-afe1-4531-a8a3-61e1aa2edb91",
            "id": "8bcaef3b-4aa7-46ab-85ae-a2a0191927d9",
            "createdAt": "2022-08-09T14:04:43.0587210Z",
            "state": "OPEN",
            "observations": [
                {
                    "type$": "OBSERVATION",
                    "id": "d34917a2-4c31-4103-9cce-a74b6f0df6d3-FedEndpointExfiltration",
                    "observedAt": "2022-08-09T13:40:00.0000000Z",
                    "type": "FedEndpointExfiltration",
                    "data": '{"type$":"OBSERVED_ENDPOINT_ACTIVITY","id":"d34917a2-4c31-4103-9cce-a74b6f0df6d3-FedEndpointExfiltration","sources":["Endpoint"],"exposureTypes":["ApplicationRead"],"exposureTypeIsSignificant":true,"firstActivityAt":"2022-08-09T13:40:00.0000000Z","lastActivityAt":"2022-08-09T13:50:00.0000000Z","fileCount":1,"totalFileSize":15116,"fileCategories":[{"type$":"OBSERVED_FILE_CATEGORY","category":"SourceCode","fileCount":1,"totalFileSize":15116,"isSignificant":true}],"fileCategoryIsSignificant":false,"files":[{"type$":"OBSERVED_FILE","eventId":"0_abcd-1234_1070535026524210892_1072575657351027611_0_EPS","path":"/Users/user/Downloads/","name":"source.py","category":"SourceCode","size":15116,"riskSeverityInfo":{"type$":"RISK_SEVERITY_INFO","score":9,"severity":"CRITICAL","matchedRiskIndicators":[{"type$":"RISK_INDICATOR","name":"Remote","weight":0},{"type$":"RISK_INDICATOR","name":"Slack upload","weight":3},{"type$":"RISK_INDICATOR","name":"First use of destination","weight":3},{"type$":"RISK_INDICATOR","name":"Source code","weight":3}]},"observedAt":"2022-08-09T13:40:24.5640000Z"}],"riskSeverityIsSignificant":true,"riskSeveritySummary":[{"type$":"RISK_SEVERITY_SUMMARY","severity":"CRITICAL","numEvents":1,"summarizedRiskIndicators":[{"type$":"SUMMARIZED_RISK_INDICATOR","name":"Remote","numEvents":1},{"type$":"SUMMARIZED_RISK_INDICATOR","name":"Slack upload","numEvents":1},{"type$":"SUMMARIZED_RISK_INDICATOR","name":"Source code","numEvents":1},{"type$":"SUMMARIZED_RISK_INDICATOR","name":"First use of destination","numEvents":1}]}],"syncToServices":[],"sendingIpAddresses":["65.29.159.48"],"isRemoteActivity":true,"appReadDetails":[{"type$":"APP_READ_DETAILS","destinationCategory":"Messaging","destinationName":"Slack"}],"destinationIsSignificant":false}',
                }
            ],
            "note": {
                "type$": "NOTE",
                "id": "6867b129-7f57-4acc-9209-360e1b76f249",
                "lastModifiedAt": "2022-09-12T15:56:52.0757340Z",
                "lastModifiedBy": "key-1234",
                "message": "sdk",
            },
        },
    ],
}


def test_alert_query_class(httpserver_auth: HTTPServer):
    query = AlertQuery().equals("State", "OPEN")
    expected = query.dict()
    expected["tenantId"] = "abcd-1234"

    httpserver_auth.expect_request(
        "/v1/alerts/query-alerts", method="POST", json=expected
    ).respond_with_json(TEST_ALERTS_RESPONSE)

    client = Client()
    response = client.alerts.v1.search(query)
    assert isinstance(response, AlertQueryPage)

    with pytest.raises(ValueError):
        client.alerts.v1.search(dict())


def test_iter_all_class(httpserver_auth: HTTPServer):
    query = AlertQuery().equals("State", "OPEN")
    expected = query.dict()
    expected["tenantId"] = "abcd-1234"

    httpserver_auth.expect_request(
        "/v1/alerts/query-alerts", method="POST", json=expected
    ).respond_with_json(TEST_ALERTS_RESPONSE)

    client = Client()
    response = client.alerts.v1.iter_all(query)
    for alert in response:
        assert isinstance(alert, AlertSummary)

    with pytest.raises(ValueError):
        next(client.alerts.v1.iter_all(dict()))


def test_alert_detail_query(httpserver_auth: HTTPServer):
    expected = {"alertIds": ["123", "234"]}
    httpserver_auth.expect_request(
        "/v1/alerts/query-details", method="POST", json=expected
    ).respond_with_json(TEST_ALERT_DETAILS_RESPONSE)

    client = Client()
    response = client.alerts.v1.get_details(["123", "234"])
    assert isinstance(response, list)
    assert isinstance(response[0], AlertDetails)


def test_alert_detail_query_single(httpserver_auth: HTTPServer):
    expected = {"alertIds": ["123"]}
    httpserver_auth.expect_request(
        "/v1/alerts/query-details", method="POST", json=expected
    ).respond_with_json(TEST_ALERT_DETAILS_RESPONSE)

    client = Client()
    response = client.alerts.v1.get_details("123")
    assert isinstance(response, list)
    assert isinstance(response[0], AlertDetails)


def test_alert_add_note(httpserver_auth: HTTPServer):
    expected = {
        "tenantId": "abcd-1234",
        "alertId": "1234",
        "note": "test",
    }
    httpserver_auth.expect_request(
        "/v1/alerts/add-note", method="POST", json=expected
    ).respond_with_data("", status=200)

    client = Client()
    response = client.alerts.v1.add_note("1234", "test")
    assert response.status_code == 200


def test_alert_change_state(httpserver_auth: HTTPServer):
    expected = {
        "tenantId": "abcd-1234",
        "alertIds": ["1234"],
        "state": "PENDING",
        "note": None,
    }
    httpserver_auth.expect_request(
        "/v1/alerts/update-state", method="POST", json=expected
    ).respond_with_data("", status=200)

    client = Client()
    response = client.alerts.v1.change_state(alert_ids=["1234"], state="PENDING")
    assert response.status_code == 200


def test_alert_change_state_single(httpserver_auth: HTTPServer):
    expected = {
        "tenantId": "abcd-1234",
        "alertIds": ["1234"],
        "state": "PENDING",
        "note": None,
    }
    httpserver_auth.expect_request(
        "/v1/alerts/update-state", method="POST", json=expected
    ).respond_with_data("", status=200)

    client = Client()
    response = client.alerts.v1.change_state(alert_ids="1234", state="PENDING")
    assert response.status_code == 200
