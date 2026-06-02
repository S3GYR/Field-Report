"""Unified API CRUD validation for FieldReport backend."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SAMPLE_IMAGE = PROJECT_ROOT / "tests" / "assets" / "sample.jpg"

REPORT_PAYLOAD = {
    "number": "RPT-API-001",
    "visit_date": "2024-06-01",
    "client": "ACME Corp",
    "site": "Paris",
    "weather": "sunny",
    "comments": "API test visit",
    "status": "draft",
}


def _create_report(client: TestClient) -> int:
    resp = client.post("/api/reports/", json=REPORT_PAYLOAD)
    assert resp.status_code == 201
    return resp.json()["id"]


class TestReportsCrud:
    def test_create_report(self, client: TestClient) -> None:
        resp = client.post("/api/reports/", json=REPORT_PAYLOAD)
        assert resp.status_code == 201
        data = resp.json()
        assert data["number"] == REPORT_PAYLOAD["number"]

    def test_list_reports(self, client: TestClient) -> None:
        _create_report(client)
        resp = client.get("/api/reports/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_report(self, client: TestClient) -> None:
        report_id = _create_report(client)
        resp = client.get(f"/api/reports/{report_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == report_id

    def test_update_report(self, client: TestClient) -> None:
        report_id = _create_report(client)
        resp = client.put(f"/api/reports/{report_id}", json={"status": "approved"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "approved"

    def test_delete_report(self, client: TestClient) -> None:
        report_id = _create_report(client)
        resp = client.delete(f"/api/reports/{report_id}")
        assert resp.status_code == 204
        assert client.get(f"/api/reports/{report_id}").status_code == 404


class TestPhotosCrud:
    def test_upload_photo(self, client: TestClient) -> None:
        report_id = _create_report(client)
        with SAMPLE_IMAGE.open("rb") as f:
            resp = client.post(
                f"/api/photos/{report_id}",
                files={"file": ("sample.jpg", f, "image/jpeg")},
            )
        assert resp.status_code == 201
        assert resp.json()["filename"]

    def test_list_photos(self, client: TestClient) -> None:
        report_id = _create_report(client)
        with SAMPLE_IMAGE.open("rb") as f:
            client.post(f"/api/photos/{report_id}", files={"file": ("sample.jpg", f, "image/jpeg")})
        resp = client.get("/api/photos/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_photo(self, client: TestClient) -> None:
        report_id = _create_report(client)
        with SAMPLE_IMAGE.open("rb") as f:
            upload = client.post(
                f"/api/photos/{report_id}", files={"file": ("sample.jpg", f, "image/jpeg")}
            )
        photo_id = upload.json()["id"]
        resp = client.get(f"/api/photos/{photo_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == photo_id

    def test_update_photo(self, client: TestClient) -> None:
        report_id = _create_report(client)
        with SAMPLE_IMAGE.open("rb") as f:
            upload = client.post(
                f"/api/photos/{report_id}", files={"file": ("sample.jpg", f, "image/jpeg")}
            )
        photo_id = upload.json()["id"]
        resp = client.put(
            f"/api/photos/{photo_id}", json={"comment": "Updated comment", "priority": "high"}
        )
        assert resp.status_code == 200
        assert resp.json()["comment"] == "Updated comment"
        assert resp.json()["priority"] == "high"

    def test_delete_photo(self, client: TestClient) -> None:
        report_id = _create_report(client)
        with SAMPLE_IMAGE.open("rb") as f:
            upload = client.post(
                f"/api/photos/{report_id}", files={"file": ("sample.jpg", f, "image/jpeg")}
            )
        photo_id = upload.json()["id"]
        resp = client.delete(f"/api/photos/{photo_id}")
        assert resp.status_code == 204
        assert client.get(f"/api/photos/{photo_id}").status_code == 404


class TestTasksCrud:
    def test_create_task(self, client: TestClient) -> None:
        report_id = _create_report(client)
        resp = client.post(
            f"/api/tasks/{report_id}",
            json={
                "description": "Fix leak",
                "status": "todo",
                "estimated_cost": 120.50,
                "estimated_duration": 2.0,
            },
        )
        assert resp.status_code == 201
        assert resp.json()["description"] == "Fix leak"

    def test_list_tasks(self, client: TestClient) -> None:
        report_id = _create_report(client)
        client.post(f"/api/tasks/{report_id}", json={"description": "Task A"})
        resp = client.get("/api/tasks/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_task(self, client: TestClient) -> None:
        report_id = _create_report(client)
        create = client.post(f"/api/tasks/{report_id}", json={"description": "Task B"})
        task_id = create.json()["id"]
        resp = client.get(f"/api/tasks/{task_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == task_id

    def test_update_task(self, client: TestClient) -> None:
        report_id = _create_report(client)
        create = client.post(f"/api/tasks/{report_id}", json={"description": "Task C"})
        task_id = create.json()["id"]
        resp = client.put(f"/api/tasks/{task_id}", json={"status": "done"})
        assert resp.status_code == 200
        assert resp.json()["status"] == "done"

    def test_delete_task(self, client: TestClient) -> None:
        report_id = _create_report(client)
        create = client.post(f"/api/tasks/{report_id}", json={"description": "Task D"})
        task_id = create.json()["id"]
        resp = client.delete(f"/api/tasks/{task_id}")
        assert resp.status_code == 204
        assert client.get(f"/api/tasks/{task_id}").status_code == 404


class TestSignaturesCrud:
    def test_create_signature(self, client: TestClient) -> None:
        report_id = _create_report(client)
        resp = client.post(
            f"/api/signatures/{report_id}",
            json={
                "name": "Alice",
                "role": "Inspector",
                "signed_on": "2024-06-01",
                "signature_image": "base64...",
            },
        )
        assert resp.status_code == 201
        assert resp.json()["name"] == "Alice"

    def test_list_signatures(self, client: TestClient) -> None:
        report_id = _create_report(client)
        client.post(f"/api/signatures/{report_id}", json={"name": "Bob"})
        resp = client.get("/api/signatures/")
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_signature(self, client: TestClient) -> None:
        report_id = _create_report(client)
        client.post(f"/api/signatures/{report_id}", json={"name": "Charlie"})
        resp = client.get(f"/api/signatures/{report_id}")
        assert resp.status_code == 200
        assert resp.json()["name"] == "Charlie"

    def test_update_signature(self, client: TestClient) -> None:
        report_id = _create_report(client)
        client.post(f"/api/signatures/{report_id}", json={"name": "Dave"})
        resp = client.put(f"/api/signatures/{report_id}", json={"name": "David"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "David"

    def test_delete_signature(self, client: TestClient) -> None:
        report_id = _create_report(client)
        client.post(f"/api/signatures/{report_id}", json={"name": "Eve"})
        resp = client.delete(f"/api/signatures/{report_id}")
        assert resp.status_code == 204
        assert client.get(f"/api/signatures/{report_id}").status_code == 404
