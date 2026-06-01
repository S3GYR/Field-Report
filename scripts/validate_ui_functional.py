"""Functional validation of Jinja2 UI connected to FastAPI backend."""

from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

BASE_URL = "http://localhost:8200"
RESULTS: list[dict] = []
_UNIQUE = str(int(time.time()))


def api_call(method: str, path: str, body: dict | None = None) -> tuple[int, dict | str]:
    url = BASE_URL + path
    req = urllib.request.Request(url, method=method)
    if body is not None:
        data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method=method)
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read().decode()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = raw
        return resp.getcode(), payload
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = raw
        return exc.code, payload


def page_call(path: str) -> tuple[int, str]:
    url = BASE_URL + path
    req = urllib.request.Request(url)
    try:
        resp = urllib.request.urlopen(req)
        return resp.getcode(), resp.read().decode()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode()


def record(feature: str, status: str, detail: str) -> None:
    RESULTS.append({"feature": feature, "status": status, "detail": detail})
    print(f"[{status}] {feature}: {detail}")


# ── Dashboard ───────────────────────────────────────────────────────────────
print("=== Dashboard ===")
code, html = page_call("/")
if code == 200 and "Tableau de bord" in html:
    record("Dashboard page load", "PASS", f"HTTP {code}, title present")
else:
    record("Dashboard page load", "FAIL", f"HTTP {code}")

# Seed a report to verify counters reflect real data
code, report = api_call("POST", "/api/reports/", {
    "number": f"VAL-{_UNIQUE}", "visit_date": "2024-06-01", "client": "TestCorp",
    "site": "Lyon", "weather": "sunny", "status": "draft"
})
report_id = report.get("id") if isinstance(report, dict) else None
record("Dashboard seed report", "PASS" if code == 201 else "FAIL", f"HTTP {code}, id={report_id}")

code, html = page_call("/")
counters_ok = code == 200 and "stat-reports" in html and "stat-photos" in html and "stat-tasks" in html
record("Dashboard counters present", "PASS" if counters_ok else "FAIL",
       "Counters DOM elements found" if counters_ok else "Missing counters")

# ── Reports CRUD ────────────────────────────────────────────────────────────
print("\n=== Reports CRUD ===")
code, r = api_call("POST", "/api/reports/", {
    "number": f"VAL-RPT-{_UNIQUE}", "visit_date": "2024-06-10", "client": "ACME",
    "site": "Paris", "weather": "cloudy", "status": "draft"
})
report_id2 = r.get("id") if isinstance(r, dict) else None
record("Report create", "PASS" if code == 201 else "FAIL", f"HTTP {code}, id={report_id2}")

code, r = api_call("GET", f"/api/reports/{report_id2}")
record("Report read", "PASS" if code == 200 else "FAIL", f"HTTP {code}")

code, r = api_call("PUT", f"/api/reports/{report_id2}", {"status": "approved"})
updated = isinstance(r, dict) and r.get("status") == "approved"
record("Report update", "PASS" if (code == 200 and updated) else "FAIL",
       f"HTTP {code}, status={r.get('status') if isinstance(r,dict) else 'N/A'}")

code, _ = api_call("DELETE", f"/api/reports/{report_id2}")
record("Report delete", "PASS" if code == 204 else "FAIL", f"HTTP {code}")

# ── Photos ──────────────────────────────────────────────────────────────────
print("\n=== Photos ===")
sample_img = Path(__file__).resolve().parents[1] / "tests" / "assets" / "sample.jpg"
if sample_img.exists():
    import urllib.request
    boundary = "----WebKitFormBoundary7MA4YWxk"
    with sample_img.open("rb") as f:
        file_data = f.read()
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"sample.jpg\"\r\n"
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(f"{BASE_URL}/api/photos/{report_id}", data=body,
                                   headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        resp = urllib.request.urlopen(req)
        photo_data = json.loads(resp.read().decode())
        photo_id = photo_data.get("id")
        record("Photo upload", "PASS", f"HTTP {resp.getcode()}, id={photo_id}")
    except urllib.error.HTTPError as exc:
        photo_id = None
        record("Photo upload", "FAIL", f"HTTP {exc.code}")
else:
    photo_id = None
    record("Photo upload", "FAIL", "sample.jpg not found")

if photo_id:
    code, html = page_call("/photos")
    photo_listed = code == 200 and str(photo_id) in html
    record("Photo listed in UI", "PASS" if photo_listed else "FAIL",
           f"photo_id {photo_id} found in /photos HTML" if photo_listed else "not found")

    code, _ = api_call("DELETE", f"/api/photos/{photo_id}")
    record("Photo delete", "PASS" if code == 204 else "FAIL", f"HTTP {code}")
else:
    record("Photo listed in UI", "FAIL", "no photo_id")
    record("Photo delete", "FAIL", "no photo_id")

# ── Tasks ───────────────────────────────────────────────────────────────────
print("\n=== Tasks ===")
code, t = api_call("POST", f"/api/tasks/{report_id}", {"description": "Fix roof", "status": "todo"})
task_id = t.get("id") if isinstance(t, dict) else None
record("Task create", "PASS" if code == 201 else "FAIL", f"HTTP {code}, id={task_id}")

code, t = api_call("GET", f"/api/tasks/{task_id}")
record("Task read", "PASS" if code == 200 else "FAIL", f"HTTP {code}")

code, t = api_call("PUT", f"/api/tasks/{task_id}", {"status": "done"})
updated = isinstance(t, dict) and t.get("status") == "done"
record("Task update", "PASS" if (code == 200 and updated) else "FAIL",
       f"HTTP {code}, status={t.get('status') if isinstance(t,dict) else 'N/A'}")

code, _ = api_call("DELETE", f"/api/tasks/{task_id}")
record("Task delete", "PASS" if code == 204 else "FAIL", f"HTTP {code}")

# ── Signatures ──────────────────────────────────────────────────────────────
print("\n=== Signatures ===")
code, s = api_call("POST", f"/api/signatures/{report_id}", {
    "name": "Alice Dupont", "role": "Inspector", "signed_on": "2024-06-01"
})
sig_id = s.get("id") if isinstance(s, dict) else None
record("Signature create", "PASS" if code == 201 else "FAIL", f"HTTP {code}, id={sig_id}")

code, s = api_call("GET", f"/api/signatures/{report_id}")
record("Signature read", "PASS" if code == 200 else "FAIL", f"HTTP {code}")

code, s = api_call("PUT", f"/api/signatures/{report_id}", {"name": "Alice D."})
updated = isinstance(s, dict) and "Alice D." in s.get("name", "")
record("Signature update", "PASS" if (code == 200 and updated) else "FAIL",
       f"HTTP {code}, name={s.get('name') if isinstance(s,dict) else 'N/A'}")

code, _ = api_call("DELETE", f"/api/signatures/{report_id}")
record("Signature delete", "PASS" if code == 204 else "FAIL", f"HTTP {code}")

# ── PDF ─────────────────────────────────────────────────────────────────────
print("\n=== PDF ===")
# Use a dedicated report for PDF to avoid cleanup issues
code, p = api_call("POST", "/api/reports/", {
    "number": f"VAL-PDF-{_UNIQUE}",
    "visit_date": "2024-06-15", "client": "PDF Corp", "site": "Paris",
    "weather": "sunny", "status": "draft"
})
pdf_report_id = p.get("id") if isinstance(p, dict) else None
if code == 201 and pdf_report_id:
    record("PDF report create", "PASS", f"HTTP {code}, id={pdf_report_id}")
    code2, p2 = api_call("POST", f"/api/reports/{pdf_report_id}/generate-pdf")
    pdf_path = p2.get("pdf") if isinstance(p2, dict) else None
    record("PDF generate", "PASS" if (code2 == 201 and pdf_path) else "FAIL",
           f"HTTP {code2}, pdf={pdf_path}")
    if pdf_path:
        url = BASE_URL + "/" + pdf_path.replace("\\", "/")
        req = urllib.request.Request(url)
        try:
            resp = urllib.request.urlopen(req)
            pdf_bytes = resp.read()
            is_pdf = pdf_bytes[:4] == b"%PDF"
            record("PDF accessible", "PASS" if (resp.getcode() == 200 and is_pdf) else "FAIL",
                   f"HTTP {resp.getcode()}, valid PDF header={is_pdf}")
        except urllib.error.HTTPError as exc:
            record("PDF accessible", "FAIL", f"HTTP {exc.code}")
    else:
        record("PDF accessible", "FAIL", "no pdf path")
    # cleanup PDF test report
    api_call("DELETE", f"/api/reports/{pdf_report_id}")
else:
    record("PDF report create", "FAIL", f"HTTP {code}")
    record("PDF generate", "FAIL", "report creation failed")
    record("PDF accessible", "FAIL", "report creation failed")

# ── Cleanup ─────────────────────────────────────────────────────────────────
print("\n=== Cleanup ===")
if report_id:
    code, _ = api_call("DELETE", f"/api/reports/{report_id}")
    record("Cleanup seed report", "PASS" if code == 204 else "FAIL", f"HTTP {code}")

# ── Summary ─────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
passed = sum(1 for r in RESULTS if r["status"] == "PASS")
failed = sum(1 for r in RESULTS if r["status"] == "FAIL")
partial = sum(1 for r in RESULTS if r["status"] == "PARTIAL")
print(f"Results: {passed} PASS, {failed} FAIL, {partial} PARTIAL")

# Write markdown report
report_path = Path(__file__).resolve().parents[1] / "UI_FUNCTIONAL_VALIDATION.md"
lines = [
    "# UI_FUNCTIONAL_VALIDATION",
    "",
    f"Date : 2026-06-01",
    f"Base URL : {BASE_URL}",
    "",
    "## R&eacute;sultats",
    "",
    "| Fonctionnalit&eacute; | Statut | D&eacute;tail |",
    "|----------------------|--------|--------|",
]
for r in RESULTS:
    lines.append(f"| {r['feature']} | {r['status']} | {r['detail']} |")
lines += [
    "",
    f"**Total** : {passed} PASS / {failed} FAIL / {partial} PARTIAL",
    "",
]
report_path.write_text("\n".join(lines), encoding="utf-8")
print(f"Report written to {report_path}")

sys.exit(0 if failed == 0 else 1)
