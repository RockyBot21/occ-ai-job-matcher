#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 00:52:06 2026

@author: arturo
"""
import numpy as np
import cv2 as cv
import pyautogui
import os

class Image:
    def take_screenshot(path_img_input:str=''):
        """
        Take an screenshot.
        
            * Arguments:
                path_img_input (str) : Path image.
            
            * Returns:
                               (str) : Status of the execution.
        """
        try:
            if path_img_input != '':
                if os.path.isfile(path_img_input):
                    os.remove(path_img_input)
                # Take an screenshot
                img = pyautogui.screenshot()
                # Convert capture to BGR 
                img = cv.cvtColor(np.array(img), cv.COLOR_RGB2BGR)
                # Write image
                cv.imwrite(path_img_input, img)                        
                return "Succesfull"
            else:
                return "Error: Not specify the path of image."

        except Exception as e:
            return f"Can't take screenshot. Error {e}"
    
