

def send_bbox_query(cur,
                    conn,
                    class_text,
                    class_id,
                    x,
                    y,
                    w,
                    h,
                    ref_image,
                    text):
    """

    """
    query = f"""
    INSERT INTO handwriting_bboxes (class_text, class_id, x, y, w, h, fpath, entry_text)
    VALUES
    (
        '{class_text}',
        {class_id},
        {x},
        {y},
        {w},
        {h},
        '{ref_image}',
        '{text}'
    );
    """
    success = True
    try:
        cur.execute(query)
    except Exception as e:
        print(f"Exception: {e}")
        success = False
    finally:
        conn.commit()
    return success