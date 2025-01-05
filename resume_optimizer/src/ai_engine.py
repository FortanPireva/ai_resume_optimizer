import os
from string import Template
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv

class PromptTemplates:
    CONTENT_TRANSFORMATION = Template('''
    Transform the following resume content to perfectly match this job description.
    
    BASE RESUME:
    $resume_text
    
    TARGET JOB DESCRIPTION:
    $job_description
    
    Create a completely tailored resume that:
    1. Matches the exact skills and qualifications mentioned in the job post
    2. Rewords experiences to highlight relevant achievements
    3. Prioritizes information based on job requirements
    4. Uses industry-specific terminology from the job description
    5. Maintains professional tone and formatting
    
    Important requirements:
    - Preserve truthful information from the original resume
    - Include all relevant experience from the original resume
    - Format in clear, ATS-friendly markdown
    - Use strong action verbs and quantifiable achievements
    - Maintain professional formatting
    
    Generate the complete resume in markdown format.
    ''')
    
    EXPERIENCE_TAILORING = Template('''
    Rewrite these experience entries to align with the target job requirements:
    
    ORIGINAL EXPERIENCE:
    $experience_entries
    
    JOB REQUIREMENTS:
    $requirements
    
    For each entry:
    1. Emphasize relevant skills and achievements
    2. Use terminology from the job description
    3. Quantify impacts where possible
    4. Start with strong action verbs
    5. Maintain factual accuracy
    
    Return the tailored experience entries in markdown format.
    ''')

class ResumeOptimizer:
    def __init__(self):
        """Initialize the optimizer with necessary configurations"""
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.templates = PromptTemplates()
        
    def get_completion(self, prompt: str, model: str = "gpt-4", temperature: float = 0.7) -> str:
        """
        Get AI completion from OpenAI.
        
        Parameters:
            prompt (str): Formatted prompt text
            model (str): GPT model to use
            temperature (float): Controls response creativity
            
        Returns:
            str: The AI-generated response
        """
        messages = [{"role": "user", "content": prompt}]
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    
    def generate_tailored_resume(self, resume_text: str, job_description: str, temperature: float = 0.4) -> str:
        """
        Generate a completely tailored resume for the target job.
        
        Parameters:
            resume_text (str): The original resume text
            job_description (str): The target job description
            temperature (float): Controls output creativity
            
        Returns:
            str: The tailored resume in markdown format
        """
        # Generate the tailored resume content
        generation_prompt = self.templates.CONTENT_TRANSFORMATION.substitute(
            resume_text=resume_text,
            job_description=job_description
        )
        
        # Get the AI to create the tailored resume
        tailored_resume = self.get_completion(
            generation_prompt,
            temperature=temperature
        )
        
        # Enhance specific sections
        sections = self.extract_sections(tailored_resume)
        enhanced_sections = self.enhance_sections(sections, job_description)
        
        # Combine into final resume
        return self.combine_sections(enhanced_sections)
    
    def extract_sections(self, resume_text: str) -> Dict[str, str]:
        """
        Extract different sections from the resume text.
        
        Parameters:
            resume_text (str): The full resume text
            
        Returns:
            Dict[str, str]: Dictionary of section names and their content
        """
        sections = {}
        current_section = "General"
        current_content = []
        
        for line in resume_text.split('\n'):
            if line.strip().startswith('#'):  # Markdown headers indicate sections
                if current_content:
                    sections[current_section.lower()] = '\n'.join(current_content)
                current_section = line.strip('#').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            sections[current_section.lower()] = '\n'.join(current_content)
            
        return sections
    
    def enhance_sections(self, sections: Dict[str, str], job_description: str) -> Dict[str, str]:
        """
        Further enhance each section of the generated resume.
        
        Parameters:
            sections (Dict[str, str]): Original sections
            job_description (str): Target job description
            
        Returns:
            Dict[str, str]: Enhanced sections
        """
        enhanced = {}
        
        for section_name, content in sections.items():
            if 'experience' in section_name.lower():
                enhanced[section_name] = self.enhance_experience(content, job_description)
            else:
                enhanced[section_name] = content
                
        return enhanced
    
    def enhance_experience(self, experience_content: str, job_description: str) -> str:
        """
        Enhance experience entries to better match job requirements.
        
        Parameters:
            experience_content (str): Original experience content
            job_description (str): Target job description
            
        Returns:
            str: Enhanced experience content
        """
        prompt = self.templates.EXPERIENCE_TAILORING.substitute(
            experience_entries=experience_content,
            requirements=job_description
        )
        
        return self.get_completion(prompt, temperature=0.3)
    
    def combine_sections(self, sections: Dict[str, str]) -> str:
        """
        Combine enhanced sections back into a complete resume.
        
        Parameters:
            sections (Dict[str, str]): Enhanced sections
            
        Returns:
            str: Complete resume in markdown format
        """
        # Define section order
        section_order = [
            'summary', 'experience', 'skills', 'education', 'certifications',
            'projects', 'publications', 'awards', 'languages', 'interests'
        ]
        
        # Combine sections in order
        resume_parts = []
        for section in section_order:
            for name, content in sections.items():
                if section in name.lower():
                    resume_parts.append(f"# {name.title()}\n\n{content.strip()}\n")
                    break
        
        # Add any remaining sections not in the predefined order
        for name, content in sections.items():
            if not any(section in name.lower() for section in section_order):
                resume_parts.append(f"# {name.title()}\n\n{content.strip()}\n")
        
        return '\n'.join(resume_parts) 