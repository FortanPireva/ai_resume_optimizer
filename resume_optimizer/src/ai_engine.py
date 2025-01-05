import os
from string import Template
from typing import Dict, List
from openai import OpenAI
from dotenv import load_dotenv

class PromptTemplates:
    RESUME_ANALYSIS = Template('''
    Analyze the following resume and job description. Provide optimization suggestions:
    
    RESUME:
    $resume_text
    
    JOB DESCRIPTION:
    $job_description
    
    Please provide a detailed analysis covering:
    1. Keyword Alignment Analysis
       - Identify matching keywords
       - Highlight missing important terms
       - Suggest synonym alternatives
       
    2. Experience and Qualifications
       - Assess experience relevance
       - Identify gaps in qualifications
       - Suggest ways to better highlight relevant experience
       
    3. Content and Structure
       - Evaluate section organization
       - Assess bullet point effectiveness
       - Recommend structural improvements
       
    4. ATS Optimization
       - Check formatting compatibility
       - Verify keyword placement
       - Assess overall ATS friendliness
    
    Format the response in markdown with clear sections and examples.
    ''')

    BULLET_POINT_OPTIMIZER = Template('''
    Optimize the following bullet points for impact and clarity:
    
    ORIGINAL BULLETS:
    $bullet_points
    
    JOB REQUIREMENTS:
    $requirements
    
    For each bullet point:
    1. Start with strong action verbs
    2. Include quantifiable achievements
    3. Incorporate relevant keywords
    4. Maintain ATS-friendly formatting
    
    Return the optimized bullet points in markdown format.
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
    
    def analyze_resume(self, resume_text: str, job_description: str, temperature: float = 0.7) -> str:
        """
        Perform complete resume analysis and optimization.
        
        Parameters:
            resume_text (str): The text content of the resume
            job_description (str): The job description text
            temperature (float): Controls response creativity
            
        Returns:
            str: Detailed analysis and optimization suggestions
        """
        analysis_prompt = self.templates.RESUME_ANALYSIS.substitute(
            resume_text=resume_text,
            job_description=job_description
        )
        
        return self.get_completion(analysis_prompt, temperature=temperature)
    
    def optimize_bullet_points(self, bullet_points: List[str], requirements: str) -> str:
        """
        Optimize resume bullet points for better impact.
        
        Parameters:
            bullet_points (List[str]): List of original bullet points
            requirements (str): Job requirements text
            
        Returns:
            str: Optimized bullet points
        """
        bullet_points_text = "\n".join(bullet_points)
        optimization_prompt = self.templates.BULLET_POINT_OPTIMIZER.substitute(
            bullet_points=bullet_points_text,
            requirements=requirements
        )
        
        return self.get_completion(optimization_prompt)
    
    def extract_sections(self, resume_text: str) -> Dict[str, str]:
        """
        Extract different sections from the resume text.
        
        Parameters:
            resume_text (str): The full resume text
            
        Returns:
            Dict[str, str]: Dictionary of section names and their content
        """
        # This is a simplified implementation
        # In a real application, you'd want more sophisticated section detection
        sections = {}
        current_section = "General"
        current_content = []
        
        for line in resume_text.split('\n'):
            if line.strip().isupper() and len(line.strip()) > 0:
                # Assume uppercase lines are section headers
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
            
        return sections 