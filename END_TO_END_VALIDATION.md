# END_TO_END_VALIDATION

Date : 2026-06-01
Base URL : http://localhost:8200

## Sc&eacute;nario

1. Cr&eacute;er un rapport
2. Ajouter une photo
3. Ajouter une t&acirc;che
4. Ajouter une signature
5. G&eacute;n&eacute;rer un PDF
6. V&eacute;rifier la pr&eacute;sence des donn&eacute;es

## R&eacute;sultats

| &Eacute;tape | Statut | D&eacute;tail |
|------|--------|--------|
| Create report | PASS | HTTP 201, id=1 |
| Add photo | PASS | HTTP 201, id=1 |
| Add task | PASS | HTTP 201, id=1 |
| Add signature | PASS | HTTP 201, id=1 |
| Generate PDF | PASS | HTTP 201, pdf=storage\exports\report-E2E-1780310400.pdf |
| Verify PDF content | PASS | PDF valid=True, size=2.4KB, api_photo=True, api_task=True, api_sig=True |

**Total** : 6 PASS / 0 FAIL

## Preuve

- Rapport cr&eacute;&eacute; : id=1, number=E2E-1780310400
- Photo ajout&eacute;e : id=1
- T&acirc;che ajout&eacute;e : id=1
- Signature ajout&eacute;e : id=1
- PDF g&eacute;n&eacute;r&eacute; : storage\exports\report-E2E-1780310400.pdf
