## Demo script (commands-only) for Guided Hands-On

# Create module folder (if needed)
mkdir -Force Content\Microsoft-Security\Module-01

# Scaffold a lesson and run the checker
python .\scripts\create_lesson.py "Intro to Microsoft Security" --course Microsoft-Security --module Module-01 --run-check

# Edit the created file in VS Code (script may open it), then validate JSON
python .\scripts\check_status_consistency.py --fix

# Commit and push demo branch (replace branch name as needed)
git add Content\Microsoft-Security\Module-01\*.md content_status.json
git commit -m "Demo: add intro-to-microsoft-security lesson"
git push --set-upstream origin demo/guided-2025-11-22
