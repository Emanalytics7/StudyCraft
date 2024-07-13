import os
from groq import Groq
from exa_py import Exa
from datetime import datetime, timedelta

# Initialize API clients
exa = Exa(os.environ.get('EXA_API_KEY'))
groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def generate_content(prompt, model='llama3-70b-8192'):
    """Generate content using the LLM."""
    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model        
    )
    return response.choices[0].message.content

def get_user_inputs():
    """Gather user inputs for learning goal, duration, and style."""
    goal = input("Enter your learning goal: ").strip()
    duration = input("Enter the duration to achieve the goal (e.g., 3 months): ").strip()
    style = input("Enter your preferred learning style (e.g., Interactive, Theoretical): ").strip()
    return goal, duration, style

def create_learning_schedule(goal, duration, style):
    """Create a detailed learning schedule based on user inputs."""    
    prompt = f"""
**Learning Schedule for: {goal}**

**Duration**: {duration}
**Learning Style**: {style}


**Comprehensive Learning Plan** :

[Generate a detailed plan divided into {duration} equal parts, each representing a month. For each month, provide the following structure:]

Month [1-{duration}]:
* Week 1:
  + Main topics to cover:
  + Recommended resources:
  + Practical exercises:
* Week 2:
  + Main topics to cover:
  + Recommended resources:
  + Practical exercises:
* Week 3:
  + Main topics to cover:
  + Recommended resources:
  + Practical exercises:
* Week 4:
  + Main topics to cover:
  + Recommended resources:
  + Practical exercises:
* Monthly Project:
  - Description:
  - Skills applied:
  - Estimated time:
* Monthly milestone:
* Self-assessment task:

[Repeat the above structure for each month in the {duration}-month period]

**Key Milestones** :
[List 3-5 major milestones spread across the {duration}-month period]

**Advanced Topics** (for latter part of the learning period):
* Topic 1:
  + Subtopics:
  + Resources:
* Topic 2:
  + Subtopics:
  + Resources:

**Resource Links** :
* [Resource Name 1]: [URL]
  - Description of resource and how it relates to the learning plan
* [Resource Name 2]: [URL]
  - Description of resource and how it relates to the learning plan
* [Resource Name 3]: [URL]
  - Description of resource and how it relates to the learning plan

**Community and Support** :
* Recommended forums or communities:
* Potential mentorship opportunities:
* Study group suggestions:

**Assessment and Evaluation** :
* Suggested methods for tracking progress:
* Key performance indicators:
* Final project or exam details:

**Additional Tips** :
* Time management strategies for a {duration}-month learning period:
* Recommended pace and intensity based on the {duration}-month duration:
* Strategies for maintaining motivation over {duration} months:


[Insert a relevant, motivational quote here that relates to learning or the specific goal, considering the {duration}-month journey]

"""
    schedule = generate_content(prompt)
    return schedule

def display_learning_schedule(schedule):
    """Display the generated learning schedule."""
    print(schedule)


def main():
    """Main function to orchestrate the learning schedule generation."""
    goal, duration, style = get_user_inputs()
        
    schedule = create_learning_schedule(goal, duration, style)
    
    display_learning_schedule(schedule)
    return schedule

if __name__ == "__main__":
    main()
