import subprocess, sys, webbrowser

is_windows = sys.platform.startswith('win')

# Start backend
flask = subprocess.Popen(['python', '-m', 'flask', 'run'] if is_windows else ['flask', 'run'], 
                        cwd='backend')

# Start frontend
npm = subprocess.Popen(['npm', 'run', 'dev'], cwd='frontend', shell=True if is_windows else False)

# Open bowser
webbrowser.open('http://localhost:3001')

npm.wait()
flask.terminate()