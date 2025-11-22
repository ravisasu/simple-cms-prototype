## quick_demo.ps1
# Minimal Quick Demo script: scaffold a lesson, run the checker

param(
    [string]$Title = "Quick Demo Lesson",
    [string]$Course = "Microsoft-Security",
    [string]$Module = "Module-01"
)

Write-Output "Creating module folder if needed..."
mkdir -Force "Content\$Course\$Module" | Out-Null

Write-Output "Scaffolding lesson..."
python .\scripts\create_lesson.py $Title --course $Course --module $Module --run-check

Write-Output "Run the checker (already run by scaffold with --run-check), but you can run again:" 
Write-Output "python .\scripts\check_status_consistency.py --fix"

Write-Output "Quick demo complete. Edit the created file in VS Code if you want to show content changes."
