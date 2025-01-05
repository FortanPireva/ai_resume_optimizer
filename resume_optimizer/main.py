import os
from src.ai_engine import ResumeOptimizer
from src.document_processor import DocumentProcessor
from src.interface import create_interface

def main():
    """
    Launch the complete Resume Optimizer application.
    
    This function:
    1. Initializes all components
    2. Creates the web interface
    3. Starts the server
    """
    # Ensure the templates directory exists
    os.makedirs("templates", exist_ok=True)
    
    # Initialize components
    optimizer = ResumeOptimizer()
    processor = DocumentProcessor()
    
    # Create and launch interface
    interface = create_interface(optimizer, processor)
    interface.launch(
        share=True,
        server_name="0.0.0.0",
        server_port=7860
    )

if __name__ == "__main__":
    main() 