# filepath: /Users/rishavchatterjee/Desktop/Projects/profile-builder/deepseek_integration.py
"""
This module integrates the deepseek-r1 model with the profile-builder project.
It provides a specialized generator for professional profile content.
"""

import logging
import json
import re
from ollama_integration import OllamaClient

class DeepseekProfileGenerator:
    """
    A class that uses the deepseek-r1 model via OllamaClient to generate content
    for professional profiles on remote work platforms.
    """
    
    def __init__(self):
        """Initialize the DeepseekProfileGenerator with the deepseek-r1 model."""
        self.client = OllamaClient(model="deepseek-r1")
        logging.info("DeepseekProfileGenerator initialized with deepseek-r1 model")
    
    def _process_response(self, response):
        """Clean up model response by removing thinking prompts and unnecessary text."""
        # Remove <think> blocks
        if "<think>" in response:
            # Find the last </think> tag and take everything after it
            parts = response.split("</think>")
            if len(parts) > 1:
                response = parts[-1].strip()
            else:
                # If there's no closing tag, remove everything from <think> onward
                response = response.split("<think>")[0].strip()
        
        return response.strip()
    
    def generate_title(self, portfolio_data, platform="general"):
        """Generate a professional title based on portfolio data."""
        # Create platform-specific prompt
        if platform.lower() == "upwork":
            prompt = f"""
            You are an expert in crafting effective Upwork profiles. 
            Based on the following professional information, create a concise and impactful professional title 
            (maximum 70 characters) that would attract clients on Upwork:
            
            Current title: {portfolio_data.get('basic_info', {}).get('title', '')}
            Experience: 
            {json.dumps(portfolio_data.get('experience', []), indent=2)}
            Skills: 
            {json.dumps(portfolio_data.get('skills', {}), indent=2)}
            
            The title should highlight expertise and specialization without buzzwords.
            DO NOT include any thinking or reasoning in your response.
            Return ONLY the title, nothing else.
            """
        elif platform.lower() == "linkedin":
            prompt = f"""
            You are an expert in crafting effective LinkedIn profiles. 
            Based on the following professional information, create a concise and impactful professional headline 
            (maximum 220 characters) that would stand out on LinkedIn:
            
            Current title: {portfolio_data.get('basic_info', {}).get('title', '')}
            Experience: 
            {json.dumps(portfolio_data.get('experience', []), indent=2)}
            Skills: 
            {json.dumps(portfolio_data.get('skills', {}), indent=2)}
            
            The headline should be specific about your expertise and value proposition.
            DO NOT include any thinking or reasoning in your response.
            Return ONLY the headline, nothing else.
            """
        else:
            # Generic professional title for other platforms
            prompt = f"""
            Based on the following professional information, create a concise and impactful professional title 
            (maximum 100 characters):
            
            Current title: {portfolio_data.get('basic_info', {}).get('title', '')}
            Experience: 
            {json.dumps(portfolio_data.get('experience', []), indent=2)}
            Skills: 
            {json.dumps(portfolio_data.get('skills', {}), indent=2)}
            
            The title should highlight expertise and specialization.
            DO NOT include any thinking or reasoning in your response.
            Return ONLY the title, nothing else.
            """
        
        logging.info(f"Generating professional title for {platform}")
        title = self.client.generate(prompt, max_tokens=50, temperature=0.7)
        
        # Clean up the response to get just the title
        title = self._process_response(title)
        title = title.strip().replace('"', '').split('\n')[0]
        
        # Apply platform-specific length constraints
        if platform.lower() == "upwork" and len(title) > 70:
            title = title[:67] + "..."
        elif platform.lower() == "linkedin" and len(title) > 220:
            title = title[:217] + "..."
            
        return title
    
    def generate_overview(self, portfolio_data, platform="general"):
        """Generate a professional overview based on portfolio data."""
        # Create platform-specific prompt
        if platform.lower() == "upwork":
            prompt = f"""
            You are an expert in crafting effective Upwork profiles. 
            Based on the following professional information, create a compelling overview 
            (between 500-1000 characters) for an Upwork profile:
            
            About: 
            {json.dumps(portfolio_data.get('about', {}), indent=2)}
            Experience: 
            {json.dumps(portfolio_data.get('experience', []), indent=2)}
            Education: 
            {json.dumps(portfolio_data.get('education', []), indent=2)}
            Skills: 
            {json.dumps(portfolio_data.get('skills', {}), indent=2)}
            
            The overview should:
            1. Start with a strong opening statement about value proposition
            2. Highlight key achievements with quantifiable results
            3. Emphasize expertise and specialized skills
            4. Include a clear call-to-action at the end
            5. Be written in first person
            
            DO NOT include any thinking or reasoning in your response.
            """
        elif platform.lower() == "linkedin":
            prompt = f"""
            You are an expert in crafting effective LinkedIn profiles. 
            Based on the following professional information, create a compelling About section 
            (between 1500-2000 characters) for a LinkedIn profile:
            
            About: 
            {json.dumps(portfolio_data.get('about', {}), indent=2)}
            Experience: 
            {json.dumps(portfolio_data.get('experience', []), indent=2)}
            Education: 
            {json.dumps(portfolio_data.get('education', []), indent=2)}
            Skills: 
            {json.dumps(portfolio_data.get('skills', {}), indent=2)}
            
            The About section should:
            1. Tell a compelling professional story
            2. Highlight key achievements with quantifiable results
            3. Show your personality and passion
            4. Include relevant keywords for discoverability
            5. Be written in first person
            
            DO NOT include any thinking or reasoning in your response.
            """
        else:
            # Generic overview for other platforms
            prompt = f"""
            Based on the following professional information, create a compelling professional overview 
            (between 800-1200 characters):
            
            About: 
            {json.dumps(portfolio_data.get('about', {}), indent=2)}
            Experience: 
            {json.dumps(portfolio_data.get('experience', []), indent=2)}
            Education: 
            {json.dumps(portfolio_data.get('education', []), indent=2)}
            Skills: 
            {json.dumps(portfolio_data.get('skills', {}), indent=2)}
            
            The overview should:
            1. Start with a strong opening statement about expertise
            2. Highlight key achievements with quantifiable results
            3. Emphasize specialized skills and experience
            4. Be written in first person
            
            DO NOT include any thinking or reasoning in your response.
            """
        
        logging.info(f"Generating professional overview for {platform}")
        overview = self.client.generate(prompt, max_tokens=1000, temperature=0.7)
        
        return self._process_response(overview).strip()
    
    def select_skills(self, portfolio_data, platform="general", max_skills=10):
        """Select the most relevant skills based on portfolio data."""
        all_skills = portfolio_data.get('skills', {}).get('technical', [])
        if not all_skills:
            all_skills = portfolio_data.get('skills', [])
        
        # Create platform-specific prompt
        if platform.lower() == "upwork":
            prompt = f"""
            You are an expert in optimizing Upwork profiles.
            From the following list of skills, select the {max_skills} most marketable skills for an Upwork profile 
            based on current market demand. Return ONLY the list of skills, one per line with a dash prefix:
            
            {json.dumps(all_skills)}
            
            DO NOT include any thinking or reasoning in your response.
            """
        elif platform.lower() == "linkedin":
            prompt = f"""
            You are an expert in optimizing LinkedIn profiles.
            From the following list of skills, select the {max_skills} most impactful skills for a LinkedIn profile 
            that will attract recruiters and improve discoverability. Return ONLY the list of skills, 
            one per line with a dash prefix:
            
            {json.dumps(all_skills)}
            
            DO NOT include any thinking or reasoning in your response.
            """
        else:
            # Generic skill selection for other platforms
            prompt = f"""
            From the following list of skills, select the {max_skills} most important skills 
            that best represent professional expertise. Return ONLY the list of skills, 
            one per line with a dash prefix:
            
            {json.dumps(all_skills)}
            
            DO NOT include any thinking or reasoning in your response.
            """
        
        logging.info(f"Selecting skills for {platform}")
        response = self.client.generate(prompt, max_tokens=300, temperature=0.7)
        
        # Process and clean up the response
        processed_response = self._process_response(response)
        
        # Parse the response to get a clean list of skills
        skills = []
        for line in processed_response.strip().split('\n'):
            skill = line.strip().replace('-', '').replace('*', '').strip()
            if skill and len(skills) < max_skills:
                skills.append(skill)
        
        return skills
    
    def suggest_hourly_rate(self, portfolio_data, platform="upwork"):
        """Suggest an appropriate hourly rate based on experience level."""
        # Calculate experience years (simple approximation)
        experience = portfolio_data.get('experience', [])
        experience_years = len(experience) * 2  # Simple approximation
        
        skills = portfolio_data.get('skills', {}).get('technical', [])
        if not skills:
            skills = portfolio_data.get('skills', [])
            
        prompt = f"""
        You are an expert in {platform} pricing strategies.
        Based on {experience_years} years of experience with the following skills:
        {json.dumps(skills)}
        
        Suggest an appropriate hourly rate (USD) for {platform} that is competitive but values expertise.
        Consider that the professional has worked with enterprise clients and has demonstrated significant ROI.
        Return ONLY the hourly rate as a number (no $ symbol), nothing else.
        
        DO NOT include any thinking or reasoning in your response.
        """
        
        logging.info(f"Suggesting hourly rate for {platform}")
        response = self.client.generate(prompt, max_tokens=20, temperature=0.7)
        
        # Process and clean up the response
        processed_response = self._process_response(response)
        
        # Parse the rate from the response
        try:
            # Clean up and extract just the number
            clean_response = processed_response.strip().replace('$', '').replace('USD', '')
            # Find the first sequence of digits (possibly with decimal point)
            match = re.search(r'\d+(\.\d+)?', clean_response)
            if match:
                rate = float(match.group(0))
                return round(rate, 2)
            else:
                return 65.00  # Default if no number found
        except Exception as e:
            logging.error(f"Error parsing hourly rate: {str(e)}")
            # Default rate if parsing fails
            return 65.00
    
    def generate_project_description(self, project_info, max_words=150):
        """Generate a project description based on project information."""
        prompt = f"""
        Create a compelling project description for a professional profile based on the following project information.
        The description should highlight achievements, technologies used, and be no more than {max_words} words.
        
        Project name: {project_info.get('name', 'Not specified')}
        Project duration: {project_info.get('duration', 'Not specified')}
        Technologies used: {', '.join(project_info.get('technologies', []))}
        Your role: {project_info.get('role', 'Not specified')}
        Key achievements: {project_info.get('achievements', 'Not specified')}
        
        Project Description:
        
        DO NOT include any thinking or reasoning in your response.
        """
        
        logging.info(f"Generating description for project: {project_info.get('name', 'Unnamed project')}")
        description = self.client.generate(prompt, max_tokens=500, temperature=0.7)
        return self._process_response(description).strip()
