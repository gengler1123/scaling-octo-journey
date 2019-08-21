


def generate_annotations(bbox, idx, image_id, cat_id):
    """

    :param bbox:
    :param idx:
    :param image_id:
    :param cat_id:
    :return:
    """
    x, y, w, h = bbox
    area = w * h
    iscrowd = 0

    data = {
        "area": area,
        "iscrowd": iscrowd,
        "image_id": image_id,
        "bbox": bbox,
        "category_id": cat_id,
        "id": idx
    }
    return data