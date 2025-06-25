import json
import os
import sys

def saveToText(line_points, file_path = "line_points.json"):
    with open(file_path, "w") as file:
        json.dump(line_points, file)
        
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def load(file_path="line_points.json"):
    full_path = resource_path(file_path)
    if os.path.exists(full_path):
        try:
            with open(full_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {file_path}: {e}")
            return {}
    else:
        print(f"File not found: {full_path}")
        return {}