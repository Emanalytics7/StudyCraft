from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from content_generation import generate_content
from reportlab.lib.enums import TA_CENTER

# Define user preferences
user_preferences = {
    'goal': 'Data Scientist',
    'duration': '12 weeks',
    'style': 'structured and comprehensive'
}

# Generate learning schedule content
generated_content = generate_content(user_preferences)

class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.doc = SimpleDocTemplate(filename, pagesize=letter)
        self.styles = getSampleStyleSheet()
        self.story = []

    def header_footer(self, canvas, doc):
        # Header
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawString(inch, 11 * inch, "Learning Schedule")
        
        # Footer
        canvas.setFont('Helvetica', 10)
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawRightString(7.5 * inch, 0.75 * inch, text)
        canvas.restoreState()

    def add_content(self, content):
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Title'],
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        heading_style = ParagraphStyle(
            'HeadingStyle',
            parent=self.styles['Heading1'],
            fontSize=14,
            textColor=colors.darkblue,
            spaceAfter=10,
            bold=True
        )
        subheading_style = ParagraphStyle(
            'SubHeadingStyle',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.black,
            spaceAfter=8
        )
        link_style = ParagraphStyle(
            'LinkStyle',
            parent=self.styles['Normal'],
            textColor=colors.blue,
            underline=True,
            spaceAfter=5
        )
        normal_style = self.styles['Normal']
        quote_style = ParagraphStyle(
            'QuoteStyle',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.grey,
            italic=True,
            spaceAfter=15,
            leftIndent=20,
            rightIndent=20
        )

        # Add the title
        self.story.append(Paragraph("Learning Schedule", title_style))
        self.story.append(Spacer(1, 0.2 * inch))

        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("#") and not line.startswith("##"):
                # Motivational quotes
                self.story.append(Paragraph(line[1:].strip(), quote_style))
                self.story.append(Spacer(1, 0.2 * inch))
            elif line.startswith("##"):
                # Start a new page for each duration and add bold headings
                if len(self.story) > 1:
                    self.story.append(PageBreak())
                self.story.append(Paragraph(line[2:].strip(), heading_style))
                self.story.append(Spacer(1, 0.2 * inch))
            elif line.startswith("### "):
                # Sub-headings
                self.story.append(Paragraph(line[3:].strip(), subheading_style))
                self.story.append(Spacer(1, 0.1 * inch))
            elif "- (" in line and ")" in line:
                # Links
                self.story.append(Paragraph(line, link_style))
                self.story.append(Spacer(1, 0.1 * inch))
            elif line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("- "):
                # Topics, Exercises, and Assessments
                self.story.append(Paragraph(line, normal_style))
                self.story.append(Spacer(1, 0.1 * inch))
            else:
                # Normal text
                self.story.append(Paragraph(line, normal_style))
                self.story.append(Spacer(1, 0.1 * inch))

    def build_pdf(self):
        self.doc.build(self.story, onFirstPage=self.header_footer, onLaterPages=self.header_footer)

# Create PDF with learning schedule
pdf_filename = 'learning_schedule.pdf'
pdf = PDFGenerator(pdf_filename)
pdf.add_content(generated_content)
pdf.build_pdf()
