import os
import json


def json_export(annotation_dict: dict, path: str, overwrite: bool = False) -> None:
    """
    Export dictionary to a JSON file.

    Parameters:
        annotation_dict (dict): Dictionary to be exported to JSON.
        path (str): Path to the JSON file.
        overwrite (bool, optional): Whether to overwrite the file if it already exists.
            Defaults to False.

    Raises:
        FileExistsError: If the file already exists and overwrite is False.
        PermissionError: If the directory cannot be created due to lack of permissions.

    Returns:
        None
    """
    # ensure absolute path
    path = os.path.abspath(path)
    # ensure existence of directory
    directory = os.path.dirname(path)
    # Ensure existence of directory
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except PermissionError:
            raise PermissionError(f"Permission denied to create directory: {directory}")
        print(f"Directory ({directory}) did not exists and was created.")
    # check if file exists
    if os.path.exists(path) and not overwrite:
        raise FileExistsError(
            f"File {path} already exists. Use --overwrite, to overwrite this file."
        )
    # dump file into json
    with open(path, "w") as f:
        json.dump(annotation_dict, f)
