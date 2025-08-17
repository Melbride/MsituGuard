#!/usr/bin/env python3
import os
import subprocess
import sys

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {command}")
        print(result.stderr)
        sys.exit(1)
    return result.stdout

if __name__ == "__main__":
    # Install dependencies
    run_command("pip install -r requirements.txt")
    
    # Collect static files
    run_command("python manage.py collectstatic --noinput")
    
    # Run migrations
    run_command("python manage.py migrate --noinput")
    
    print("Build completed successfully!")