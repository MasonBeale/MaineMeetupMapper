import os, subprocess, sys, webbrowser
from pathlib import Path

is_windows = sys.platform.startswith("win")

root = Path(__file__).resolve().parent

if is_windows:
    # Use system Python on Windows
    python_exe = sys.executable
else:
    # Use venv Python on non-Windows
    python_exe = root / ".venv" / "bin" / "python"

env = os.environ.copy()
env.setdefault("FLASK_APP", "app.py")
env.setdefault("FLASK_ENV", "development")

# Start backend
flask = subprocess.Popen(
    [str(python_exe), "-m", "flask", "run"],
    cwd=root / "backend",
    env=env,
)

# Start frontend
npm = subprocess.Popen(
    ["npm", "run", "dev"],
    cwd="frontend",
    shell=is_windows,   # shell=True only on Windows if you need it
)

webbrowser.open("http://localhost:3001")

npm.wait()
flask.terminate()