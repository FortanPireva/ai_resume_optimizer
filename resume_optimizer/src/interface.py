import gradio as gr
from typing import Tuple, BinaryIO
import os
import tempfile
from .ai_engine import ResumeOptimizer
from .document_processor import DocumentProcessor

def create_interface(optimizer: ResumeOptimizer, processor: DocumentProcessor) -> gr.Interface:
    """
    Create the main Gradio interface.
    
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
        Core optimization function that processes user inputs.
        
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
            "Balanced": 0.7,
            "Aggressive": 0.9
        }.get(optimization_level, 0.7)
        
        # Get AI optimization with adjusted temperature
        optimized_content = optimizer.analyze_resume(
            resume_text,
            job_description,
            temperature=temperature
        )
        
        # Convert to different formats
        outputs = processor.convert_to_formats(
            optimized_content,
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
                label="Upload Your Resume",
                file_types=[".pdf", ".docx", ".txt"]
            ),
            gr.Textbox(
                label="Job Description",
                placeholder="Paste the job description here...",
                lines=5
            ),
            gr.Radio(
                choices=["Conservative", "Balanced", "Aggressive"],
                label="Optimization Level",
                value="Balanced"
            )
        ],
        outputs=[
            gr.Markdown(label="Optimization Suggestions"),
            gr.HTML(label="Resume Preview"),
            gr.File(label="Download Optimized Resume")
        ],
        title="AI Resume Optimizer",
        description="""
        Upload your resume and paste a job description to get AI-powered optimization suggestions.
        The tool will analyze keyword alignment, experience relevance, and provide ATS-friendly improvements.
        """,
        theme="default",
        allow_flagging="never"
    )
    
    return interface 