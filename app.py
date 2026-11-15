"""
Food Delivery Time Prediction System
Entrypoint for Streamlit Community Cloud and Local Execution
Liquid Glass UI Architecture
"""

import os
import sys

# Ensure Code directory is in python search path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODE_DIR = os.path.join(BASE_DIR, 'Code')
if CODE_DIR not in sys.path:
    sys.path.insert(0, CODE_DIR)

# Change working directory to Code directory so relative file paths resolve
os.chdir(CODE_DIR)

# Execute the Liquid Glass Dashboard
dashboard_path = os.path.join(CODE_DIR, 'dashboard.py')
with open(dashboard_path, 'r', encoding='utf-8') as f:
    dashboard_code = compile(f.read(), dashboard_path, 'exec')
    exec(dashboard_code, globals())
