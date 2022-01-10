# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 12:08:24 2022

@author: wmord
"""

import cv2
import shapes_finder
import img_mod


def video_loop(cap, out):
    """
    Parameters
    ----------
    cap : cv2 VideoCapture object.
    out : cv2 VideoWriter object. 

    Returns
    -------
    Void function. Performs loop logic for identifying ball and locating the
    ball's region. Writes video to @param out. 

    """
    while True:
        ret, frame = cap.read()
        if ret==True: #while we still return frames from cap
            
            regions = shapes_finder.find_regions(frame) #find the court regions contours
            
            ball = shapes_finder.find_ball(frame) #find the ball contour
            
            if ball is not None: #if the ball is in frame:
                curr_region = shapes_finder.find_ball_region(ball, regions) #find which region the ball is in
                
                img_mod.draw_regions(frame, [regions[curr_region - 1]]) #draw the contour for the region that contains the ball, adjust indexing
                img_mod.draw_ball(frame, ball) #Draw the bounding box and center of the ball
                img_mod.write_text(frame, str(curr_region)) #Display the ball's current region with a text overlay
                
                
            
            out.write(frame)
        else:
            break;
            
    #close all windows after iterating through all frames
    cap.release()
    out.release()
    cv2.destroyAllWindows()