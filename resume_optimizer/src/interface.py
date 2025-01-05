import gradio as gr
from typing import Tuple, BinaryIO
import os
import tempfile
from .ai_engine import ResumeOptimizer
from .document_processor import DocumentProcessor

def create_interface(optimizer: ResumeOptimizer, processor: DocumentProcessor) -> gr.Interface:
    """
    Create the main interface for resume generation.
    
    Parameters:
        optimizer (ResumeOptimizer): Instance of the resume optimizer
        processor (DocumentProcessor): Instance of the document processor
        
    Returns:
        gr.Interface: Gradio interface object
    """
    def optimize_resume(
        resume_file: BinaryIO,
        job_description: str,
        optimization_level: str
    ) -> Tuple[str, str, str]:
        """
        Generate a tailored resume from the uploaded base resume.
        
        Parameters:
            resume_file (BinaryIO): Uploaded resume file
            job_description (str): Job description text
            optimization_level (str): Level of optimization to apply
            
        Returns:
            Tuple[str, str, str]: Markdown preview, HTML view, and path to PDF file
        """
        # Process the uploaded resume
        resume_text = processor.process_upload(resume_file)
        
        # Adjust temperature based on optimization level
        temperature = {
            "Conservative": 0.3,
            "Balanced": 0.4,
            "Aggressive": 0.5
        }.get(optimization_level, 0.4)
        
        # Generate tailored resume
        tailored_content = optimizer.generate_tailored_resume(
            resume_text,
            job_description,
            temperature=temperature
        )
        
        # Convert to different formats
        outputs = processor.convert_to_formats(
            tailored_content,
            css_file="templates/style.css"
        )
        
        # Save PDF to a temporary file
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, "optimized_resume.pdf")
        with open(pdf_path, "wb") as f:
            f.write(outputs['pdf'])
        
        return (
            outputs['markdown'],  # For preview
            outputs['html'],      # For web view
            pdf_path             # Path to PDF file
        )

    # Create the interface layout
    interface = gr.Interface(
        fn=optimize_resume,
        inputs=[
            gr.File(
                label="Upload Your Base Resume",
                file_types=[".pdf", ".docx", ".txt"]
            ),
            gr.Textbox(
                label="Job Description",
                placeholder="Paste the complete job description here...",
                lines=8
            ),
            gr.Radio(
                choices=["Conservative", "Balanced", "Aggressive"],
                label="Optimization Level",
                value="Balanced",
                info="Conservative: Minimal changes, Balanced: Moderate optimization, Aggressive: Extensive rewriting"
            )
        ],
        outputs=[
            gr.Markdown(label="Preview Your Tailored Resume"),
            gr.HTML(label="Web Version"),
            gr.File(label="Download Resume")
        ],
        title="AI Resume Tailoring System",
        description="""
        Upload your base resume and paste a job description to get a professionally tailored resume.
        The system will:
        - Match skills and qualifications to the job requirements
        - Rewrite experiences to highlight relevant achievements
        - Optimize formatting for ATS compatibility
        - Maintain truthful information while enhancing impact
        """,
        theme="default",
        allow_flagging="never"
    )
    
    return interface 