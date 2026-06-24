# Death Counter

Small app to track deaths per game, chapter/area, and boss. Data is stored in `deaths.json`.

Usage
-----

- Run the GUI (Tkinter is included with CPython):

```powershell
python main.py
```

- Force the CLI:

```powershell
python main.py --cli
```

Windows launchers
-----------------

Two simple batch files are included for convenience on Windows:

- `run-ui.bat` — launches the GUI (runs `python main.py`)
- `run-cli.bat` — launches the CLI (runs `python main.py --cli`)

Double-click a `.bat` file or run it from PowerShell to start the app.

Notes
-----

- This project no longer depends on Kivy. The GUI uses Tkinter so no extra packages are required for the UI.
- If you want a packaged desktop app later, I can add a PyInstaller script to produce an EXE.
