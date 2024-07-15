import os
from groq import Groq
from exa_py import Exa

# Initialize API clients
exa = Exa(os.environ.get('EXA_API_KEY'))
groq_client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def fetch_response(topic):
    response = exa.search(topic, num_results=1)
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
Dont write Heres is...

**Learning Schedule for**: {goal}
**Duration**: {duration} months
**Learning Style**: {style}

    [Insert a relevant, motivational quote here that relates to learning or the specific goal, considering the {duration}-month journey]


[Generate a detailed plan divided into {duration} equal parts, each representing a month. For each month, provide the following structure:]

Month [1-{duration}]:

* Week 1:

  + Main topics to cover:
  + Practical exercises:

* Week 2:

  + Main topics to cover:
  + Practical exercises:

* Monthly Project:

  - Description:
  - Skills applied:
  - Estimated time:

* Monthly milestone:

* Self-assessment task:

[Repeat the above structure for each week in the {duration}-month period]

**Key Milestones**:

[List 3-5 major milestones spread across the {duration}-month period]

**Advanced Topics (for latter part of the learning period):

* Topic 1:
  + Subtopics:
  + Resources:
* Topic 2:
  + Subtopics:
  + Resources:

**Community and Support**:

* Recommended forums or communities:
* Potential mentorship opportunities:
* Study group suggestions:

**Assessment and Evaluation**:

* Suggested methods for tracking progress:
* Key performance indicators:
* Final project or exam details:

**Additional Tips**:

* Time management strategies for a {duration}-month learning period:
* Recommended pace and intensity based on the {duration}-month duration:
* Strategies for maintaining motivation over {duration} months:

"""
    schedule = generate_content(prompt)
    return schedule

def extract_topics(schedule):
    """Extract main topics from the generated learning schedule."""
    topics = []
    for line in schedule.split('\n'):
        if "Main topics to cover" in line or "Topic" in line:
            topic = line.split(":")[-1].strip()
            if topic:  
                topics.append(topic)
    return topics

def resources(schedule, topics):
    """Fetch relevant resources for the extracted topics."""
    all_resources = []
    for topic in topics:
        fetched_resources = fetch_response(f" Give some latest resources related to {topic}")
        if fetched_resources:
            for resource in fetched_resources:
                all_resources.append(f"* {resource['url']}")
    
    # Flatten the list of resources and join them to the schedule
    motivation = 'Be brave enough to find the life you want and courageous enough to chase it. Then start over and love yourself the way you were always meant to!'
    schedule = f"{schedule}\n\n**Additional Resources**\n\n" + "\n".join(all_resources) + "\n\n" + motivation
    return schedule

def display_learning_schedule(schedule):
    """Display the generated learning schedule."""
    print(schedule)

def main():
    """Main function to orchestrate the learning schedule generation."""
    goal, duration, style = get_user_inputs()
    
    schedule = create_learning_schedule(goal, duration, style)
    
    topics = extract_topics(schedule)
    schedule = resources(schedule, topics)

    display_learning_schedule(schedule)
    return schedule

if __name__ == "__main__":
    main()
