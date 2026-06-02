# UI_FUNCTIONAL_VALIDATION

Date : 2026-06-01
Base URL : http://localhost:8200

## R&eacute;sultats

| Fonctionnalit&eacute; | Statut | D&eacute;tail |
|----------------------|--------|--------|
| Dashboard page load | PASS | HTTP 200, title present |
| Dashboard seed report | PASS | HTTP 201, id=1 |
| Dashboard counters present | PASS | Counters DOM elements found |
| Report create | PASS | HTTP 201, id=2 |
| Report read | PASS | HTTP 200 |
| Report update | PASS | HTTP 200, status=approved |
| Report delete | PASS | HTTP 204 |
| Photo upload | PASS | HTTP 201, id=1 |
| Photo listed in UI | PASS | photo_id 1 found in /photos HTML |
| Photo delete | PASS | HTTP 204 |
| Task create | PASS | HTTP 201, id=1 |
| Task read | PASS | HTTP 200 |
| Task update | PASS | HTTP 200, status=done |
| Task delete | PASS | HTTP 204 |
| Signature create | PASS | HTTP 201, id=1 |
| Signature read | PASS | HTTP 200 |
| Signature update | PASS | HTTP 200, name=Alice D. |
| Signature delete | PASS | HTTP 204 |
| PDF report create | PASS | HTTP 201, id=2 |
| PDF generate | PASS | HTTP 201, pdf=storage\exports\report-VAL-PDF-1780364860.pdf |
| PDF accessible | PASS | HTTP 200, valid PDF header=True |
| Cleanup seed report | PASS | HTTP 204 |

**Total** : 22 PASS / 0 FAIL / 0 PARTIAL
