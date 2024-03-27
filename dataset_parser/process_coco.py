from utils.dataloader import load_json_coco
from utils.process import process_coco_annotation
from utils.validate import validate_coco
from utils.export import json_export

import argparse


def main(
    coco_path: str,
    export_path: str,
    overwrite: bool,
    encoding: list[str],
    supercategory: str,
    skip_incomplete_annotations: bool,
) -> None:
    # load the COCO json to be processed
    coco_dict = load_json_coco(coco_path)
    # validate COCO before processing it
    if not validate_coco(
        coco_dict, encoding, supercategory, skip_incomplete_annotations
    ):
        return
    # process coco to custom annotation dict
    custom_anno_dict = process_coco_annotation(
        coco_dict, encoding, supercategory, "body_parts"
    )
    # export result to JSON
    json_export(custom_anno_dict, export_path, overwrite)
    print(f"Success! Processed COCO dataset {coco_path} to {export_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process COCO JSON file and export the result to JSON."
    )
    parser.add_argument("--coco_path", type=str, help="Path to the COCO JSON file.")
    parser.add_argument(
        "--export_path", type=str, help="Path to export the processed JSON file."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the export file if it already exists. Default: False",
    )
    parser.add_argument(
        "--encoding",
        nargs="+",
        default=["x", "y", "visibility"],
        help="List of encoding types used for keypoints. Default: ['x', 'y', 'visibility']",
    )
    parser.add_argument(
        "--supercategory",
        type=str,
        default="person",
        help="The supercategory for which keypoints are extracted. Default: 'person'.",
    )
    parser.add_argument(
        "--skip-incomplete-annotations",
        action="store_true",
        help="Skip incomplete annotations instead of raising an error. Default: True",
    )

    args = parser.parse_args()
    main(
        args.coco_path,
        args.export_path,
        args.overwrite,
        args.encoding,
        args.supercategory,
        args.skip_incomplete_annotations,
    )
