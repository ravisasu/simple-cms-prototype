# Real-time Collaboration (Live Share)

This file lists quick, copy-paste steps to get Visual Studio Code Live Share working for all authors.

## Prerequisites

- Visual Studio Code (recent version).
- Internet access and ability to sign in with a Microsoft or GitHub account.
- If behind a corporate proxy/firewall, ensure outbound HTTPS is allowed.

## 1) Install Live Share (each author)

GUI: Extensions view → search `Live Share` → install `Live Share` (and optionally the Live Share Extension Pack for audio/chat).

PowerShell (install from CLI):

```powershell
# Install core Live Share
code --install-extension ms-vsliveshare.vsliveshare

# Optional: install the Live Share Extension Pack (adds audio/chat)
code --install-extension ms-vsliveshare.vsliveshare-pack

# Verify installation
code --list-extensions | Select-String "vsliveshare"
```

## 2) Sign in

- In VS Code: click the Live Share icon or run `Live Share: Sign In` from the Command Palette.
- Sign in with Microsoft or GitHub (all participants must sign in).

## 3) Host — start a session

- Command Palette → `Live Share: Start Collaboration Session` or click the Live Share status button.
- A shareable link is copied to your clipboard — send to collaborators.

## 4) Guest — join a session

- Click the invite link or run `Live Share: Join Collaboration Session` and paste the link.

## 5) Common session actions

- Follow someone: right-click a participant → `Follow Participant`.
- Share terminal: `Live Share: Share Terminal` (choose read-only or read/write).
- Share server/port: Live Share auto-detects forwarded ports; use the Live Share view to expose them.
- Share debug session: start debug and choose `Share Debug Session`.

## 6) Permissions & security

- Be careful granting terminal write access — only to trusted collaborators.
- End session when done: `Live Share: End Collaboration Session`.

## 7) Troubleshooting

- Can't join: ensure everyone installed Live Share and is signed in; check firewall/proxy settings.
- Audio missing: install the Extension Pack.
- `code` CLI not found: enable the VS Code shell command (Command Palette → `Shell Command: Install 'code' command in PATH`) or install via GUI.

## 8) Quick checklist (for repo contributors)

1. Install Live Share extension.
2. Sign in with Microsoft/GitHub account.
3. Host a session and share the link.
4. Use `Follow` for edits and optionally share terminals/servers.

---
If you want, I can add session templates, an internal policy for sharing terminals, or a short GIF demonstrating join/host flows.
