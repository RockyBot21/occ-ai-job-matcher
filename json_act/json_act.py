#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 02:55:33 2026

@author: arturo
"""
from typing import Any
import json, os

class JsonAct:
    @staticmethod
    def filter_by_one_element(path_json_file:str, filter_col_name:str) -> str:
        """
        Filter by json element.
            
            * Arguments:
                - path_json_file        (str) : Path of json file.
                - filter_col_name       (str) : Value to filter elements.
            
            * Returns:
                - json_element_filter   (str) : Element or elements in json (Dictionary).
        """
        try:
            data = JsonAct.read_file(path_json_file = path_json_file)
            
            #filter_by_one_element
            if bool(data):
                json_element_filter = data[filter_col_name]
                return json_element_filter
            else:
                print('* Error. No se encontrarón elemetos en el archivo json.')
                return None
                
        except Exception as e:
            print(f'Error al leer archivo json.\n* Error {e}')
        
        
    @staticmethod
    def read_file(path_json_file:str) -> str:
        """
        Read json file.
    
            * Arguments:
                - path_json_file  (str) : Path of json file.
            
            * Returns:
                - data            (str) : Element or elements in json file (Dictionary).
        """
        f      = open(path_json_file)
        data   = json.load(f)
        f.close()        
        return data
    
    @staticmethod
    def create_and_write(path_json_file:str, dictionary:dict[Any]) -> bool:
        """
        write json file with the content.
        
            * Arguments:
                - path_json_file  (str) : Full path json file.
                - dictionary     (dict) : Json content.        
            
            * Returns:
                -                (bool) : File created status.
        """
        try:
            # Serializing & write it
            json_object = json.dumps(dictionary, indent= 4)
            
            with open(path_json_file, "w") as outfile:
            	outfile.write(json_object)
            
            return True if os.path.isfile(path_json_file) else False

        except Exception as e:
            print(f'Error no se pudo crear archivo json: {path_json_file}.\n * Error: {e}')
            return False
