import os
import re
from groq import Groq
from exa_py import Exa

exa = Exa(os.environ.get('EXA_API_KEY'))
groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))


prompt_template = """
You are an expert in designing comprehensive learning paths. Create a detailed learning path for the following goal:

Goal: {goal} Time period {number}

The learning path should be structured as follows:
1. Title
2. Description
3. Weekly/Daily Schedule
    - Week/Day
        - Topic Title
        - Description
        - Estimated Time
        - Resources/Links
4. Additional Resources
5. Conclusion

Ensure the content is detailed and well-structured. Provide links to external resources where necessary.
"""

def create_prompt(goal, number):
    return prompt_template.format(goal=goal, number=number)


def generate_learning_path(goal, number):
    prompt = create_prompt(goal, number)
    response = groq_client.chat.completions.create(
        messages=[
            {
               "role": "user",
               "content": prompt 
            }
        ],
        model = 'llama3-70b-8192'
        
    )
    return response.choices[0].message.content


def fetch_response(topic):
    response = exa.search(topic, num_results=3)
    resources = []
    for item in response.results:
        resources.append({
            "title": item.title,
            "url": item.url,
            "score": item.score,
            "published_date": item.published_date,
            "author": item.author
        })
    return resources

def integrate_resources(learning_path):
    for week in learning_path['schedule']:
        for topic in week['topics']:
            topic['resources'] = fetch_response(topic['url'])

    return 


print(generate_learning_path('Software engineer', '2 weeks'))