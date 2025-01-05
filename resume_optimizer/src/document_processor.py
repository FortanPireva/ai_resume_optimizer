import os
from typing import Dict, BinaryIO
from docx import Document
from pdfminer.high_level import extract_text
from markdown2 import markdown
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

class DocumentProcessor:
    def __init__(self, templates_dir: str = "templates"):
        """
        Initialize document processor with necessary templates.
        
        Parameters:
            templates_dir (str): Directory containing HTML templates
        """
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        
    def extract_from_pdf(self, file_obj: BinaryIO) -> str:
        """
        Extract text content from a PDF file.
        
        Parameters:
            file_obj (BinaryIO): PDF file object
            
        Returns:
            str: Extracted text content
        """
        return extract_text(file_obj)
    
    def extract_from_docx(self, file_obj: BinaryIO) -> str:
        """
        Extract text content from a Word document.
        
        Parameters:
            file_obj (BinaryIO): Word document file object
            
        Returns:
            str: Extracted text content
        """
        doc = Document(file_obj)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    
    def extract_from_text(self, file_obj: BinaryIO) -> str:
        """
        Extract content from a text file.
        
        Parameters:
            file_obj (BinaryIO): Text file object
            
        Returns:
            str: File content
        """
        return file_obj.read().decode('utf-8')
    
    def process_upload(self, file_obj: BinaryIO) -> str:
        """
        Process uploaded resume files.
        
        Parameters:
            file_obj (BinaryIO): Uploaded file object
            
        Returns:
            str: Extracted text content
        """
        filename = file_obj.name.lower()
        
        if filename.endswith('.pdf'):
            return self.extract_from_pdf(file_obj)
        elif filename.endswith(('.docx', '.doc')):
            return self.extract_from_docx(file_obj)
        elif filename.endswith('.txt'):
            return self.extract_from_text(file_obj)
        else:
            raise ValueError(f"Unsupported file format: {filename.split('.')[-1]}")
    
    def markdown_to_html(self, content: str) -> str:
        """
        Convert markdown content to HTML.
        
        Parameters:
            content (str): Markdown formatted content
            
        Returns:
            str: HTML content
        """
        return markdown(content)
    
    def html_to_pdf(self, html_content: str, css_file: str = None) -> bytes:
        """
        Convert HTML content to PDF.
        
        Parameters:
            html_content (str): HTML content to convert
            css_file (str, optional): Path to CSS file for styling
            
        Returns:
            bytes: PDF content
        """
        # Load template and render HTML
        template = self.env.get_template('resume.html')
        rendered_html = template.render(content=html_content)
        
        # Convert to PDF
        html = HTML(string=rendered_html)
        if css_file and os.path.exists(css_file):
            return html.write_pdf(stylesheets=[css_file])
        return html.write_pdf()
    
    def convert_to_formats(self, content: str, css_file: str = None) -> Dict[str, str]:
        """
        Convert optimized content to various formats.
        
        Parameters:
            content (str): Original content in markdown format
            css_file (str, optional): Path to CSS file for styling
            
        Returns:
            Dict[str, str]: Dictionary containing different format versions
        """
        html_content = self.markdown_to_html(content)
        pdf_content = self.html_to_pdf(html_content, css_file)
        
        return {
            'markdown': content,
            'html': html_content,
            'pdf': pdf_content
        } 