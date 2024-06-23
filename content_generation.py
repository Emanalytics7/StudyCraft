from exa_py import Exa
from groq import Groq
import os

exa = Exa(os.environ.get("EXA_API_KEY"))
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def search_engine(user_query):
    results = exa.search(user_query, num_results=3)
    return results

def generate_content(preferences):
    goal = preferences['goal']
    duration = preferences['duration']
    style = preferences['style']
    
    courses = search_engine(f"{goal} courses links")
    tutorials = search_engine(f"{goal} tutorials links")
    documentation = search_engine(f"{goal} documentation links ")
    articles = search_engine(f"{goal} articles links")
    projects = search_engine(f"{goal} capstone projects links")

    template = """
# {duration} {goal} Learning Schedule

## Adapt this title according to the {duration}
e.g (for weeks use week and for months use months etc.)

### Topics
1. {topic1}: {description1}
2. {topic2}: {description2}
3. {topic3}: {description3}

### Resources
- ({resource_link1})
- ({resource_link2})
- ({resource_link3})

### Practical Exercises
- {exercise1}
- {exercise2}
- {exercise3}

### Assessments
- {assessment1}
- {assessment2}
- {assessment3}

---
"""

    prompt = f"""
I want to become a {goal} within {duration} following a {style} learning approach. 
Please create a comprehensive learning schedule to help me achieve this goal. 
Break down the schedule into weekly segments, specifying the topics to be covered each week, the time to be spent on each topic, and the resources to be used. 
Include a mix of theoretical learning, practical exercises, projects, and assessments. 
Also, provide guidance on how to integrate these learning activities into daily study routines. 

Use the following template:

{template}

User the following links with each related topic above from here: [Mandatory]
{courses}\n{tutorials}\n{documentation}\n{articles}\n{projects}         

Add two motivate quotes in the start and end.Avoid ('Here is your' sentence) Be straightforward and professional.
"""

    response = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-70b-8192"
    )

    return response.choices[0].message.content

# # # Example usage
# user_preferences = {
#     'goal': 'Data Scientist',
#     'duration': '12 weeks',
#     'style': 'project based'
# }
# generated_content = generate_content(user_preferences)
# print(generated_content)
