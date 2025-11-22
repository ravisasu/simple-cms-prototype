# Recording Instructions — capture the Guided Hands-On demo

This file explains recommended settings and a simple checklist to record the demo session (screen + audio). Use OBS Studio or the Windows Xbox Game Bar (Win+G). For consistent results I recommend OBS.

Quick checklist

- Install OBS Studio (https://obsproject.com/) or use Win+G to capture.
- Use a quiet room and a headset mic for clear audio.
- Record at 1920x1080 (30 or 60 fps) and 30–40 Mbps bitrate for good quality.

OBS recommended settings

- Capture: use a single window capture for VS Code (or Display Capture if you want the whole desktop).
- Audio: set microphone as your primary input, set desktop audio to capture system sounds.
- Recording format: `mp4` or `mkv` (mkv is safer for crash recovery).
- Encoder: use hardware encoder (NVENC/QuickSync) if available; otherwise x264.

Recording workflow

1. Start OBS and configure a Scene that captures VS Code and your microphone.
2. Start a transcript/log in PowerShell before running demo commands (see `auto_demo_runner.ps1`).
3. Start recording in OBS.
4. Run the demo steps (use `demo_script.ps1` or `auto_demo_runner.ps1`).
5. Stop recording when demo ends and save the file.

Tips for a smooth recording

- Pause after major steps so the viewer can absorb what happened (use `Start-Sleep -Seconds 8`).
- If you want captions, capture the terminal output with `Start-Transcript` (script provided).
- Keep the demo short (10–15 minutes). Trim unnecessary sections in a simple editor.

File naming and upload

- Save with a descriptive filename: `simple-cms-guided-demo-YYYYMMDD.mp4`.
- Upload to your chosen hosting (internal drive, Teams, YouTube unlisted) and include `Demo-cheatsheet.md` as the show notes.
