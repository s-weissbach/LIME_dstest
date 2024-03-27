def process_coco_annotation(
    coco_dict: dict,
    encoding: list[str] = ["x", "y", "visibility"],
    supercategory: str = "person",
    keypoints_dictkey: str = "body_parts",
) -> dict:
    """
    Processes COCO annotations and transforms them into a custom annotation format.

    Parameters:
        coco_dict (dict): Dictionary containing COCO annotations.
        encoding (list[str], optional): List of encoding features for keypoints.
            Defaults to ["x", "y", "visibility"].
        supercategory (str, optional): Selected supercategory for processing annotations.
            Defaults to "person".
        keypoints_dictkey (str, optional): Key for storing transformed keypoints in the output dict.
            Defaults to "body_parts".

    Raises:
        KeyError: If any required keys are missing in the coco_dict.
        ValueError: If no annotations are found in the provided coco_dict or if annotations
            do not match the desired encoding.
        NotImplementedError: If the selected supercategory is not annotated in the provided coco_dict.

    Returns:
        dict: Custom annotation dictionary containing processed annotations.
    """
    # validate coco dict
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

    # initalize custom annotation dict
    annotation_dict = {"annotations": []}
    # copy-paste image-info, licence and info
    annotation_dict["info"] = coco_dict["info"]
    annotation_dict["licenses"] = coco_dict["licenses"]
    annotation_dict["images"] = coco_dict["images"]
    # meta info on how to connect keypoints
    annotation_dict["skeleton"] = category_annotation["skeleton"]
    # process annotations
    for annotation in coco_dict["annotations"]:
        # check if annotation matches selected super-category
        if annotation["category_id"] != category_annotation["id"]:
            continue
        # check if coco annotation is consistent
        if len(annotation["keypoints"]) != n_features * len(encoding):
            print(
                f"WARNING: Skipped annotation {annotation['id']} because it had of missing keypoints (found: {len(annotation['keypoints'])}, expected: {n_features * len(encoding)}). Potentially file corrupted."
            )
            continue
        # parse copy-paste annotations
        annotation_entry = {
            "image_id": annotation["image_id"],
            "meta_info": {
                "segmentation": annotation["segmentation"],
                "area": annotation["area"],
                "iscrowd": annotation["iscrowd"],
                "bbox": annotation["bbox"],
                "category_id": annotation["category_id"],
                "id": annotation["id"],
            },
        }
        # the keypoints have to be transformed in the new, desired structure
        # coco annotates keypoints as a plain list, and per keypoint_type, the
        # challenge has by default 3 points [x,y,visible], however, I designed
        # it more flexible, to also enable z-cordinate (if available)
        keypoint_dict = {}
        for i, keypoint_type in enumerate(category_annotation["keypoints"]):
            keypoint_dict[keypoint_type] = {}
            for j, feature in enumerate(encoding):
                keypoint_dict[keypoint_type][feature] = annotation["keypoints"][
                    i * len(encoding) + j
                ]
        annotation_entry[keypoints_dictkey] = keypoint_dict
        annotation_dict["annotations"].append(annotation_entry)
    return annotation_dict
