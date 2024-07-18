# StudyCraft <img src="https://github.com/Emanalytics7/StudyCraft/blob/main/artifacts/swan.png" alt="Logo" width="100"/>

## Overview

StudyCraft is a web application that creates a personalized learning schedule of your preferred style and generates a comprehensive PDF of the plan.

Try yourself here 👉   *[StudyCraft](https://study-craft.streamlit.app/)*

Demo: 

https://github.com/user-attachments/assets/b950d6c2-04ec-42dc-8c1d-38804115e91f

## Features

- **Personalized Study Plans**: Tailored to individual goals and learning styles.
- **AI-Powered Content Generation**: Uses LLM for creating study material.
- **Resource Integration**: Extracts and includes useful resources.
- **PDF Generation**: Compiles plans into a downloadable PDF.

## Technologies Used
* **Groq API**:
Used for interacting with Llama3-70b to generate custom study content.
*[Groq API](https://console.groq.com/)*

* **Exa API**:
Extracts and integrates relevant resources from the internet.
*[Exa API](https://exa.ai/)*

* **Google Fonts** :
Uses Google Fonts for styling the generated PDFs. The current font is "Anonymous Pro."

## File Structure 

```plaintext
StudyCraft/
│
├── artifacts/               # Contains generated PDFs and other output files
│   ├── example_output.pdf
│   └── ...
│
├── fonts/                   # Includes custom fonts used in PDF generation
│   ├── AnonymousPro-Regular.ttf
│   └── ...
│  
├── app.py                   # Main Streamlit application file
│                            
├── content_generation.py   # Contains the main logic for generating content based on user input and templates.
│                      
│
├── pdf_conversion.py       # Uses ReportLab to style and compile the final PDF documents.                           
│
└── prompt_template.txt      # Template for AI content generation prompts
```
## Installation

### Prerequisites
- Python 3.10+
- Groq & Exa API credentials [optional in case rate limit occured]

## Steps
Clone the repository:
```bash
git clone https://github.com/Emanalytics7/StudyCraft.git
cd StudyCraft
```
### Install the dependencies:
```bash
pip install -r requirements.txt
```
Set up your API credentials in a .env file.

### Run the application:

```bash
streamlit run app.py
```
## Usage
- Open the application in your browser.
- Enter your study goals, duration, and preferred learning style.
- Generate and download your personalized study PDF.



