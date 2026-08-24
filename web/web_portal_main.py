#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 13 00:28:58 2026

@author: arturo
"""
from web.web_portal_activities import OccWebActivities

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import sys, re

class OccAgent(webdriver.Chrome):
    def __init__(self, variables, teardown=False):
        """
        * Attributes:
            - url_web_page                (str) : Url of the web page to consult.
            - teardown                   (Bool) : Quit session in the browser.
        """
        self.variables:dict = variables
        self.teardown:bool  = teardown

        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Load web driver
        service = Service(ChromeDriverManager().install())
        
        super().__init__(service=service, options=chrome_options)

        # Not show message this web page is being control by driver
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })
        self.implicitly_wait(30)
        self.maximize_window()
        
        
    def open_web_browser(self) -> None:
        """
        Open a web browser (URL web page).
            
            * Arguments:
                None (NoneType) : Not arguments required.
            
            * Returns:
                None (NoneType) : Not returns any value.
        """
        mail_regex_pattern = "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[A-Za-z]{2,7}"
        if bool(re.findall(mail_regex_pattern, self.variables["user_name_mail"], re.IGNORECASE)):        
            self.get(self.variables["url_occ_mundial"])
        else:
            print("Error: Can't open de web page check code.")
            sys.exit()
        
        
    def logging_in_app(self) -> bool:
        """
        Open a web browser (URL web page).
        """
        if not (bool(self.variables["user_name_mail"]) and bool(self.variables["password"])):
            print("Error: Not has been specify credentials in the .env file.")
            sys.exit()

        logging = OccWebActivities(driver= self, variables=self.variables)
        return logging.logging_page()
        
    
    def match_and_apply_in_jobs(self, role, cv_summary)-> None:
        """
        Navigate and surf in the app and apply to the job positions.
        
            * Arguments:
                - cv_summary  (list[str]) : all elements of the summary cv
                - role        (str) : Name of the position to apply.
                
            * Returns:
                None
        """
        apply_positions = OccWebActivities(driver= self, variables=self.variables)
        apply_positions.search_positions_by_match(role=role, cv_summary=cv_summary)
            
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
