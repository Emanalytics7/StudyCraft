from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import blue, black, gray
import re

# Register custom fonts
pdfmetrics.registerFont(TTFont('Regular', 'fonts/AnonymousPro-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Bold', 'fonts/AnonymousPro-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Italic', 'fonts/AnonymousPro-Italic.ttf'))

class PDFDocument:
    def __init__(self, filename, title):
        self.canvas = canvas.Canvas(filename, pagesize=letter)
        self.canvas.setTitle(title)
        self.width, self.height = letter

    def add_page_number(self, page_num):
        self.canvas.setFont('Regular', 10)
        self.canvas.drawRightString(self.width - inch, 0.5 * inch, f"Page {page_num}")
        self.canvas.line(inch, 0.6 * inch, self.width - inch, 0.6 * inch)

    def draw_text(self, text, x, y, size=12, line_height=14, indent=0):
        def get_chunks(text):
            patterns = [r'\*\*(.*?)\*\*', r'\*(.*?)\*', r'(https?://\S+)']
            cursor = 0
            for match in re.finditer('|'.join(patterns), text):
                if cursor < match.start():
                    yield text[cursor:match.start()], 'Regular', black
                if match.group().startswith('**'):
                    yield match.group()[2:-2], 'Bold', black
                elif match.group().startswith('*') and not match.group().startswith('**'):
                    yield match.group()[1:-1], black
                elif re.match(r'https?://', match.group()):
                    yield match.group(), 'Italic', blue
                cursor = match.end()
            if cursor < len(text):
                yield text[cursor:], 'Regular', black

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
                self.canvas.setFont('Bold', 18)
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
            else:
                _, y = self.draw_text(f"**{section}**", inch, y)

            y -= 0.1 * inch

        self.add_page_number(page_num)
        self.canvas.save()

