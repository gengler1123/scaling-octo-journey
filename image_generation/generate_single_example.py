from random import choice, randint
from typing import List
import cv2
import numpy as np
from uuid import uuid4
from utils import createBoundingBoxes, generate_image_section, generate_annotations
import matplotlib.pyplot as plt
import psycopg2 as psql
from db_writes import send_file_query, send_bbox_query


def generate_single_example(TEXT_SAMPLES: List[str],
                            IMG_FILES: List[str],
                            write_dir: str,
                            img_type: str="png",
                            print_img: bool=False,
                            base_height: int=400,
                            base_width: int=1000,
                            db_conn: psql.connect=None):
    """

    :return:
    """
    BASE_IMG = np.zeros((base_height, base_width)) + 255
    BASE_IMG = BASE_IMG.astype(np.uint16)

    text = choice(TEXT_SAMPLES)
    font = cv2.FONT_HERSHEY_PLAIN
    font_scale = 4
    font_thickness = 2
    (label_width, label_height), baseline = cv2.getTextSize(
        text,
        font,
        font_scale,
        font_thickness
    )

    leftMargin = randint(50, 150)
    topOffset = randint(label_height + 150, label_height + 250)

    TEXT_MASK = BASE_IMG.copy()

    TEXT_MASK = cv2.putText(
        TEXT_MASK,
        text,
        (leftMargin, topOffset),
        font,
        font_scale,
        (0,),
        font_thickness,
        cv2.LINE_AA
    )

    img_file = choice(IMG_FILES)
    img = cv2.imread(img_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = img.shape
    while w < 100:
        img_file = choice(IMG_FILES)
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = img.shape

    WRITING_MASK = BASE_IMG.copy()

    writingOffset = leftMargin + label_width + randint(10, 120)

    randomYOffset = 0 # randint(-20, 30)

    rightPoint = writingOffset + w

    offset = rightPoint - base_width
    if offset < 0:
        offset = 0

    if rightPoint >= base_width:
        rightPoint = base_width

    if offset == 0:
        copy_img = img
    else:
        copy_img = img[:, :-offset]

    WRITING_MASK[
        topOffset - h + randomYOffset:topOffset + randomYOffset,
        writingOffset:rightPoint
    ] = copy_img

    """

    FORM LINES

    """

    LINE_MASK_0 = BASE_IMG.copy()

    entryLineOffset = leftMargin + label_width + 10

    qt1 = (entryLineOffset, topOffset)
    qt2 = (entryLineOffset + w + 60, topOffset)
    cv2.line(
        LINE_MASK_0,
        qt1,
        qt2,
        (0,),
        5
    )

    TEXT_BBOX = createBoundingBoxes(TEXT_MASK)
    WRITING_BBOX = createBoundingBoxes(WRITING_MASK)
    LINE_BBOX = createBoundingBoxes(LINE_MASK_0)

    """
    Write Image
    """
    TEXT_MASK = 255 * TEXT_MASK / np.max(TEXT_MASK)
    WRITING_MASK = 255 * WRITING_MASK / np.max(WRITING_MASK)
    LINE_MASK_0 = 255 * LINE_MASK_0 / np.max(LINE_MASK_0)

    WRITE_IMG = TEXT_MASK + WRITING_MASK + LINE_MASK_0

    WRITE_IMG = WRITE_IMG.astype(np.uint16)

    img_id = f"{uuid4()}"
    filename = f"{img_id}.{img_type}"
    write_path = f"{write_dir}/{filename}"
    cv2.imwrite(write_path, WRITE_IMG)

    IMG = generate_image_section(
        filename,
        img_id,
        h=base_height,
        w=base_width
    )
    """
    
    """

    if db_conn is not None:
        cur = db_conn.cursor()
        f_suc = send_file_query(
            cur=cur,
            conn=db_conn,
            fpath=write_path,
            height=base_height,
            width=base_width,
            file_encoding=img_type
        )
        if f_suc:
            text_suc = send_bbox_query(
                cur=cur,
                conn=db_conn,
                class_text="typed_text",
                class_id=0,
                x=TEXT_BBOX[0],
                y=TEXT_BBOX[1],
                w=TEXT_BBOX[2],
                h=TEXT_BBOX[3],
                ref_image=write_path,
                text=text
            )
            hand_suc = send_bbox_query(
                cur=cur,
                conn=db_conn,
                class_text="handwriting",
                class_id=1,
                x=WRITING_BBOX[0],
                y=WRITING_BBOX[1],
                w=WRITING_BBOX[2],
                h=WRITING_BBOX[3],
                ref_image=write_path,
                text="<handwriting>"
            )
            line_suc = send_bbox_query(
                cur=cur,
                conn=db_conn,
                class_text="form_line",
                class_id=2,
                x=LINE_BBOX[0],
                y=LINE_BBOX[1],
                w=LINE_BBOX[2],
                h=LINE_BBOX[3],
                ref_image=write_path,
                text="<form_line>"
            )
        else:
            print(f"File Did Not Return Success")
    else:
        print(f"No Database Connection")

    """
    Create Annotation Elements
    """

    annotations = []
    # TEXT Annotation
    annotations.append(
        generate_annotations(
            TEXT_BBOX,
            f"{uuid4()}",
            img_id,
            cat_id=2
        )
    )

    annotations.append(
        generate_annotations(
            WRITING_BBOX,
            f"{uuid4()}",
            img_id,
            cat_id=3
        )
    )

    annotations.append(
        generate_annotations(
            LINE_BBOX,
            f"{uuid4()}",
            img_id,
            cat_id=1
        )
    )

    ret_data = {
        "image": IMG,
        "annotations": annotations
    }

    return ret_data
