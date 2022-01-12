# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 10:17:09 2022

@author: wmord
"""

import cv2
import math
import shapes_finder

###GLOBALS###
GREEN = (0,255,0)
RED = (0,0,255)
BLUE = (255,0,0)

OBJECT_DETECTOR = cv2.createBackgroundSubtractorMOG2(history=3, varThreshold=700, detectShadows = False) 
#################

    
def motionmask(img):
    """
    Parameters
    ----------
    img : CV2 IMAGE.

    Returns
    -------
    mask : CV2 IMAGE, ask is a new image in which non-moving objects will
    masked out. Finding contours of mask will outline those objects that are
    in motion.

    """
    mask = OBJECT_DETECTOR.apply(img)
    return mask

def draw_ball(img, cnt):
    """
    Parameters
    ----------
    img : CV2 IMAGE
    cnt : CV2 CONTOUR, the contour of the ball

    Returns
    -------
    None. Void function that draws box around ball and red dot at center
    of ball onto @param img.

    """
    x,y,w,h = cv2.boundingRect(cnt)
    ball_ctr = shapes_finder.cnt_center(cnt)
    
    cv2.rectangle(img, (x,y), (x+w, y+h), GREEN, 3)
    cv2.circle(img, ball_ctr, 20, RED, -1)


def make_border(img):
    """
    
    Parameters
    ----------
    img : CV2 IMAGE.

    Returns
    -------
    bordered : CV2 IMAGE, an identical image to img with a small white border.
    Useful to "complete" contours that go out of frame.

    """
    borderType = cv2.BORDER_CONSTANT
    
    top = 20
    bottom = top
    left = 20
    right = left
    
    COLOR = (255,255,255)
    bordered = cv2.copyMakeBorder(img, top, bottom, left, right, borderType, None, COLOR)
    return bordered
    
def draw_regions(img, regions, thickness = 5):
    """

    Parameters
    ----------
    img : CV2 IMAGE.
    regions : LIST, a list of cv2 contours.
    thickness : FLOAT, thickness of line drawn around contour, optional

    Returns
    -------
    Void function which traces each contour in #param contours with a red line
    of @param thickness.

    """
    
    for cnt in regions:
        cv2.drawContours(img, [cnt], 0, RED, thickness)

def write_text(img, text, org = (200,200), fontFace = cv2.FONT_HERSHEY_DUPLEX, fontScale = 3.0, color = (125, 246, 55), thickness = 3):
    """
    Parameters
    ----------
    img : CV2 IMAGE, an image.
    text : STRING, the text that will write to the screen.
    org : INT TUPLE, pixel coordinates at which text will be placed, optional.
        he default is (200,200) -- top left corner.
    fontFace : CV2 FONT, the font, optional
        The default is cv2.FONT_HERSHEY_DUPLEX.
    fontScale : FLOAT, font size, optional
        The default is 3.0.
    color : INT TUPLE, BGR color for the text, optional
        DESCRIPTION. The default is (125, 246, 55).
    thickness : FLOAT, the thickness of the text, optional
        The default is 3.

    Returns
    -------
    Void function. Writes @param text to @param org location

    """
    
    frame = cv2.putText(
                  img,
                  text,
                  org,
                  fontFace,
                  fontScale,
                  color,
                  thickness
                )


