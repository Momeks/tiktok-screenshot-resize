#!/usr/bin/env python3
"""Launcher: forwards to the TikTok resize script (see .cursor/skills/tiktok-screenshot-resize/)."""

import runpy
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent / ".cursor/skills/tiktok-screenshot-resize/scripts/resize_for_tiktok.py"
runpy.run_path(str(_SCRIPT), run_name="__main__")
