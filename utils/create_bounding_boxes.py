import cv2
import numpy as np


def createBoundingBoxes(mask):
    """

    """

    HMASK = mask.astype(np.uint8)

    HMASK = 255 - HMASK

    contours, hierarchy = cv2.findContours(
        HMASK,
        cv2.RETR_CCOMP,
        cv2.CHAIN_APPROX_SIMPLE
    )
    X = []
    Y = []
    R = []
    B = []
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 1, True)

        x, y, w, h = cv2.boundingRect(approx)

        bot = y + h
        right = x + w

        X.append(x)
        Y.append(y)
        R.append(right)
        B.append(bot)

    x = np.min(X)
    y = np.min(Y)
    r = np.max(R)
    b = np.max(B)
    w = r - x
    h = b - y

    return x, y, w, h
