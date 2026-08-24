#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 03:06:07 2026

@author: arturo
"""
from glob import glob
import os

class FolderAct:
    @staticmethod 
    def search_all_docs(file_path:str, pattern:str):
        """
        Search all files in the path.
        
            * Arguments:
                - file_path (str) : File path to analyze
                - pattern   (str) : Pattern to take (Depens how you search in the folder)
                
            * Returns:
                -          (bool) : Exists files in path.
                -          (list) : All files in path (If exists).
        """
        try:
            all_docs = glob(f"{os.path.join(file_path, pattern)}")
            
            if bool(all_docs):      return True, all_docs
            else:                   return False, None
        
        except Exception as e:
            msg_error = "Error: Can't search files in folder"
            print(f"{msg_error}\n {e}")
            return False, msg_error 
        

