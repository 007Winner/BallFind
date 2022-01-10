# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 15:19:20 2022

@author: wmord
"""
import logic_loop
import cv2
import sys

OUT_PATH = "out.avi"

def main():
    
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        input_vid = cv2.VideoCapture(file_path)
        
        frame_width = int(input_vid.get(3))
        frame_height = int(input_vid.get(4))
        size = (frame_width, frame_height)
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(OUT_PATH, fourcc, 30, size)
        
        logic_loop.video_loop(input_vid, out)
        
        print("Done!")
if __name__ == "__main__":
    main()