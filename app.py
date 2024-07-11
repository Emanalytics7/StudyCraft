import streamlit as st
import json

from content_generation import generate_learning_path, integrate_resources


user_name = st.text_input("Enter your name (optional):")
goal = st.text_area("Describe your learning goal/objective:")
schedule_type = st.radio("Select schedule type:", ("Weekly", "Daily"))
start_date = st.date_input("Select start date:")
num_weeks_or_days = st.number_input("Number of weeks/days:", min_value=1)

if st.button("Generate Learning Schedule"):
    user_preferences = {
        "user_name": user_name,
        "goal": goal,
        "schedule_type": schedule_type,
        "start_date": start_date,
        "num_weeks_or_days": num_weeks_or_days
    }
    
    learning_path = generate_learning_path(goal)
    learning_path = integrate_resources(learning_path)

    # Format the content
    content = {
        "cover_page": {
            "title": "Personalized Learning Schedule",
            "user_name": user_preferences.get("user_name", "Anonymous")
        },
        "table_of_contents": [
            "Introduction",
            "Weekly Schedule",
            "Resources",
            "Progress Tracking",
            "Conclusion"
        ],
        "introduction": {
            "goal": user_preferences["goal"]
        },
        "schedule": learning_path['schedule'],
        "resources": [resource for week in learning_path['schedule'] for topic in week['topics'] for resource in topic['resources']],
        "progress_tracking": "Use this section to track your progress.",
        "conclusion": "Congratulations on completing your learning schedule! Keep learning and growing."
    }

    # Save the content as JSON for now (later we can convert it to PDF)
    with open("learning_schedule.json", "w") as f:
        json.dump(content, f, indent=4)

    st.write("Learning schedule generated successfully! Check the learning_schedule.json file.")