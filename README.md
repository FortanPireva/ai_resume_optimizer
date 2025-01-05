# AI Resume Optimizer

An AI-powered tool that helps optimize resumes for specific job descriptions, improving ATS compatibility and highlighting relevant experience.

## Features

- Resume analysis and optimization using OpenAI's GPT models
- Support for multiple file formats (PDF, DOCX, TXT)
- ATS compatibility checking
- Keyword alignment analysis
- Experience and qualification assessment
- Downloadable results in multiple formats

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

3. Upload your resume and paste the job description

4. Choose your optimization level:
   - Conservative: Minimal changes, focus on keyword alignment
   - Balanced: Moderate optimization with some rewording
   - Aggressive: Extensive optimization and restructuring

5. Review the suggestions and download the optimized resume

## Project Structure

```
resume_optimizer/
├── .env                 # Configuration
├── templates/           # Document templates
│   ├── resume.html     # HTML template
│   └── style.css       # Styling
├── src/                # Source code
│   ├── __init__.py
│   ├── ai_engine.py    # AI optimization logic
│   ├── document_processor.py # File handling
│   └── interface.py    # User interface
└── main.py            # Entry point
```

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 