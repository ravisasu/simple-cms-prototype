# PowerShell helper to install a Git pre-commit hook that runs the consistency checker
param(
    [string]$RepoRoot = ".",
    [string]$HookPath = ".git\hooks\pre-commit"
)

$hookScript = @'
#!/bin/sh
# Run the Python consistency checker; abort commit if inconsistencies exist
python "./scripts/check_status_consistency.py"
if [ $? -ne 0 ]; then
    echo "\nPre-commit: content_status.json inconsistency detected. Commit aborted."
    echo "Run: python ./scripts/check_status_consistency.py --fix to auto-add missing entries (or fix manually)."
    exit 1
fi
'@

Write-Host "Installing pre-commit hook to $HookPath"

$fullHookPath = Join-Path -Path $RepoRoot -ChildPath $HookPath

if (-not (Test-Path -Path (Split-Path $fullHookPath -Parent))) {
    New-Item -ItemType Directory -Path (Split-Path $fullHookPath -Parent) | Out-Null
}

Set-Content -Path $fullHookPath -Value $hookScript -Encoding UTF8

Write-Host "Setting execute permissions (if on Unix)."
try {
    & git update-index --add --chmod=+x $fullHookPath 2>$null
} catch {
    # ignore failures on Windows
}

Write-Host "Pre-commit hook installed. It will run the consistency checker before commits."
