#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 00:31:30 2026

@author: arturo
"""
from json_act.json_act import JsonAct

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaLLM
import pypdf
import json, os

class Llm:
    def __init__(self, input_folder:str, model_name:str, json_cv_name:str):
        """
        * Attributes:
            - input_folder    (str) : Full path folder input.
            - model_name      (str) : Ollama model.
            - json_cv_name    (str) : Name summary json create by llm analysis.
        """
        self.input_folder = input_folder
        self.model_name   = model_name
        self.json_cv_name = json_cv_name
        
    def read_cv_in_pdf(self):
        try:
            # Read cv pdf doc
            with open(self.input_folder, "rb") as file:
                reader = pypdf.PdfReader(file)
                cv_info = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
                
            return cv_info if bool(cv_info) else ''                    

        except Exception as e:
            print(f"Error: {e}")
            return ''            

    def call_llm_capabilities(self, cv_info):
        """
        Call local LLM for to analyce the cv doc.
        
            * Arguments:
                - cv_info  (str) : Analyze the pdf doc (CV text content doc)
            
            * Returns:
                -         Tuple(bool, str|None) : Return boolena execution and text or none content.

        """
        try:
            keys:list[str] = ['summary', 'skills', 'jobs', 'experience']
            dic_val:list[dict] = []
            
            # Init Ollama
            llm = OllamaLLM(model=self.model_name,
                            temperature=0.1)
            
            # Define prompts
            summary_prompt = PromptTemplate.from_template(
                """Summarize this CV in exactly 2 sentences:
    
                    CV:
                        {text}
    
                Summary:"""
            )
            
            skills_prompt = PromptTemplate.from_template(
                """Extract the main skills from the CV below as standalone keywords.
                    Rules:
                    1. Output ONLY two lines: one for 'Technical Skills' and one for 'Soft Skills'.
                    2. Each line must be a comma-separated list of keywords.
                    3. Do NOT include job titles, companies, or explanatory text.
                    
                    CV:
                    ###
                    {text}
                    ###
                    
                    Technical Skills:
                    Soft Skills:"""
            )
            
            jobs_prompt = PromptTemplate.from_template(
                """Analyze the CV below and suggest exactly 3 relevant job titles based on the candidate's experience level and core skills.
    
                    Rules:
                    1. Output MUST be a valid JSON array of exactly 3 strings.
                    2. Do NOT include markdown formatting (like ```json).
                    3. Do NOT include any explanatory text.
                    
                    CV:
                    ###
                    {text}
                    ###
                    
                    Output:"""        
                )
            
            experience_prompt = PromptTemplate.from_template(
                """Analyze the CV below and determine the total years of professional work experience.
    
                    Rules:
                    1. Count ONLY professional work history. IGNORE education, courses, and certifications.
                    2. Calculate the duration if dates are provided.
                    3. Output MUST be a valid JSON object with a single key "years" containing an integer.
                    4. If no experience is found, the value must be 0.
                    5. NO markdown formatting, NO explanatory text.
                    
                    CV:
                    ###
                    {text}
                    ###
                    
                    Output:"""
            )
    
            # Analize info with llm     
            summary_chain = summary_prompt | llm
            skills_chain = skills_prompt | llm
            jobs_chain = jobs_prompt | llm
            experience_chain = experience_prompt | llm
            
            for k in keys:
                query = None
                
                if k == 'summary':
                    print("- Generating summary...")
                    query = summary_chain.invoke({"text": cv_info})
                    query = self.convert_plain_text(txt_input= query)
                            
                elif k == 'skills':
                    print("- Extracting skills...")
                    query = skills_chain.invoke({"text": cv_info})
                    query = self.convert_plain_text(txt_input= query)
            
                elif k == 'jobs':
                    print("- Suggesting job titles...")
                    query = dic_val.append({k : jobs_chain.invoke({"text": cv_info})})
                    query = self.convert_plain_text(txt_input= query)
            
                elif k == 'experience':
                    print("- Calculating years of experience...")
                    query = experience_chain.invoke({"text": cv_info})
                    query = self.convert_plain_text(txt_input= query)
                
                if bool(query):
                    dic_val.append({k : query})
            
            # Convert to JSON
            cv_json = json.dumps(dic_val, indent=4, ensure_ascii=False)
            path_cv_summary = os.path.join(os.path.dirname(self.input_folder), f"{self.json_cv_name}.json")
            cv_summary_result = JsonAct.create_and_write(path_json_file=f"{path_cv_summary}", dictionary=cv_json)
            print("="*50)
            
            if bool(cv_json) and cv_summary_result:  return True, path_cv_summary
            else:                                    return False, None 
            
        except Exception as e:
            msg_err = "Error: Can't analyze the pdf doc file."
            return False, f"{msg_err}\n {e}"
                
        
    @staticmethod
    def call_llm_match_positions(model_name, cv_summary, job_description):
        """
        Compare cv summary vs job offer.
        
            * Arguments:
                - model_name       (str) : Local LLM.
                - cv_summary      (list) : Summary cs (Json).
                - job_description  (str) : Job offer in OCC mundial.
                
            * Returns:
                -                 (json) : Answer question.
        """
        try:
            llm = OllamaLLM(model=model_name, temperature=0)
        
            compare_cv_vs_offer = PromptTemplate.from_template(
            """
                Act as an expert technical recruiter. Your task is to compare a candidate's profile against a job description to determine their level of fit.
                
                **Candidate Profile (Summary):**
                {cv_summary}
                
                **Job Description:**
                {job_description}
                
                Analyze the texts and return ONLY valid JSON. Do not include markdown formatting like ```json. Use exactly the following structure:
                {{
                  "fit_percentage": 85,
                  "recommendation": "A brief 2-line opinion on whether the candidate is a good fit."
                }}
            """)
    
            # Get a dictionary
            parser = JsonOutputParser()
    
            # Compare and analyze info with LLM
            comparison_chain = compare_cv_vs_offer | llm | parser
            
            result_comparison = comparison_chain.invoke({
                                    "cv_summary": cv_summary,
                                    "job_description": job_description
                                })
    
            print(result_comparison)
            return result_comparison

        except Exception as e:
            msg_err = "Can't make comparison cv summary VS job offer."
            print(f"{msg_err}\n {e}")
            return None


    @staticmethod
    def call_llm_skills_comparison(model_name, cv_skills, job_description):
        """
        Compare cv summary vs job offer.
        
            * Arguments:
                - model_name       (str) : Local LLM.
                - cv_skills      (list) : Summary cv (Json).
                - job_description  (str) : Job offer in OCC mundial.
                
            * Returns:
                -                 (json) : Answer question
        """
        try:
            if type(cv_skills) == list:        cv_skills = ' '.join(cv_skills)
            
            llm = OllamaLLM(model=model_name, temperature=0)
        
            compare_cv_vs_offer = PromptTemplate.from_template(
            """
            Act as an expert technical recruiter. Your task is to compare the tools, programs, or technologies that a candidate knows how to use against the requirements of a job offer.
            
                Candidate tools/programs:
                {cv_skills}
                
                Job offer:
                {job_description}
                
                Analyze the information and return ONLY valid JSON. Do not include code tags, comments, or text outside the JSON.
                
                Use exactly this structure:
                {{
                  "fit_percentage": 75,
                  "level": "high|medium|low"
                }}
                
                Rules:
                1. Do not invent tools that do not appear in the offer or in the candidate's profile.
                2. "fit_percentage" must be an integer between 0 and 100.
                3. The value of "level" must be one of the following: "high", "medium", or "low".
            """)
    
            # Get a dictionary
            parser = JsonOutputParser()
    
            # Compare and analyze info with LLM
            comparison_chain = compare_cv_vs_offer | llm | parser
            
            result_comparison = comparison_chain.invoke({
                                    "cv_skills": cv_skills,
                                    "job_description": job_description
                                })
    
            print(result_comparison)
            return result_comparison
        
        except Exception as e:
            msg_err = "Can't make comparison cv skills VS job offer."
            print(f"{msg_err}\n {e}")
            return None        
    
    @staticmethod
    def call_llm_small_question(model_name, prompt, job_description):
        """
        Compare cv summary vs job offer.
        
            * Arguments:
                - model_name       (str) : Local LLM.
                - cv_skills      (list) : Summary cs (Json).
                
            * Returns:
                -                 (json) : Answer question
        """
        try:          
            llm = OllamaLLM(model=model_name, temperature=0)
        
            ask_question = PromptTemplate.from_template(prompt)
    
            # Get a dictionary
            parser = JsonOutputParser()
    
            # Compare and analyze info with LLM
            comparison_chain = ask_question | llm | parser            
      
            result_comparison = comparison_chain.invoke({
                        "job_pos_text": job_description  
                })
                    
            print(result_comparison)
            return result_comparison
        
        except Exception as e:
            msg_err = "Can't answer the small question"
            print(f"{msg_err}\n {e}")
            return None
        
    @staticmethod
    def chat_consult(model_name, context, human_msg):
        """
        Briewl consult (Chat)

            * Arguments:
                - model_name  (str): Model name (ollama).
                - context     (str): If llm take and specific role in the query.
                - human_msg   (str): What a want to evaluate.
        
            * Returns
                -             (str): Return the response (LLM).
        """
        try:
            llm = ChatOllama(model=model_name, temperature=0)

            msgs = [
                SystemMessage(content=context),
                HumanMessage(content=human_msg)
            ]
            answer = llm.invoke(msgs)
            print(answer.content)
            return  answer.content

        except Exception as e:
            msg_err = "Can't answer the small question"
            print(f"{msg_err}\n {e}")
            return None
        
        
    def convert_plain_text(self, txt_input):
        """ Analize if text is a list and convert to string value"""
        if type(txt_input) == list:     return ' '.join(txt_input)
        else:                           return txt_input
        