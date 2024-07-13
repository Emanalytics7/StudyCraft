from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def create_learning_schedule_pdf(filename, goal, duration, style):
    # Create a document template
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Get the default stylesheet
    styles = getSampleStyleSheet()
    
    # Define custom styles
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    bold_style = ParagraphStyle(name='Bold', parent=styles['BodyText'], fontName='Helvetica-Bold')
    normal_style = styles['BodyText']
    
    # Create content
    elements = []

    # Title
    elements.append(Paragraph(f"Learning Schedule for: {goal}", title_style))
    elements.append(Spacer(1, 12))

    # Subtitles
    elements.append(Paragraph(f"Duration: {duration} months", bold_style))
    elements.append(Paragraph(f"Learning Style: {style}", bold_style))
    elements.append(Spacer(1, 12))

    # Comprehensive Learning Plan
    elements.append(Paragraph("Comprehensive Learning Plan:", subtitle_style))
    
    for month in range(1, duration + 1):
        elements.append(Paragraph(f"Month {month}:", bold_style))
        for week in range(1, 5):
            week_items = [
                ListItem(Paragraph("Main topics to cover:", normal_style)),
                ListItem(Paragraph("Recommended resources:", normal_style)),
                ListItem(Paragraph("Practical exercises:", normal_style))
            ]
            elements.append(ListFlowable(week_items, bulletType='bullet', start='*', leftIndent=20))
        
        monthly_project_items = [
            ListItem(Paragraph("Description:", normal_style)),
            ListItem(Paragraph("Skills applied:", normal_style)),
            ListItem(Paragraph("Estimated time:", normal_style))
        ]
        elements.append(Paragraph("Monthly Project:", bold_style))
        elements.append(ListFlowable(monthly_project_items, bulletType='bullet', start='-', leftIndent=20))
        
        elements.append(Paragraph("Monthly milestone:", normal_style))
        elements.append(Paragraph("Self-assessment task:", normal_style))
        elements.append(Spacer(1, 12))

    # Key Milestones
    elements.append(Paragraph("Key Milestones:", subtitle_style))
    milestone_items = [
        ListItem(Paragraph(f"Milestone 1:", normal_style)),
        ListItem(Paragraph(f"Milestone 2:", normal_style)),
        ListItem(Paragraph(f"Milestone 3:", normal_style))
    ]
    elements.append(ListFlowable(milestone_items, bulletType='bullet', start='*', leftIndent=20))
    elements.append(Spacer(1, 12))

    # Advanced Topics
    elements.append(Paragraph("Advanced Topics:", subtitle_style))
    for topic in ["Topic 1", "Topic 2"]:
        elements.append(Paragraph(topic, bold_style))
        advanced_topic_items = [
            ListItem(Paragraph("Subtopics:", normal_style)),
            ListItem(Paragraph("Resources:", normal_style))
        ]
        elements.append(ListFlowable(advanced_topic_items, bulletType='bullet', start='+', leftIndent=20))
    elements.append(Spacer(1, 12))

    # Resource Links
    elements.append(Paragraph("Resource Links:", subtitle_style))
    for i in range(1, 4):
        elements.append(Paragraph(f"[Resource Name {i}]: [URL]", bold_style))
        elements.append(Paragraph("Description of resource and how it relates to the learning plan", normal_style))
    elements.append(Spacer(1, 12))

    # Community and Support
    elements.append(Paragraph("Community and Support:", subtitle_style))
    community_items = [
        ListItem(Paragraph("Recommended forums or communities:", normal_style)),
        ListItem(Paragraph("Potential mentorship opportunities:", normal_style)),
        ListItem(Paragraph("Study group suggestions:", normal_style))
    ]
    elements.append(ListFlowable(community_items, bulletType='bullet', start='-', leftIndent=20))
    elements.append(Spacer(1, 12))

    # Assessment and Evaluation
    elements.append(Paragraph("Assessment and Evaluation:", subtitle_style))
    assessment_items = [
        ListItem(Paragraph("Suggested methods for tracking progress:", normal_style)),
        ListItem(Paragraph("Key performance indicators:", normal_style)),
        ListItem(Paragraph("Final project or exam details:", normal_style))
    ]
    elements.append(ListFlowable(assessment_items, bulletType='bullet', start='*', leftIndent=20))
    elements.append(Spacer(1, 12))

    # Additional Tips
    elements.append(Paragraph("Additional Tips:", subtitle_style))
    tips_items = [
        ListItem(Paragraph(f"Time management strategies for a {duration}-month learning period:", normal_style)),
        ListItem(Paragraph(f"Recommended pace and intensity based on the {duration}-month duration:", normal_style)),
        ListItem(Paragraph(f"Strategies for maintaining motivation over {duration} months:", normal_style))
    ]
    elements.append(ListFlowable(tips_items, bulletType='bullet', start='*', leftIndent=20))
    elements.append(Spacer(1, 12))

    # Motivational Quote
    elements.append(Paragraph("[Insert a relevant, motivational quote here that relates to learning or the specific goal, considering the {duration}-month journey]", normal_style))
    
    # Build the PDF
    doc.build(elements)

# Example usage
create_learning_schedule_pdf("learning_schedule.pdf", "Python Programming", 6, "Self-paced")
