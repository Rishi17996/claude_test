# Kivy Android APK Base

This project is a minimal Kivy app scaffold intended to be built into an Android APK using Buildozer.

Prerequisites (recommended):
- Linux or WSL (Buildozer requires Linux environment)
- Python 3.10+
- Buildozer (install via `pip install buildozer` in Linux)

Quick build steps (on Linux/WSL):

```bash
# Install buildozer and dependencies
pip install --user buildozer

# Initialize build environment (first time)
buildozer android debug

# Build APK
buildozer -v android debug

# Deploy to device
buildozer android deploy run
```

Files:
- `main.py` - minimal Kivy app
- `buildozer.spec` - build configuration
- `requirements.txt` - Python dependencies

Notes:
- Buildozer only runs on Linux. Use WSL2 on Windows.
- Adjust `buildozer.spec` for icons, permissions, and dependencies as needed.
