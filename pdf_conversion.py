from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import blue, grey, black
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import re
from content_generation import main

class CustomDocTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        SimpleDocTemplate.__init__(self, *args, **kwargs)

    def afterPage(self):
        self.canv.saveState()
        self.canv.setFont('Helvetica', 9)
        self.canv.setStrokeColor(grey)
        self.canv.setLineWidth(0.5)
        self.canv.line(inch, 0.75 * inch, 7.5 * inch, 0.75 * inch)
        self.canv.drawString(4 * inch, 0.5 * inch, f"Page {self.canv.getPageNumber()}")
        self.canv.restoreState()

def format_text(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)
    text = re.sub(r'(https?://\S+)', r'<link href="\1"><font color="blue"><u>\1</u></font></link>', text)
    return text

def parse_content(content):
    if content is None:
        raise ValueError("Content is None. Please ensure the 'main' function returns valid content.")
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=18,
        alignment=1,
        spaceAfter=24
    )
    heading_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=14,
        alignment=1,
        spaceBefore=24,
        spaceAfter=12
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=1,
        spaceBefore=6,
        spaceAfter=6
    )
    quote_style = ParagraphStyle(
        'Quote',
        parent=styles['BodyText'],
        fontSize=10,
        alignment=1,
        spaceBefore=24,
        spaceAfter=24,
        italic=True
    )

    story = []
    weekly_plan = []
    current_week = None

    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        formatted_line = format_text(line)
        
        if line.startswith("Learning Schedule for:"):
            story.append(Paragraph(formatted_line, title_style))
        elif line.lower().startswith(("duration", "learning style")):
            story.append(Paragraph(formatted_line, normal_style))
        elif line == "Weekly Plan**:":
            story.append(Paragraph("Weekly Plan", heading_style))
        elif line.startswith("Week"):
            if current_week:
                weekly_plan.append(current_week)
            current_week = [Paragraph(f"<b>{formatted_line}</b>", normal_style)]
        elif line.startswith("Day"):
            if current_week:
                current_week.append(Paragraph(formatted_line, normal_style))
        elif line == "Resource Links":
            if current_week:
                weekly_plan.append(current_week)
            story.append(Paragraph("Weekly Plan", heading_style))
            table = Table(weekly_plan, colWidths=[2*inch, 4*inch])
            table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('GRID', (0,0), (-1,-1), 0.5, grey),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            story.append(table)
            story.append(Spacer(1, 24))
            story.append(Paragraph("Resource Links", heading_style))
        elif line.startswith("http"):
            story.append(Paragraph(formatted_line, normal_style))
        elif line.startswith('"') and line.endswith('"'):
            story.append(Paragraph(formatted_line, quote_style))
        else:
            story.append(Paragraph(formatted_line, normal_style))

    return story

def create_pdf(file_path, content):
    doc = CustomDocTemplate(file_path, pagesize=letter,
                            leftMargin=inch, rightMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    story = parse_content(content)
    doc.build(story)

# Use this function in your main script
if __name__ == "__main__":
    content = main()
    create_pdf("weekly_plan.pdf", content)