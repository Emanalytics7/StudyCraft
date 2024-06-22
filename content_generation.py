from exa_py import Exa
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

"""
First the user input: Data science
Second research necessary content
Thrid generate content using llama3
"""

# def collect

def search_engine(query):
    api_key = os.getenv('EXA_API_KEY')
    exa = Exa(api_key)
    response = exa.search(query, num_results=1)
    return response 


results = search_engine('How to become a Data Sciencist')
print(results)


def get_content(resources):
    groq_api = os.getenv('GROOQ_API_KEY')
    llm = ChatGroq(groq_api, model_name = 'llama3-70b-8192', temperature = 0) 

    prompt = "Create a detailed learning schecule based on these resources"