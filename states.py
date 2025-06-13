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


def load(file_path = "line_points.json"):
    res = []

    # Read line_points from a text file

    # Check if the file exists before trying to load it
    full_path = resource_path(file_path)
    if os.path.exists(full_path):
        with open(full_path, "r") as file:
            res = json.load(file)

    return res