"""
Tests Init
"""

import os

from dotenv import load_dotenv

load_dotenv()

config = {
    "api_key": os.getenv("API_KEY", ""),
    "api_base_url": os.getenv("API_BASE_URL", "http://127.0.0.1:8000"),
    "curp": os.getenv("CURP", ""),
    "timeout": int(os.getenv("TIMEOUT", "10")),
}
