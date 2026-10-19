# Run a pipeline script in the background, at low CPU priority, with a log file (keeps the machine usable).
# Usage: .\scripts\run_logged.ps1 03_build_aggregates [extra args]
# Log: data\interim\logs\<script>_<yyyyMMdd_HHmmss>.log ; follow it with: Get-Content <log> -Wait
param([Parameter(Mandatory = $true)][string]$Script, [Parameter(ValueFromRemainingArguments = $true)][string[]]$Rest)
$root = Split-Path -Parent $PSScriptRoot
$logs = Join-Path $root "data\interim\logs"
New-Item -ItemType Directory -Force $logs | Out-Null
$log = Join-Path $logs ("{0}_{1}.log" -f $Script, (Get-Date -Format "yyyyMMdd_HHmmss"))
$py = Join-Path $root ".venv\Scripts\python.exe"
$pyArgs = @("-u", "scripts\$Script.py") + @($Rest | Where-Object { $_ })
$p = Start-Process -FilePath $py -ArgumentList $pyArgs -WorkingDirectory $root -WindowStyle Hidden `
    -RedirectStandardOutput $log -RedirectStandardError "$log.err" -PassThru
$p.PriorityClass = "BelowNormal"
Write-Output "PID $($p.Id) -> $log"
