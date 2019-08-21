from uuid import uuid4


def generate_image_section(filename: str,
                           img_id: str,
                           h: int,
                           w: int):
    """

    """
    filename = filename
    license = 1
    idx = img_id
    data = {
        "license": license,
        "filename": filename,
        "height": h,
        "width": w,
        "id": idx
    }
    return data