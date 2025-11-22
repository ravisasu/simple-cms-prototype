<#
Auto demo runner for the Guided Hands-On session.

This script does the following (interactive):
- starts a PowerShell transcript to capture terminal output to `demo_run.log`
- scaffolds a lesson using `create_lesson.py` (opens file in VS Code)
- waits for the presenter to edit the file and press Enter
- runs the consistency checker to auto-fix JSON
- commits and pushes a demo branch

Usage: run from repository root in PowerShell (replace branch name as needed)
  .\auto_demo_runner.ps1 -Branch demo/guided-2025-11-22
#>

param(
    [string]$Branch = "demo/guided-2025-11-22",
    [string]$Title = "Intro to Microsoft Security",
    [string]$Course = "Microsoft-Security",
    [string]$Module = "Module-01",
    [int]$PauseSeconds = 5
)

Start-Transcript -Path .\demo_run.log -Append

Write-Output "Switching to branch: $Branch"
git checkout -b $Branch

Write-Output "Creating module folder (if needed)"
mkdir -Force "Content\$Course\$Module" | Out-Null

Write-Output "Scaffolding lesson (this will open the file in VS Code)..."
python .\scripts\create_lesson.py $Title --course $Course --module $Module --open --run-check

Write-Output "Pausing $PauseSeconds seconds to let the editor open..."
Start-Sleep -Seconds $PauseSeconds

Write-Output "When you finish editing the file, press Enter to continue (this will run the checker and push the branch)."
Read-Host -Prompt "Press Enter after edits"

Write-Output "Running consistency checker to update content_status.json"
python .\scripts\check_status_consistency.py --fix

Write-Output "Staging changes and committing"
git add Content\$Course\$Module\*.md content_status.json
git commit -m "Demo: add $($Title -replace ' ','-') lesson"

Write-Output "Pushing branch to origin: $Branch"
git push --set-upstream origin $Branch

Stop-Transcript

Write-Output "Demo run complete. Transcript saved to demo_run.log"
