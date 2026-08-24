#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 21:09:33 2026

@author: arturo
"""
from dotenv import dotenv_values
from typing import OrderedDict
from pathlib import Path
import traceback
import os

class Config:    
    @classmethod
    def load_info(cls) -> dict:
        """
        Read file "config.env".
        
            * Arguments:
                - None

            * Returns:
                -            (dict) : All variables for the execution.
                -             (str) : Text log error.
        """
        try:
            # Get current work directory
            current_work_dir:str  = Path.cwd()
            #base_path_dir:str     = current_work_dir.parent
            env_path:str          =  os.path.join(current_work_dir, ".env")
            env_vars:OrderedDict  = dotenv_values(env_path)
            
            # Read static varibles in ".env"        
            url_occ_mundial:str     = env_vars.get("URL_OCC_MUNDIAL")
            folder_input:str        = env_vars.get("FOLDER_INPUT")
            folder_output:str       = env_vars.get("FOLDER_OUTPUT")
            img_error_name:str      = env_vars.get("IMG_ERROR_NAME")
            user_name_mail:str      = env_vars.get("USER_NAME_MAIL")
            password:str            = env_vars.get("PASSWORD")
            model_name:str          = env_vars.get("MODEL_NAME")
            json_cv_name:str        = env_vars.get("JSON_CV_NAME")
            match_job_apply:str     = env_vars.get("MATCH_JOB_APPLY")
            review_salay:str        = env_vars.get("REVIEW_SALARY")
            salary_expectations:str = env_vars.get("SALARY_EXPECTATIONS")
            english_level:str       = env_vars.get('ENGLISH_LEVEL')
            match_to_expect:str     = env_vars.get('MATCH_TO_EXPECT')
            location_search_job:str = env_vars.get('LOCATION_SEARCH_JOB')
            log_name:str            = 'log.log'

            # Output llm analisis 
            summary:str             = "summary"
            skills:str              = "skills"
            programming:str         = "programming"
            jobs:str                = "jobs"
            experience:str          = "experience"
            
            end_process_error:bool  = False
            
            return {
                    'url_occ_mundial':url_occ_mundial,
                    'folder_input':folder_input,
                    'folder_output':folder_output,             
                    'log_name': log_name,
                    'end_process_error': end_process_error,
                    'img_error_name':img_error_name,
                    'user_name_mail':user_name_mail,
                    'password':password,
                    'summary':summary,
                    'skills':skills,
                    'programming':programming,
                    'jobs':jobs,   
                    'experience':experience,
                    'model_name':model_name,
                    'json_cv_name':json_cv_name,
                    'match_job_apply':match_job_apply,
                    'review_salay':review_salay,
                    'salary_expectations':salary_expectations,
                    'english_level':english_level,
                    'match_to_expect':match_to_expect,
                    'location_search_job':location_search_job
                    }, ''

        except:
            txt_in_log = "Error: Can't read config file.\n"
            print(f'{txt_in_log}.\n * Error:', traceback.print_exc())
            return {}, txt_in_log
