def validate_coco(
    coco_dict: dict,
    encoding: list,
    supercategory: str,
    skip_incomplete_annotations: bool = True,
) -> bool:
    """
    Validates the integrity of a COCO format dictionary.

    Args:
        coco_dict (dict): The COCO format dictionary to be validated.
        encoding (list): List of encoding types used for keypoints.
        supercategory (str): The supercategory for which keypoints are validated.
        skip_incomplete_annotations (bool, optional): Whether to skip incomplete annotations or raise an error.
            Defaults to True.

    Raises:
        KeyError: If any of the required keys ('info', 'licenses', 'images', 'annotations', 'categories')
            are missing in the provided COCO dictionary.
        ValueError: If no annotations are found in the COCO dictionary,
            if the encoding of keypoints does not match the expected encoding,
            or if skip_incomplete_annotations is False and an incomplete annotation is found.
        NotImplementedError: If the specified supercategory is not annotated in the COCO dictionary.

    Returns:
        bool: True if the COCO dictionary passes all integrity checks, False otherwise.
    """
    # base required structure
    coco_base_keys = ["info", "licenses", "images", "annotations", "categories"]
    if any([not key in coco_dict.keys() for key in coco_base_keys]):
        for key in coco_base_keys:
            if key in coco_dict.keys():
                continue
            raise KeyError(
                f"Did not found {key} in provided coco_dict. Please ensure coco file format"
            )
    # check if annotation is not-empty
    if len(coco_dict["annotations"]) == 0:
        raise ValueError("No annotations found in the provided coco_dict.")
    # check if keypoints available for selected supercategory in coco dict
    if not any(
        [
            category["supercategory"] == supercategory
            for category in coco_dict["categories"]
        ]
    ):
        raise NotImplementedError(
            f"The selected supercategory {supercategory} is not annotated in the provided coco file."
        )
    # parse category part
    for category in coco_dict["categories"]:
        if category["supercategory"] != supercategory:
            continue
        category_annotation = category
        break
    # check if annotations match desired encoding
    # keypoints have length = n_features * len(encoding)

    n_features = len(category_annotation["keypoints"])
    if not n_features * len(encoding) == len(coco_dict["annotations"][0]["keypoints"]):
        raise ValueError(
            f"You selected {len(encoding)} cordinates/features ({encoding}). The annotation must have {len(coco_dict['annotations'][0]['keypoints']) // n_features } cordinates/features."
        )
    annotations_for_supercategory = False
    # check each annotation whether it is complete
    for annotation in coco_dict["annotations"]:
        # check if annotation matches selected super-category
        if annotation["category_id"] != category_annotation["id"]:
            continue
        # check if coco annotation is consistent
        if len(annotation["keypoints"]) != n_features * len(encoding):
            if skip_incomplete_annotations:
                print(
                    f"WARNING: Skipped annotation {annotation['id']} because it had of missing keypoints (found: {len(annotation['keypoints'])}, expected: {n_features * len(encoding)}). Potentially file corrupted."
                )
                continue
            else:
                raise ValueError(
                    f"Annotation {annotation['id']} has missing keypoints (found: {len(annotation['keypoints'])}, expected: {n_features * len(encoding)}). File potentially corrupted. You can ignore this error and skip this annotation by setting skip_incomplete_annotations=True"
                )
        annotations_for_supercategory = True
    if not annotations_for_supercategory:
        print(
            f"WARNING: Found zero annotations for selected supercategory {supercategory} in coco dict."
        )
    return True
