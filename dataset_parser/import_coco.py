import json
import os


def json_coco(path: str) -> dict:
    """
    Load COCO dictionary from a JSON file.

    Parameters:
        path (str): Path to the JSON file containing the COCO dictionary.

    Raises:
        FileNotFoundError: If no COCO dictionary is found at the given path.
        json.JSONDecodeError: If the JSON file cannot be decoded.

    Returns:
        dict: COCO dictionary loaded from the JSON file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No COCO dictionary found at the given path: {path}")
    try:
        with open(path, "r") as f:
            coco_dict = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Error decoding JSON file at {path}: {e.msg}", e.doc, e.pos
        )
    return coco_dict
