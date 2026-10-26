# Limitations

- The face workflow is a presence check only, never identity authentication.
- Haar cascades can miss faces or detect false positives under poor lighting/pose.
- Speech input needs an accessible microphone, audio backend, and recognition service.
- TTS voices and Windows app availability vary by host.
- SQLite is local single-user persistence.
- The allowlist intentionally excludes arbitrary shell commands and destructive operations.
- No performance measurements are included until they are collected on the target hardware.
