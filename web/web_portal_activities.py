#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 23:50:41 2026

@author: arturo
"""
from llm.make_a_summary import Llm

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import re

class OccWebActivities:
    def __init__(self, driver:WebDriver, variables):
        """
        * Attributes:
            - driver        (WebDriver) : Webdriver of element of chrome.
            - variables           (int) : Static variables.
        """
        self.driver:WebDriver  = driver
        self.variables:dict    = variables
    

    def search_positions_by_match(self, role:str, cv_summary) -> None:
        """
        Search suggestions in OCC an make match with the positions.
        
            * Arguments:
                - cv_summary  (list[str]) : all elements of the summary cv
                - role        (str) : Name of the position to apply.
                
            * Returns:
                None                 
        """
        role     = '-'.join((role.lower()).split(" "))
        location = '-'.join((self.variables['location_search_job'].lower()).split(" "))
        url = f"{self.variables['url_occ_mundial']}/empleos/de-{role}/en-{location}/"
        self.driver.get(url)
        sleep(4)
        
        all_jobs_search = self.driver.find_elements(By.CSS_SELECTOR, "div[data-offers-grid-offer-item-container]")

        if bool(all_jobs_search):
            print("********** Jobs found **********")
            for job_pos in all_jobs_search:
                try:
                    cover_salary = False
                    cover_language = False
                    
                    # Get info job position
                    job_name = job_pos.find_element(By.TAG_NAME, "h2").text.strip()
                    print(f" - {job_name}")
                    
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", job_pos)
                    sleep(1)

                    self.driver.execute_script("arguments[0].click();", job_pos)
                    sleep(2)

                    job_description = None
                    job_pos_text = self.driver.find_element(By.ID, "job-detail-container").text

                    skills_detec = [next(iter(e.values())) for e in cv_summary if next(iter(e.keys())) == "skills"]

                    cv_skills_comp = Llm.call_llm_skills_comparison(model_name      = self.variables["model_name"],
                                                                    cv_skills       = skills_detec,
                                                                    job_description = job_pos_text)

                    cv_match_comp = Llm.call_llm_match_positions(model_name      = self.variables["model_name"],
                                                                 cv_summary      = cv_summary,
                                                                 job_description = job_pos_text)

                    require_english_offer = Llm.call_llm_small_question(model_name= self.variables["model_name"],
                                                                        prompt= f"""
                                                                        Analyze this job offer and return exclusively a valid JSON object, without markdown, without comments,
                                                                        and without any text before or after.

                                                                            The JSON must have exactly these keys:
                                                                            - "english_req": true or false.
                                                                            - "level": one of "A1", "A2", "B1", "B2", "C1", "C2", "Nativo", "No especificado", or null.
                                                                            
                                                                            Rules:
                                                                            - If English is not mentioned at all, "pide_ingles" must be false and "nivel" must be null.
                                                                            - If it is mentioned as mandatory, desirable, or a requirement, "pide_ingles" must be true.
                                                                            - If English is required but no explicit level is indicated, deduce the most likely level or use "No especificado".
                                                                            - Do not add additional keys.
                                                                            - The booleans true/false and null must be unquoted.
                                                                    
                                                                            Job offer: {{job_pos_text}}
                                                                        """,
                                                                        job_description = job_pos_text)


                    salary_expectations = Llm.call_llm_small_question(model_name= self.variables["model_name"],
                                                                        prompt= f"""
                                                                            You are a salary information extractor for job offers.
                                                                            Analyze the job offer text and return ONLY valid JSON, without markdown, comments, or additional text.
    
                                                                            The JSON must have exactly 4 fields:
                                                                              - "min_salary": null or quntity in number.
                                                                              - "max_salary": null or quntity in number
                                                                              - "mentioned_salary": null or quntity in number or text.
                                                                              - "found": True or false
    
                                                                            Rules:
                                                                            1. "min_salary" and "max_salary" must be numbers or null.
                                                                            2. If the job offer includes a salary range, set "min_salary" to the lower value and "max_salary" to the higher value.
                                                                            3. If the job offer includes a single salary, set the same value for both "min_salary" and "max_salary".
                                                                            4. "mentioned_salary" must contain the literal text or the most faithful representation of the mentioned salary/range, including currency and period if present. If no salary is found, it must be null.
                                                                            5. "found" must be true if any salary, salary amount, or salary range appears in the job offer; otherwise, it must be false.
                                                                            6. If no salary information is found, return the empty json only with the keys.
                                                                            7. Do not invent values or fill missing data with external estimates.
                                                                            8. Normalize obvious abbreviations when the value is clear, for example "24k" to 24000, but keep the original text in "mentioned_salary".
                                                                                   
                                                                            Job offer: {job_pos_text}                                                                        
                                                                        """,
                                                                        job_description = job_pos_text)
                    
                    try:
                        # Get salary expectations             
                        min_salary = salary_expectations['min_salary']
                        max_salary = salary_expectations['max_salary']
                        
                        if (not (bool(min_salary) and bool(max_salary))) and salary_expectations["found"]:
                            # Get salary
                            salary = re.findall(r"(\d[\d,.]*)\s*(?:-|–|—|[aA]\b|al\b|hasta\b)\s*(?:[^0-9\n]*)\s*(\d[\d,.]*)", salary_expectations['mentioned_salary'])
                            min_salary = salary[0][0]
                            max_salary = salary[0][1]
                            
                            if ',' in min_salary:    min_salary = float(min_salary.replace(',', ''))
                            if ',' in max_salary:    max_salary = float(max_salary.replace(',', ''))                       
                            
                            print(f"- Min salary {min_salary}\n- Max Salary {max_salary}")
                        
                        if float(min_salary) >= float(self.variables["salary_expectations"]):
                            cover_salary = True
                    except:
                        print("- Not show salary")
                        cover_salary = True
                    
                    # Get languaje
                    if require_english_offer["english_req"]:
                       match_english = Llm.chat_consult(model_name=self.variables["model_name"],
                                                        context="""
                                                                    You are an English examiner.
                                                                    
                                                                    **ENGLISH LEVEL** (according to CEFR):
                                                                    - A1: Beginner
                                                                    - A2: Elementary
                                                                    - B1: Intermediate low
                                                                    - B2: Intermediate high
                                                                    - C1: Advanced
                                                                    - C2: Mastery
                                                     """, 
                                                     human_msg=f"""
                                                                 The job position requires {require_english_offer['level']}. The applicant is {self.variables["english_level"]}.
    
                                                                    **Rules**
                                                                    - Respond with a boolean indicating whether it covers the requirement or not.
                                                                    - No explanations of any kind.
                                                                    - If no information related to that language appears, respond False.
                                                                    - Only respond with the True or False
                                                     """)
                                    
                       if match_english.lower() == "true":          
                           cover_language = True

                    else:
                        cover_language = False
                        
                    per_match_job = float(self.variables['match_to_expect'])
                    
                    # Check if is match cv with the job offer
                    if (float(cv_skills_comp['fit_percentage']) >= per_match_job) and  (float(cv_match_comp['fit_percentage'])>= per_match_job) and cover_language and cover_salary:
                        print("Apply to the position")
                        btn_apply = self.driver.find_element(By.ID, "btn-apply")
                        print(btn_apply.text)
                        self.driver.execute_script("arguments[0].click();", btn_apply)
                        sleep(4)
                         
                    else:
                        print(f"NOT APPLY to the position: {cv_match_comp['recommendation']}")
                    
                except StaleElementReferenceException:
                    continue
            print("===============================================")
            
    
    def logging_page(self) -> bool:
        """Enter to the OCC mundial web page"""
        try:
            page_load = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "login-link")))        
            if bool(page_load.text):
                page_load.click()
    
                # Insert credential to web page            
                user_cred = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "Email")))
                user_cred.send_keys(self.variables["user_name_mail"])
                
                pass_cred = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Password")))
                pass_cred.send_keys(self.variables["password"])
                sleep(2)
    
                btn_logging = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "btnSubmitPass")))
                btn_logging.click()
    
                main_user_cv = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "Mi CV")))
                return True
            
            return False
    
        except Exception as e:
            print(f"Error: {e}")
            return False
