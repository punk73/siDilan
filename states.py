import json
import os

def saveToText(line_points, file_path = "line_points.json"):
    with open(file_path, "w") as file:
        json.dump(line_points, file)

def load(file_path = "line_points.json"):
    res = []

    # Read line_points from a text file

    # Check if the file exists before trying to load it
    if os.path.exists(file_path):
        with open( file_path, "r") as file:
            res = json.load(file)
    
    return res