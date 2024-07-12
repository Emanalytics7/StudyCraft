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
Dont add here is your etc. 
**Learning Schedule for: {goal}**

**Duration**: {duration}
**Learning Style**: {style}

---
**{duration}Monthly/Weekly/Daily/Yearly Plan**:

* Create a detailed learning plan with daily or weekly tasks.
* Include recommended study materials, and activities.
* Set clear milestones and objectives for each week.

** Resource Links**
Share some relevant resource links for e.g https://example.com

General motivational quote here 
---
    """
    schedule = generate_content(prompt)
    return schedule

# def display_learning_schedule(schedule):
#     """Display the generated learning schedule."""
#     print("\nGenerated Learning Schedule:")
#     print(schedule)


def main():
    """Main function to orchestrate the learning schedule generation."""
    goal, duration, style = get_user_inputs()
        
    schedule = create_learning_schedule(goal, duration, style)
    
    # display_learning_schedule(schedule)
    return schedule

# if __name__ == "__main__":
#     main()
