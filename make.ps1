# PowerShell equivalent of the Makefile (Windows without make).
# Usage: .\make.ps1 setup | data | test | run
param([Parameter(Mandatory = $true)][ValidateSet("setup", "data", "test", "run")][string]$Target)
$ErrorActionPreference = "Stop"
$py = ".\.venv\Scripts\python.exe"
switch ($Target) {
    "setup" {
        python -m venv .venv
        & $py -m pip install --upgrade pip
        & $py -m pip install -r requirements.txt
    }
    "data" {
        foreach ($s in "01_download", "02_build_parquet", "03_build_aggregates", "04_referentiels", "05_build_scores", "06_build_app_tables") {
            & $py "scripts\$s.py"
            if ($LASTEXITCODE -ne 0) { throw "scripts\$s.py failed" }
        }
    }
    "test" { & $py -m pytest -q }
    "run" { & $py -m streamlit run app.py }
}
