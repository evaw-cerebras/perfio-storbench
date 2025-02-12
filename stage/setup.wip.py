#!/usr/bin/env python
import os
import sys
import shutil
import subprocess
import argparse

# Basic options parser workflow
parser = argparse.ArgumentParser(description='Options for PerfIO-StorBench virtualenv setup.')

parser.add_argument('--env-dir',
                    '-d',
                    type=str,
                    required=True,
                    default='venv',
                    help='Directory to install the venv, [default: venv')

parser.add_argument('--create',
                    '-c',
                    action='store_true',
                    default=False,
                    help='Create the directory if it does not exist. [default: unset]')

args = parser.parse_args()
virtualenv_dir = args.env_dir

# Check dir & create if needed
if args.create and not os.path.exists(virtualenv_dir):
    os.makedirs(virtualenv_dir)

    # Locate 'virtualenv' module command
    virtualenv_command = shutil.which('virtualenv')
    if virtualenv_command is None:
        print("Error: virtualenv python module is not installed, consult the docs.")
        sys.exit(1)

    # Create venv
    print("Creating virtualenv")
    subprocess.check_call([virtualenv_command, virtualenv_dir])

# Ident python version
py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
print(f"PATH prioritized Python version: {py_ver}")

# Set bin and hit go
pybin = sys.executable

print("Activating virtualenv")
venv_activate = virtualenv_dir + "/bin/activate_this.py"
venv_python = virtualenv_dir + "/bin/python"

exec(compile(open(venv_activate, "rb").read(),
             venv_activate,
             'exec'),
     dict(__file__=venv_activate)
     )

# Upgrade pip
subprocess.check_call([venv_python, '-m', 'ensurepip', '--upgrade'])
subprocess.check_call([venv_python, '-m', 'pip', 'install', '--upgrade', 'pip'])

### Put the script you want to load and run below
### or exec(open('script1.py').read())
### or import script1 ; script1.some_function()
