from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from content_generation import main

class ProfessionalPDFCreator:
    def __init__(self, content, output_filename, title):
        self.content = content
        self.output_filename = output_filename
        self.title = title
        self.doc = SimpleDocTemplate(output_filename, pagesize=letter,
                                     rightMargin=72, leftMargin=72,
                                     topMargin=72, bottomMargin=72)
        self.styles = getSampleStyleSheet()
        self.add_custom_styles()

    def add_custom_styles(self):
        self.styles['Normal'].alignment = TA_JUSTIFY
        self.styles['Title'].fontSize = 24
        self.styles['Title'].fontName = 'Helvetica-Bold'
        self.styles['Title'].spaceAfter = 12
        self.styles['Title'].alignment = TA_CENTER

        styles_to_add = {
            'Heading1': {'fontSize': 18, 'fontName': 'Helvetica-Bold', 'spaceAfter': 6},
            'Heading2': {'fontSize': 16, 'fontName': 'Helvetica-Bold', 'spaceAfter': 6},
            'Heading3': {'fontSize': 14, 'fontName': 'Helvetica-Bold', 'spaceAfter': 6},
            'BulletPoint': {'fontSize': 12, 'fontName': 'Helvetica', 'leftIndent': 20, 'spaceAfter': 3},
            'Justify': {'alignment': TA_JUSTIFY, 'fontSize': 12, 'fontName': 'Helvetica'}
            }

        for style_name, style_attributes in styles_to_add.items():
            try:
                self.styles.add(ParagraphStyle(name=style_name, **style_attributes))
            except KeyError:
                for attr, value in style_attributes.items():
                    setattr(self.styles[style_name], attr, value)

    def create_pdf(self):
        story = []
        sections = self.content.split('\n\n')
        for section in sections:
            lines = section.split('\n')
            if lines[0].startswith('**'):
                # Section title
                story.append(Paragraph(lines[0].strip('*'), self.styles['Heading1']))
                story.append(Spacer(1, 12))
                self.process_subsection(story, lines[1:])
            else:
                self.process_subsection(story, lines)
            
            story.append(Spacer(1, 12))

        self.doc.build(story, onFirstPage=self.add_page_number, onLaterPages=self.add_page_number)

    def process_subsection(self, story, lines):
        current_list = []
        in_list = False

        for line in lines:
            line = line.strip()
            if not line:
                if in_list:
                    story.append(self.create_table(current_list))
                    current_list = []
                    in_list = False
                story.append(Spacer(1, 6))
            elif line.startswith('**') and line.endswith('**:'):
                if in_list:
                    story.append(self.create_table(current_list))
                    current_list = []
                    in_list = False
                story.append(Paragraph(line.strip('*'), self.styles['Heading2']))
            elif line.startswith('*') or line.startswith('+') or line.startswith('-'):
                in_list = True
                current_list.append(line)
            else:
                if in_list:
                    story.append(self.create_table(current_list))
                    current_list = []
                    in_list = False
                story.append(Paragraph(line, self.styles['Justify']))

        if current_list:
            story.append(self.create_table(current_list))

    def create_table(self, lines):
        data = []
        for line in lines:
            if line.startswith('* '):
                data.append([Paragraph('•', self.styles['BulletPoint']), Paragraph(line[2:], self.styles['Normal'])])
            elif line.startswith('+') or line.startswith('-'):
                data.append(['', Paragraph('○ ' + line[4:], self.styles['BulletPoint'])])
        
        table = Table(data, colWidths=[0.2*inch, 5.3*inch])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        return table

    def add_page_number(self, canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawString(letter[0]-72, 0.75 * inch, text)
        canvas.restoreState()

        # Add header
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(72, letter[1] - 36, self.title)
        canvas.restoreState()

        # Add footer
        canvas.saveState()
        canvas.setFont('Helvetica', 9)
        canvas.drawString(72, 0.75 * inch, "Learning Plan")
        canvas.restoreState()

# Your content here (the result of the LLM output based on your template)
content = main()

pdf_creator = ProfessionalPDFCreator(content, 'learning_plan.pdf', "Data Science Learning Plan")
pdf_creator.create_pdf()