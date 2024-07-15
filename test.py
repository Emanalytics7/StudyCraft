from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import blue, black
import re

class PDFDocument:
    def __init__(self, filename, title):
        self.canvas = canvas.Canvas(filename, pagesize=letter)
        self.canvas.setTitle(title)
        self.width, self.height = letter

    def add_page_number(self, page_num):
        self.canvas.setFont('Helvetica', 10)
        self.canvas.drawRightString(self.width - inch, 0.5 * inch, f"Page {page_num}")
        self.canvas.line(inch, 0.6 * inch, self.width - inch, 0.6 * inch)

    def draw_text(self, text, x, y, size=12, line_height=14, indent=0):
        def get_chunks(text):
            patterns = [r'\*\*(.*?)\*\*', r'\*(.*?)\*', r'(https?://\S+)']
            cursor = 0
            for match in re.finditer('|'.join(patterns), text):
                if cursor < match.start():
                    yield text[cursor:match.start()], 'Helvetica', black
                if match.group().startswith('**'):
                    yield match.group()[2:-2], 'Helvetica-Bold', black
                elif match.group().startswith('*') and not match.group().startswith('**'):
                    yield match.group()[1:-1], 'Helvetica-Oblique', black
                elif re.match(r'https?://\S+', match.group()):
                    yield match.group(), 'Helvetica', blue
                cursor = match.end()
            if cursor < len(text):
                yield text[cursor:], 'Helvetica', black

        cursor_x = x + indent
        cursor_y = y
        line_width = self.width - 2 * inch - indent
        for chunk, style, color in get_chunks(text):
            self.canvas.setFont(style, size)
            self.canvas.setFillColor(color)
            
            words = chunk.split()
            for word in words:
                word_width = self.canvas.stringWidth(word, self.canvas._fontname, size)
                if cursor_x + word_width > x + line_width:
                    if word_width > line_width:
                        while word:
                            for i in range(len(word), 0, -1):
                                part = word[:i]
                                part_width = self.canvas.stringWidth(part, self.canvas._fontname, size)
                                if part_width <= line_width:
                                    if cursor_x + part_width > x + line_width:
                                        cursor_y -= line_height
                                        cursor_x = x + indent
                                    self.canvas.drawString(cursor_x, cursor_y, part)
                                    cursor_x += part_width
                                    word = word[i:]
                                    break
                            if cursor_x > x + line_width:
                                cursor_y -= line_height
                                cursor_x = x + indent
                    else:
                        cursor_y -= line_height
                        cursor_x = x + indent
                self.canvas.drawString(cursor_x, cursor_y, word)
                cursor_x += word_width + self.canvas.stringWidth(' ', self.canvas._fontname, size)
            
            self.canvas.setFillColor(black)

        return x, cursor_y - line_height

    def create_pdf(self, content):
        page_num = 1
        y = self.height - 1.5 * inch
        sections = content.split("\n")
        bullet = u"\u2022"
        list_counter = 1

        for section in sections:
            if section.startswith("### ") and y < self.height - 2 * inch:
                self.add_page_number(page_num)
                self.canvas.showPage()
                page_num += 1
                y = self.height - inch

            if y < 2 * inch:
                self.add_page_number(page_num)
                self.canvas.showPage()
                page_num += 1
                y = self.height - inch

            if section.startswith("### "):
                y -= 0.5 * inch
                self.canvas.setFont('Helvetica-Bold', 18)
                self.canvas.drawString(inch, y, section[4:].strip())
                y -= 0.3 * inch
                self.canvas.line(inch, y, self.width - inch, y)
                y -= 0.4 * inch
            elif section.startswith("**"):
                y -= 0.3 * inch
                _, y = self.draw_text(section, inch, y, 14)
            elif section.startswith("* "):
                section = f"**{list_counter}.** {section[2:]}"
                list_counter += 1
                _, y = self.draw_text(section, inch, y, 12, 14, 10)
            elif section.startswith("  + ") or section.startswith("  - "):
                section = f"{bullet} {section[4:]}"
                _, y = self.draw_text(section, inch, y, 12, 14, 20)
            elif section.startswith("> "):
                _, y = self.draw_text(section, inch, y, 12, 14, 10)
            else:
                _, y = self.draw_text(f"**{section}**", inch, y)

            y -= 0.1 * inch

        self.add_page_number(page_num)
        self.canvas.save()

# Usage
filename = 'study.pdf'
title = 'Studycraft'
content = """
Enter your preferred learning style (e.g., Interactive, Theoretical): mix
**Learning Schedule for: data science**

**Duration**: 1 month
**Learning Style**: mix

"The best way to get started is to quit talking and begin doing." - Walt Disney

**Month 1:**

* Week 1:
  + Main topics to cover: Introduction to Data Science, Python basics, and data preprocessing
  + Practical exercises: Setup Python environment, practice basic Python scripts, and perform simple data preprocessing tasks

* Week 2:
  + Main topics to cover: Data visualization, statistical inference, and machine learning fundamentals
  + Practical exercises: Use popular data visualization libraries like Matplotlib and Seaborn, practice statistical inference, and implement basic machine learning models

* Week 3:
  + Main topics to cover: Data manipulation and analysis, regression, and decision trees
  + Practical exercises: Practice data manipulation using Pandas, implement regression models, and build decision trees

* Week 4:
  + Main topics to cover: Clustering, dimensionality reduction, and model evaluation
  + Practical exercises: Implement k-means clustering, practice dimensionality reduction techniques, and evaluate machine learning models

* Monthly Project:
  - Description: Build a simple machine learning model to predict a continuous target variable
  - Skills applied: Data preprocessing, feature engineering, and model evaluation
  - Estimated time: 10 hours

* Monthly milestone: Complete the implementation of a basic machine learning model
* Self-assessment task: Evaluate and improve the model's performance

**Key Milestones**:
1. Complete the setup of the Python environment and perform basic data preprocessing tasks (Week 1)
2. Implement and evaluate a basic machine learning model (Week 4)
3. Complete the monthly project and submit it for review (Week 4)

**Advanced Topics (for latter part of the learning period):
* Topic 1: Deep Learning
  + Subtopics: Neural networks, convolutional neural networks, and recurrent neural networks
  + Resources: Online courses, research papers, and blogs
* Topic 2: Big Data Analytics
  + Subtopics: Hadoop, Spark, and NoSQL databases
  + Resources: Online courses, research papers, and blogs
https://example.com
**Community and Support**:
* Recommended forums or communities: Kaggle, Reddit (r/learnpython and r/MachineLearning), and Data Science subreddit
* Potential mentorship opportunities: Reach out to professionals on LinkedIn or attend data science meetups
* Study group suggestions: Join online study groups or create a local study group with fellow learners

**Assessment and Evaluation**:
* Suggested methods for tracking progress: Set specific goals, track time spent on tasks, and maintain a learning journal
* Key performance indicators: Completion of practical exercises, implementation of machine learning models, and improvement in model performance
* Final project or exam details: Submit a comprehensive project that demonstrates the application of data science concepts

**Additional Tips**:
* Time management strategies for a 1 month-month learning period: Allocate 2-3 hours per day, set specific goals, and prioritize tasks
* Recommended pace and intensity based on the 1 month-month duration: Focus on building a strong foundation, then gradually increase the pace
* Strategies for maintaining motivation: Celebrate small wins, share progress with others, and reward yourself for milestones achieved

**Additional Resources**:
https://www.datacamp.com/
https://www.kaggle.com/
https://python.org/
https://scikit-learn.org/
https://matplotlib.org/
https://seaborn.pydata.org/
PDF created successfully: studycraft.pdf
"""

pdf = PDFDocument(filename, title)
pdf.create_pdf(content)

filename = 'studycraft.pdf'
title = 'Studycraft'
