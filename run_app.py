#!/usr/bin/env python
"""Wrapper to run the Streamlit app with proper path configuration."""
import sys
import os
import subprocess

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Run streamlit with proper environment
env = os.environ.copy()
env['PYTHONPATH'] = project_root + os.pathsep + env.get('PYTHONPATH', '')

venv_python = os.path.join(project_root, '.venv', 'Scripts', 'python.exe')
subprocess.run([venv_python, '-m', 'streamlit', 'run', 'src/ui/app.py'], cwd=project_root, env=env)
