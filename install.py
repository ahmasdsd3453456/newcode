import subprocess

def run_command(command):
    """Run a shell command and print the output."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Error output: {e.stderr}")

# Commands to run
commands = [
    ["python3", "-m", "pip", "install", "playwright==1.48.0", "beautifulsoup4", "requests"],
    ["python3", "-m", "playwright", "install", "--with-deps"]
]

for command in commands:
    run_command(command)
