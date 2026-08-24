# 🤖 OCC AI Job Matcher (Use LLM Local)

Automated job search flow that uses **local LLMs (Ollama)** to analyze your CV, search for job offers on **OCC Mundial**, and automatically apply to positions that best match your profile.

---

## Features

- **Automatic CV reading** in PDF format
- **Intelligent analysis** using local LLM (Ollama)
- **Automatic job search** on OCC Mundial
- **CV vs Job Offer comparison** with multiple criteria:
  - Technical and soft skills
  - Years of experience
  - English level
  - Salary range
- **Automatic application** to offers that match ≥ 70%
- **Screenshot capture** in case of errors

---

## Prerequisites

Before installing, make sure you have:

- **Python 3.12+**
- **Ollama** installed and running ([download here](https://ollama.com/download))
- **Google Chrome** installed
- **Conda** (optional but recommended)

---

## ⚠️ Limitations and Minimum Requirements

- **Hardware:** Can run on 2nd generation and later equipment without dedicated GPU (using low-end LLMs), although execution time is slow (approx. 3 min per analysis).
- **Windows 11:** Minimum 16 GB of RAM.
- **Linux:** Minimum 8 to 12 GB of RAM (Developed on Debian with Openbox and 8 GB of RAM without dedicated GPU).
- **Recommended model:** RAM consumption depends on the model. For equipment with limited resources, it is recommended to use lightweight models such as `llama3.2:3b`, `qwen2.5:3b` or `phi3:mini`.

> **NOTE:** Currently it does NOT apply to jobs with pop-ups on OCC Mundial, nor does it perform paginated search (planned to be added in future updates).

---

## ⚙️ Configuration (`.env`)

Create a `.env` file in the root of the project with the following variables. Make sure to replace the values between `< >` with your actual information:

```env
# ===== Jobs =====
URL_OCC_MUNDIAL=https://www.occ.com.mx/
LOCATION_SEARCH_JOB=Ciudad de Mexico

# ===== Path files =====
FOLDER_INPUT=<Tu ruta de CVs>
FOLDER_OUTPUT=<Tu ruta de resultados>
IMG_ERROR_NAME=Error.jpg

# ===== Credencial OCC =====
USER_NAME_MAIL=<YOUR_EMAIL@ejemplo.com>
PASSWORD=<YOUR_PASSWORD_OCC>

# ===== Config select LLM =====
MODEL_NAME=llama3.2:latest
JSON_CV_NAME=cv_summary

# ===== Filters for applycation job =====
MATCH_JOB_APPLY=70
REVIEW_SALARY=False
SALARY_EXPECTATIONS=25000
ENGLISH_LEVEL=B2
MATCH_TO_EXPECT=70
```

---

## Usage and folder creation

Create folder and put CV in PDF format

FOLDER_INPUT/
├── mi_cv.pdf                    # Your CV in PDF format
└── cv_summary.json              # Automatically generated

---

### Workflow

1. **Configuration loading** (`.env`)  
   ⬇️  
2. **CV reading** in PDF format  
   ⬇️  
3. **Analysis with LLM (Ollama)**  
   - Summary in 2 sentences  
   - Skill extraction  
   - Job suggestions  
   - Years of experience calculation  
   ⬇️  
4. **Saved in JSON** (local cache)  
   ⬇️  
5. **Browser startup** (web automation)  
   ⬇️  
6. **Login on OCC Mundial**  
   ⬇️  
7. **Search for suggested jobs**  
   ⬇️  
8. **Evaluation of each offer**:  
   - Skills comparison (≥ 70%)  
   - Overall profile match (≥ 70%)  
   - Required English level verification  
   - Salary analysis  
   ⬇️  
9. **If overall match is ≥ 70%** → ✅ **Apply automatically**  
   ⬇️  
10. **Error capture** (screenshot `Error.jpg` in case of failure)

---

### Execution example

```
=====  EXECUTION STARTED =====
Cv summary not exists. Create summary and save it.
- Generating summary...
- Extracting skills...
- Suggesting job titles...
- Calculating years of experience...
==================================================
Enter to the OCC web page & logging successful.
==================================================
Search job suggestion - Desarrollador Python
********** Jobs found **********
- Desarrollador Python Senior
  {'fit_percentage': 85, 'level': 'high'}
  {'fit_percentage': 88, 'recommendation': 'Excellent fit for this position'}
  Apply to the position
- Ingeniero de Machine Learning
  {'fit_percentage': 45, 'level': 'low'}
  {'fit_percentage': 40, 'recommendation': 'Skills mismatch'}
  NOT APPLY to the position
===============================================
=====  EXECUTION ENDED =====
```

*Powered by local LLM (Ollama) · Private · Free · No cloud APIs*
