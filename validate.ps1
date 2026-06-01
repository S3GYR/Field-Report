param(
    [ValidateSet("db", "storage", "pdf", "api", "all")]
    [string]$Target = "all"
)

$python = "python"

function Run-Validation {
    param([string]$Script)
    & $python $Script
    if ($LASTEXITCODE -ne 0) {
        throw "Validation failed for $Script"
    }
}

switch ($Target) {
    "db" { Run-Validation "scripts/validate_database.py" }
    "storage" { Run-Validation "scripts/validate_storage.py" }
    "pdf" { Run-Validation "scripts/validate_pdf.py" }
    "api" { Run-Validation "scripts/validate_api.py" }
    "all" {
        Run-Validation "scripts/validate_database.py"
        Run-Validation "scripts/validate_storage.py"
        Run-Validation "scripts/validate_pdf.py"
        Run-Validation "scripts/validate_api.py"
    }
}
