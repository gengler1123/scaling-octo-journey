

def send_file_query(cur,
                    conn,
                    fpath: str,
                    height: int,
                    width: int,
                    file_encoding: str = 'png',
                    ):
    """

    """
    query = f"""
    INSERT INTO handwriting_files (fpath, height, width, file_encoding)
    VALUES 
    (
        '{fpath}',
        {height},
        {width},
        '{file_encoding}'
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