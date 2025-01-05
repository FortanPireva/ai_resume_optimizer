# AI Resume Tailoring System

An AI-powered tool that automatically generates tailored resumes for specific job descriptions, optimizing your resume for both ATS systems and human readers.

## Features

- Complete resume transformation based on job descriptions
- Smart content adaptation while maintaining truthfulness
- Multiple optimization levels (Conservative, Balanced, Aggressive)
- Support for multiple file formats (PDF, DOCX, TXT)
- Professional output in multiple formats (Markdown, HTML, PDF)
- ATS-friendly formatting
- Industry-specific terminology matching
- Quantifiable achievement enhancement

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-resume-optimizer.git
cd ai-resume-optimizer
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
cd resume_optimizer
python main.py
```

2. Open your web browser and navigate to `http://localhost:7860`

3. Use the interface to:
   - Upload your base resume (PDF, DOCX, or TXT format)
   - Paste the complete job description
   - Choose your optimization level:
     - Conservative: Minimal changes, focuses on keyword alignment
     - Balanced: Moderate optimization with some rewording
     - Aggressive: More extensive rewriting while maintaining truthfulness

4. Get your tailored resume in multiple formats:
   - Preview the changes in markdown format
   - View the formatted HTML version
   - Download the professional PDF version

## How It Works

The system uses advanced AI to:
1. Analyze your base resume and the target job description
2. Transform your resume content to match job requirements
3. Enhance experience descriptions with relevant achievements
4. Optimize keyword placement for ATS compatibility
5. Maintain professional formatting and truthful information

## Project Structure

```
resume_optimizer/
├── .env                 # Configuration
├── templates/           # Document templates
│   └── resume.html     # HTML template for PDF generation
├── src/                # Source code
│   ├── __init__.py
│   ├── ai_engine.py    # AI transformation logic
│   ├── document_processor.py # File handling
│   └── interface.py    # User interface
└── main.py            # Entry point
```

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt

## Best Practices

When using the system:
1. Always review the generated content for accuracy
2. Verify that all information remains truthful
3. Double-check important dates and numbers
4. Test different optimization levels for best results
5. Keep your base resume up-to-date

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 