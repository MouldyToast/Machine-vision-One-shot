"""
Resource initialization for PyQt6.

PyQt6 removed pyrcc6 (the resource compiler), so resources are loaded
directly from the filesystem instead of being compiled into a Python module.
"""
import os

RESOURCES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
ICONS_DIR = os.path.join(RESOURCES_DIR, 'icons')
STRINGS_DIR = os.path.join(RESOURCES_DIR, 'strings')
