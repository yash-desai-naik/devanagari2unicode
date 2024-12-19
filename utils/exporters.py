import docx
from weasyprint import HTML, CSS
from pathlib import Path
import tempfile

def save_as_txt(text, filename):
    """Save text as UTF-8 encoded txt file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)
    return filename

def save_as_docx(text, filename):
    """Save text as docx file."""
    doc = docx.Document()
    doc.add_paragraph(text)
    doc.save(filename)
    return filename

def save_as_pdf(text, filename):
    """Save text as PDF file using WeasyPrint."""
    # Create HTML content with proper styling
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-family: Arial Unicode MS, Noto Sans Devanagari, sans-serif;
                    font-size: 12pt;
                    line-height: 1.5;
                }}
                p {{
                    margin: 0;
                    padding: 0;
                    text-align: justify;
                }}
            </style>
        </head>
        <body>
            <div>{text.replace('\n', '<br>')}</div>
        </body>
    </html>
    """
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', mode='w', encoding='utf-8', delete=False) as temp:
        temp.write(html_content)
        temp_path = temp.name
    
    try:
        # Convert HTML to PDF
        HTML(filename=temp_path).write_pdf(filename)
        return filename
    finally:
        # Clean up temporary file
        Path(temp_path).unlink()

def save_as_html(text, filename):
    """Save text as HTML file."""
    html_content = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Converted Devanagari Text</title>
            <style>
                body {{
                    font-family: Arial Unicode MS, Noto Sans Devanagari, sans-serif;
                    margin: 2em;
                    line-height: 1.5;
                }}
            </style>
        </head>
        <body>
            <div>
                {text.replace('\n', '<br>')}
            </div>
        </body>
    </html>
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return filename