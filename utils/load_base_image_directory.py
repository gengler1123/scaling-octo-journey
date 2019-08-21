from os import listdir
from os.path import join


def return_base_image_paths():
    """

    :return:
    """
    base_path = "/data/handwriting/words/"
    base_words = [
        join(base_path, d) for d in listdir(base_path)
    ]
    print(f"Number of Base Word Directories: {len(base_words)}")

    files = []
    for bw in base_words:
        subdirs = [
            join(bw, f) for f in listdir(bw)
        ]
        for sd in subdirs:
            files.extend(
                [
                    join(sd, f) for f in listdir(sd)
                ]
            )
    return files
