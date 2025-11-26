from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from pathlib import Path

def md_to_pdf(md_path: Path, pdf_path: Path):
    text = md_path.read_text(encoding='utf-8')
    styles = getSampleStyleSheet()
    # ensure headings exist and adjust spacing safely
    if 'Heading1' in styles:
        h1 = styles['Heading1']
        h1.spaceAfter = 6
    else:
        styles.add(ParagraphStyle(name='Heading1', parent=styles['Normal'], spaceAfter=6))
    if 'Heading2' in styles:
        h2 = styles['Heading2']
        h2.spaceAfter = 4
    else:
        styles.add(ParagraphStyle(name='Heading2', parent=styles['Normal'], spaceAfter=4))
    if 'Code' not in styles:
        styles.add(ParagraphStyle(name='Code', parent=styles['Normal'], fontName='Courier', fontSize=8, leading=10))

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    story = []

    for line in text.splitlines():
        if line.startswith('# '):
            story.append(Paragraph(line[2:].strip(), styles['Heading1']))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:].strip(), styles['Heading2']))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:].strip(), styles['Heading3']))
        elif line.strip() == '':
            story.append(Spacer(1, 6))
        elif line.startswith('```'):
            # simple code block handling: skip fence lines
            continue
        else:
            # inline preserve backticks and code blocks as normal text
            story.append(Paragraph(line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), styles['BodyText']))

    doc.build(story)

if __name__ == '__main__':
    base = Path(__file__).resolve().parents[1]
    md = base / 'TESTS.md'
    pdf = base / 'TESTS.pdf'
    md_to_pdf(md, pdf)
    print(f'Generated {pdf}')
