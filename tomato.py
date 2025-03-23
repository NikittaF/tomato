#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path
import psutil

TOMATO_DIR = Path.home() / ".tomato"
FORMULAE_DIR = TOMATO_DIR / "Formulae"
INSTALLED_PACKAGES = TOMATO_DIR / "installed.json"

# Инициализация Tomato
TOMATO_DIR.mkdir(exist_ok=True)
FORMULAE_DIR.mkdir(exist_ok=True)
if not INSTALLED_PACKAGES.exists():
    INSTALLED_PACKAGES.write_text(json.dumps({}, indent=4))

def load_installed():
    return json.loads(INSTALLED_PACKAGES.read_text())

def save_installed(data):
    INSTALLED_PACKAGES.write_text(json.dumps(data, indent=4))

def tomato_install(package):
    formula_path = FORMULAE_DIR / f"{package}.json"
    if not formula_path.exists():
        print(f"Package {package} not found.")
        return
    
    formula = json.loads(formula_path.read_text())
    print(f"Installing {package}...")
    subprocess.run(formula["install"], shell=True)
    installed = load_installed()
    installed[package] = formula
    save_installed(installed)
    print(f"{package} installed successfully!")

def tomato_uninstall(package):
    installed = load_installed()
    if package not in installed:
        print(f"Package {package} is not installed.")
        return
    
    formula = installed[package]
    print(f"Uninstalling {package}...")
    subprocess.run(formula["uninstall"], shell=True)
    del installed[package]
    save_installed(installed)
    print(f"{package} uninstalled successfully!")

def tomato_list():
    installed = load_installed()
    print("Installed packages:")
    for package in installed:
        print(f"- {package}")

def tomato_search(package):
    available = [f.stem for f in FORMULAE_DIR.glob("*.json")]
    matches = [p for p in available if package in p]
    print("Found packages:")
    for match in matches:
        print(f"- {match}")

def tomato_update():
    print("Updating package list...")

def tomato_upgrade():
    print("Upgrading installed packages...")

def tomato_run(script):
    print(f"Running script: {script}")
    subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Script {script} started.")

def tomato_status():
    print("Running processes:")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['cmdline'] and 'python' in proc.info['cmdline'][0]:
            print(f"PID: {proc.info['pid']} - {' '.join(proc.info['cmdline'])}")

def main():
    if len(sys.argv) < 2:
        print("Usage: tomato <command> [options]")
        return
    
    command = sys.argv[1]
    if command == "install" and len(sys.argv) > 2:
        tomato_install(sys.argv[2])
    elif command == "uninstall" and len(sys.argv) > 2:
        tomato_uninstall(sys.argv[2])
    elif command == "list":
        tomato_list()
    elif command == "search" and len(sys.argv) > 2:
        tomato_search(sys.argv[2])
    elif command == "update":
        tomato_update()
    elif command == "upgrade":
        tomato_upgrade()
    elif command == "run" and len(sys.argv) > 2:
        tomato_run(sys.argv[2])
    elif command == "status":
        tomato_status()
    else:
        print("Unknown command.")

if __name__ == "__main__":
    main()
