PYTHON ?= python

.PHONY: validate-db validate-storage validate-pdf validate-api validate-all

validate-db:
	$(PYTHON) scripts/validate_database.py

validate-storage:
	$(PYTHON) scripts/validate_storage.py

validate-pdf:
	$(PYTHON) scripts/validate_pdf.py

validate-api:
	$(PYTHON) scripts/validate_api.py

validate-all: validate-db validate-storage validate-pdf validate-api
