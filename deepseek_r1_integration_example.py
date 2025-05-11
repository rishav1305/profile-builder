from ollama_integration import OllamaClient
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DeepseekProfileGenerator:
    """
    A class that uses the deepseek-r1 model via OllamaClient to generate content
    for professional profiles on remote work platforms.
    """
    
    def __init__(self):
        """Initialize the DeepseekProfileGenerator with the deepseek-r1 model."""
        self.client = OllamaClient(model="deepseek-r1")
        logging.info("DeepseekProfileGenerator initialized with deepseek-r1 model")
    
    def generate_title(self, portfolio_data):
        """Generate a professional title based on portfolio data."""
        prompt = f"""
        Based on the following portfolio information, create a compelling professional title 
        for a remote work platform profile (no more than 10 words):
        
        Skills: {', '.join(portfolio_data.get('skills', []))}
        Experience: {portfolio_data.get('experience', 'Not specified')}
        Domain expertise: {portfolio_data.get('domain_expertise', 'Not specified')}
        
        Title:
        """
        
        logging.info("Generating professional title")
        title = self.client.generate(prompt, max_tokens=50, temperature=0.7)
        return title.strip()
    
    def generate_overview(self, portfolio_data, max_words=250):
        """Generate a professional overview based on portfolio data."""
        prompt = f"""
        Create a professional overview for a remote work platform profile based on the following information.
        The overview should be engaging, highlight key strengths, and be no more than {max_words} words.
        
        Name: {portfolio_data.get('name', 'Not specified')}
        Skills: {', '.join(portfolio_data.get('skills', []))}
        Experience: {portfolio_data.get('experience', 'Not specified')}
        Domain expertise: {portfolio_data.get('domain_expertise', 'Not specified')}
        Previous projects: {portfolio_data.get('projects', 'Not specified')}
        Education: {portfolio_data.get('education', 'Not specified')}
        
        Professional Overview:
        """
        
        logging.info("Generating professional overview")
        overview = self.client.generate(prompt, max_tokens=1000, temperature=0.7)
        return overview.strip()
    
    def generate_project_description(self, project_info, max_words=150):
        """Generate a project description based on project information."""
        prompt = f"""
        Create a compelling project description for a remote work platform profile based on the following project information.
        The description should highlight achievements, technologies used, and be no more than {max_words} words.
        
        Project name: {project_info.get('name', 'Not specified')}
        Project duration: {project_info.get('duration', 'Not specified')}
        Technologies used: {', '.join(project_info.get('technologies', []))}
        Your role: {project_info.get('role', 'Not specified')}
        Key achievements: {project_info.get('achievements', 'Not specified')}
        
        Project Description:
        """
        
        logging.info(f"Generating description for project: {project_info.get('name', 'Unnamed project')}")
        description = self.client.generate(prompt, max_tokens=500, temperature=0.7)
        return description.strip()
    
    def suggest_skill_prioritization(self, skills, target_platform):
        """Suggest how to prioritize skills for a specific platform."""
        prompt = f"""
        I have the following skills:
        {', '.join(skills)}
        
        I'm creating a profile on {target_platform}. How should I prioritize these skills for maximum impact? 
        Return your response as a JSON with two lists: "primary_skills" and "secondary_skills".
        """
        
        logging.info(f"Generating skill prioritization for {target_platform}")
        response = self.client.generate(prompt, max_tokens=500, temperature=0.7)
        
        # Try to extract JSON from the response
        try:
            # Find JSON in the response (it might be surrounded by other text)
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # If no JSON format was found, parse it manually
                skills_dict = {"primary_skills": [], "secondary_skills": []}
                if "primary_skills" in response.lower():
                    # Simple parsing logic - could be improved
                    parts = response.split("secondary_skills")
                    primary_part = parts[0].lower().split("primary_skills")[-1]
                    primary_skills = [s.strip() for s in primary_part.replace(':', '').replace('-', '').split(',') if s.strip()]
                    skills_dict["primary_skills"] = primary_skills
                    
                    if len(parts) > 1:
                        secondary_skills = [s.strip() for s in parts[1].replace(':', '').replace('-', '').split(',') if s.strip()]
                        skills_dict["secondary_skills"] = secondary_skills
                
                return skills_dict
        except Exception as e:
            logging.error(f"Error parsing skill prioritization response: {str(e)}")
            return {"primary_skills": skills[:len(skills)//2], "secondary_skills": skills[len(skills)//2:]}


def sample_usage():
    """Sample usage of the DeepseekProfileGenerator class."""
    
    # Sample portfolio data
    portfolio_data = {
        "name": "Alex Johnson",
        "skills": ["Python", "Data Analysis", "Machine Learning", "SQL", "Data Visualization", "Django", "Flask", "AWS"],
        "experience": "7 years of experience in data science and web development",
        "domain_expertise": "Healthcare, Finance, E-commerce",
        "projects": "Built an ML pipeline for medical image analysis; Developed a recommendation system for an e-commerce platform",
        "education": "MS in Computer Science, Stanford University"
    }
    
    # Sample project info
    project_info = {
        "name": "Healthcare Predictive Analytics Platform",
        "duration": "8 months",
        "technologies": ["Python", "TensorFlow", "AWS", "Docker", "MongoDB"],
        "role": "Lead Data Scientist",
        "achievements": "Reduced patient readmission rates by 15% through predictive modeling; Implemented real-time monitoring system for patient health indicators"
    }
    
    # Create an instance of DeepseekProfileGenerator
    generator = DeepseekProfileGenerator()
    
    # Generate content
    print("\n=== Generated Professional Title ===")
    title = generator.generate_title(portfolio_data)
    print(title)
    
    print("\n=== Generated Professional Overview ===")
    overview = generator.generate_overview(portfolio_data)
    print(overview)
    
    print("\n=== Generated Project Description ===")
    description = generator.generate_project_description(project_info)
    print(description)
    
    print("\n=== Suggested Skill Prioritization for Upwork ===")
    skills_priority = generator.suggest_skill_prioritization(portfolio_data["skills"], "Upwork")
    print(f"Primary Skills: {', '.join(skills_priority.get('primary_skills', []))}")
    print(f"Secondary Skills: {', '.join(skills_priority.get('secondary_skills', []))}")


if __name__ == "__main__":
    print("\n=== Testing DeepseekProfileGenerator with deepseek-r1 model ===\n")
    sample_usage()
    print("\n=== Test completed ===\n")
