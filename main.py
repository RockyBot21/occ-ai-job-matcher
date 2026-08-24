#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 21:10:27 2026

@author: arturo
"""
from screenshot.take_an_screenshoot import Image
from folder_act.folder_act import FolderAct
from config.read_config_file import Config
from web.web_portal_main import OccAgent
from json_act.json_act import JsonAct
from llm.make_a_summary import Llm
import os, re, json, ast, sys

if __name__ == "__main__":
    # Read config file
    variables, text_error = Config.load_info() 
    
    if not bool(text_error):
        # Check folder if is empty or not
        file_exists, all_docs = FolderAct.search_all_docs(file_path=variables["folder_input"], pattern="*")
                
        for doc in all_docs:            
            # Process only pdf documents
            if re.findall(r".pdf", doc, re.IGNORECASE):
                txt_analyze = f"{os.path.join(variables['folder_input'], variables['json_cv_name'])}.json"
                exe_result = os.path.isfile(txt_analyze)
                
                if not exe_result:
                    print("Cv summary not exists. Create summary and save it.")
                    # Call Lmm for make a summary of cv doc file
                    call_llm = Llm(input_folder=doc, model_name=variables["model_name"], json_cv_name=variables["json_cv_name"])
                    cv_info = call_llm.read_cv_in_pdf()
                    exe_result, txt_analyze = call_llm.call_llm_capabilities(cv_info= cv_info)
                
                else:
                    print("Cv summary exists: Not analyze pdf document.")
                                
                # If summary is complete and correct continue
                if exe_result and os.path.isfile(txt_analyze):
                    cv_summary = JsonAct.read_file(txt_analyze)
                    if type(cv_summary) == str:
                        cv_summary = json.loads(cv_summary)

                    job_suggestion = [next(iter(e.values())) for e in cv_summary if next(iter(e.keys())) == "jobs"]
                    
                    # Get job suggestions
                    if type(job_suggestion) == list:
                        job_suggestion = list({
                            job 
                            for e in cv_summary 
                            if "jobs" in e 
                            for job in ast.literal_eval(e["jobs"])
                        })
                    # Searcch jobs and apply if match with cv profile
                    with OccAgent(variables=variables, teardown=True) as bot:                        
                        try:
                            bot.open_web_browser()                # Enter the web page
                            load_page = bot.logging_in_app()      # Logging in the platform
                            
                            if not load_page:
                                print("Can't logging web page")
                                print("==================================================")
                                sys.exit()
                                
                            print("Enter to the OCC web page & logging successful.")
                            print("==================================================")
                                
                            for job in job_suggestion:
                                print(f'Search job suggestion - {job}')
                                bot.match_and_apply_in_jobs(role=job, cv_summary=cv_summary)                                    
                            
                        except Exception as e:
                            print(f"Error: {e}")
                            Image.take_screenshot(path_img_input=os.path.join(variables["folder_input"], variables["img_error_name"]))

    else:
        print("ERROR: Can't read config file (.json).\n * ERROR: {text_error}")

    print("=====  EXECUTION ENDED =====")
