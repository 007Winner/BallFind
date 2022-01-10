# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 10:17:09 2022

@author: wmord
"""

import cv2
import math
import img_mod

###GLOBALS###
MAX = 99999999

#################


def cntfind(img, size):
    """
    Parameters
    ----------
    img : CV2 IMAGE
    size : INT, the min size of contours which will be found on @param img

    Returns
    -------
    big_contours : LIST, list of cv2 contours larger than the @param size

    """
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    i = 0
    big_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if i == 0:
            i=1
        
        elif area > size:
            big_contours.append(cnt)

    return big_contours

def find_ball(img):
    """
    Parameters
    ----------
    img : CV2 IMAGE

    Returns
    -------
    ball_cnt : CONTOUR, the contour of the ball.
    If no balls found, returns None.

    """
    mask = img_mod.motionmask(img)
    ball = (cntfind(mask, 5000))
    if len(ball) > 0:
        ball_cnt = ball[0]
        return ball_cnt
    else:
        return None
    

def cnt_center(cnt):
    """
    Parameters
    ----------
    cnt : CV2 CONTOUR.

    Returns
    -------
    ctr : INT TUPLE, the pixel coordinate of @param cnt's center
    
    """
    
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
    ctr = (cx, cy)
    return ctr

def order_regions(regions):
    """
    
    Parameters
    ----------
    regions : LIST, the list of contours that outline each court region.

    Returns
    -------
    finallist : LIST, a sorted list of the above contours which will have each
    contour's index correspond with its court region's official number, as per
    the game rules. Diagram below
    _______
    |  2  |
    |1   3|
    |__4__|
    
    """
    reg_ctr_list = []
    for region in regions:
        ctr = cnt_center(region)
        tup = ctr, region
        reg_ctr_list.append(tup)
    
    templistx = []
    templisty = []
    for entry in reg_ctr_list:
        templistx.append(entry[0][0])
        templisty.append(entry[0][1])
    
    finallist = [0] * len(regions)
    for entry in reg_ctr_list:
        if entry[0][0] == min(templistx):
            finallist[0] = entry[1]
            
        elif entry[0][0] == max(templistx):
            finallist[2] = entry[1]
            
        elif entry[0][1] == min(templisty):
            finallist[1] = entry[1]
            
        else:
            finallist[3] = entry[1]
    
    return finallist


def find_regions(img):
    """
    
    Parameters
    ----------
    img : CV2 IMAGE

    Returns
    -------
    regions : LIST, list of contours -- one for each court region.

    """
    bordered = img_mod.make_border(img) #triangles are not "completed" unless img is bordered
    gray = cv2.cvtColor(bordered, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    regions = cntfind(threshold, 100000)
    
    #Translate the coordinates to account for the offset from the border.
    for region in regions:
        region[:][:][:] = region[:][:][:] - 20

    #cv2 findContours finds contours in different orders on each frame,
    #so we must order the contours on each frame
    regions = order_regions(regions)
    return regions
    

def distance(p1, p2):
    """
    
    Parameters
    ----------
    p1 : INT TUPLE
    p2 : INT TUPLE

    Returns
    -------
    dist : FLOAT, the euclidian distance between p1 and p2

    """
    dist = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)
    return dist

def calc_nearest_region_midpt(pt, contours):
    """
    
    Parameters
    ----------
    pt : INT TUPLE, a tuple.
    contours : LIST, a list of cv2 contours.

    Returns
    -------
    index : INT, the index of the contour in @param contours which is
    the shortest euclidian distance to @param pt
    
    """
    
    ctr_list = []
    for cnt in contours:
        ctr_list.append(cnt_center(cnt))
    
    distances = [MAX] * len(contours)
    for index in range(len(ctr_list)):
        distances[index] = distance(pt, ctr_list[index])
    
    for index in range(len(distances)):
        if distances[index] == min(distances):
            return index + 1
    
    return -1

def find_ball_region(ball, regions):
    """
    
    Parameters
    ----------
    ball : CV2 CONTOUR, the contour of the ball.
    regions : LIST, list of contours -- one contour for each court region.

    Returns
    -------
    INT, returns the index of the region in which @param ball's 
    center is located.

    """
    ball_ctr = cnt_center(ball)

    #the first method for calculating the ball's region with openCV. Works
    #whenever a ball is not crossing over a line.
    count = 0
    for index in range(len(regions)):
        isinregion = cv2.pointPolygonTest(regions[index], ball_ctr, False)
        if isinregion == 1:
            return index + 1
        else:
            count += 1
    
    #geometrically, this method of finding the ball's region always works for
    #the given example. However, if the camera were to pan, trig would need
    #to be used to weigh distances. The above method is a bit more robust, but
    #it cannot be used when the ball crosses over region lines, as the ball's
    #edges become a part of the region contour.
    if count == len(regions):
        return calc_nearest_region_midpt(ball_ctr, regions)
    
    return -1
    
    