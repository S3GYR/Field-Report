from __future__ import annotations

from fastapi.testclient import TestClient


def test_report_crud_flow(client: TestClient) -> None:
    payload = {
        "number": "RPT-001",
        "visit_date": "2024-05-01",
        "client": "ACME Corp",
        "site": "Paris",
        "weather": "sunny",
        "comments": "Initial visit",
        "status": "draft",
    }

    create_resp = client.post("/api/reports/", json=payload)
    assert create_resp.status_code == 201
    report = create_resp.json()
    report_id = report["id"]

    list_resp = client.get("/api/reports/")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    update_resp = client.put(f"/api/reports/{report_id}", json={"status": "approved"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "approved"

    detail_resp = client.get(f"/api/reports/{report_id}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["id"] == report_id

    delete_resp = client.delete(f"/api/reports/{report_id}")
    assert delete_resp.status_code == 204

    final_list = client.get("/api/reports/")
    assert final_list.status_code == 200
    assert final_list.json() == []
