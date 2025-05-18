import logging
import json
from ollama_integration import OllamaClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DeepseekProfileGenerator:
    """
    Class for generating optimized professional profile content using the deepseek model.
    This class utilizes the Ollama API client to generate content specifically tailored
    for various professional platforms.
    """
    
    def __init__(self, model="deepseek-r1"):
        """Initialize the DeepseekProfileGenerator with the specified model."""
        self.ollama_client = OllamaClient(model=model)
    
    def generate_title(self, portfolio_data, platform="generic"):
        """
        Generate an optimized professional title based on portfolio data.
        
        Args:
            portfolio_data (dict): Portfolio information
            platform (str): Target platform (upwork, linkedin, etc.)
            
        Returns:
            str: Generated professional title
        """
        # Extract relevant information
        current_title = portfolio_data.get('basic_info', {}).get('title', '')
        experiences = portfolio_data.get('experience', [])
        skills = portfolio_data.get('skills', {})
        
        # Create a prompt specific to the platform
        if platform.lower() == "upwork":
            prompt = f"""
            You are an expert in optimizing Upwork freelancer profiles. 
            Create a compelling professional title (maximum 70 characters) based on the following information:
            
            Current title: {current_title}
            Experience: {json.dumps(experiences[:2], indent=2)}
            Skills: {json.dumps(skills, indent=2)}
            
            The title should:
            1. Include key skills that clients search for
            2. Communicate expertise level (Senior, Expert, etc.)
            3. Be specific about the value offered
            4. Include relevant technologies/tools
            
            Format as a single line without quotes.
            """
        elif platform.lower() == "linkedin":
            prompt = f"""
            You are an expert in LinkedIn profile optimization.
            Create a compelling LinkedIn headline (maximum 220 characters) based on the following information:
            
            Current title: {current_title}
            Experience: {json.dumps(experiences[:2], indent=2)}
            Skills: {json.dumps(skills, indent=2)}
            
            The headline should:
            1. Start with your current role or expertise
            2. Include industry specialization
            3. Mention key skills or technologies
            4. Add value proposition (optional)
            
            Format as a single line without quotes.
            """
        else:
            prompt = f"""
            Create a compelling professional title (maximum 100 characters) based on:
            
            Current title: {current_title}
            Experience: {json.dumps(experiences[:2], indent=2)}
            Skills: {json.dumps(skills, indent=2)}
            
            Format as a single line without quotes.
            """
        
        # Generate title using Ollama
        response = self.ollama_client.generate(prompt)
        
        # Clean up response
        title = response.strip().replace('"', '').split('\n')[0]
        
        # Enforce character limits based on platform
        if platform.lower() == "upwork" and len(title) > 70:
            title = title[:67] + "..."
        elif platform.lower() == "linkedin" and len(title) > 220:
            title = title[:217] + "..."
        elif len(title) > 100:
            title = title[:97] + "..."
        
        return title

    def generate_overview(self, portfolio_data, platform="generic"):
        """
        Generate an optimized professional overview/summary based on portfolio data.
        
        Args:
            portfolio_data (dict): Portfolio information
            platform (str): Target platform (upwork, linkedin, etc.)
            
        Returns:
            str: Generated professional overview
        """
        # Extract relevant information
        about = portfolio_data.get('about', {})
        experiences = portfolio_data.get('experience', [])
        education = portfolio_data.get('education', [])
        skills = portfolio_data.get('skills', {})
        
        # Create a prompt specific to the platform
        if platform.lower() == "upwork":
            prompt = f"""
            You are an expert in Upwork profile optimization.
            Create a compelling overview section (600-1000 characters) for an Upwork profile based on:
            
            About: {json.dumps(about, indent=2)}
            Experience: {json.dumps(experiences, indent=2)}
            Education: {json.dumps(education, indent=2)}
            Skills: {json.dumps(skills, indent=2)}
            
            The overview should:
            1. Start with an attention-grabbing first sentence
            2. Highlight expertise and specializations
            3. Mention years of experience in key areas
            4. Include technologies and methodologies
            5. Explain the unique value proposition
            6. End with a call-to-action
            
            Write in first person and focus on client benefits.
            """
        elif platform.lower() == "linkedin":
            prompt = f"""
            You are an expert in LinkedIn profile optimization.
            Create a compelling summary/about section (2000-2600 characters) for a LinkedIn profile based on:
            
            About: {json.dumps(about, indent=2)}
            Experience: {json.dumps(experiences, indent=2)}
            Education: {json.dumps(education, indent=2)}
            Skills: {json.dumps(skills, indent=2)}
            
            The summary should:
            1. Start with a strong opening paragraph about professional identity
            2. Include a brief story that demonstrates expertise and passion
            3. Highlight 3-5 key achievements with measurable results
            4. Mention important technologies and methodologies
            5. Include industry-relevant keywords for better visibility
            6. End with information about current interests or goals
            7. Include a call to action for connecting
            
            Write in first person and make it personable yet professional.
            """
        else:
            prompt = f"""
            Create a professional summary (800-1200 characters) based on:
            
            About: {json.dumps(about, indent=2)}
            Experience: {json.dumps(experiences[:2], indent=2)}
            Skills: {json.dumps(skills, indent=2)}
            
            Write in first person and focus on demonstrating expertise.
            """
        
        # Generate overview using Ollama
        return self.ollama_client.generate(prompt).strip()
    
    def select_skills(self, portfolio_data, platform="generic", max_skills=50):
        """
        Select and optimize skills list based on portfolio data.
        
        Args:
            portfolio_data (dict): Portfolio information
            platform (str): Target platform (upwork, linkedin, etc.)
            max_skills (int): Maximum number of skills to return
            
        Returns:
            list: Optimized list of skills
        """
        # Extract skills from portfolio data
        technical_skills = portfolio_data.get('skills', {}).get('technical', [])
        soft_skills = portfolio_data.get('skills', {}).get('soft', [])
        experiences = portfolio_data.get('experience', [])
        
        # Combine all skills
        all_skills = technical_skills + soft_skills
        
        if not all_skills:
            # Return default skills if none are provided
            return ["Python", "Data Engineering", "SQL", "ETL", "Cloud Services"]
        
        # Create a prompt specific to the platform
        if platform.lower() == "upwork":
            prompt = f"""
            You are an Upwork profile optimization expert.
            From the following skills and experience, select the most marketable skills for an Upwork profile (maximum {max_skills}).
            Focus on specific technical skills and technologies that clients search for, rather than general abilities.
            
            Skills: {json.dumps(all_skills, indent=2)}
            Experience: {json.dumps(experiences, indent=2)}
            
            For each selected skill, make sure it's specific, marketable, and demonstrable.
            Order skills by relevance and searchability.
            Return ONLY the list of skills, with each skill on a new line (no bullets or numbers).
            """
        elif platform.lower() == "linkedin":
            prompt = f"""
            You are a LinkedIn profile optimization expert. 
            From the following skills and experience, select the most impactful skills for a LinkedIn profile (maximum {max_skills}).
            Include both technical skills and relevant soft skills for a well-rounded profile.
            
            Skills: {json.dumps(all_skills, indent=2)}
            Experience: {json.dumps(experiences, indent=2)}
            
            Consider both the LinkedIn Skills Graph and skills commonly used for recruiters' searches.
            Balance specific technical skills with broader skill categories.
            Return ONLY the list of skills, with each skill on a new line (no bullets or numbers).
            """
        else:
            prompt = f"""
            From the following skills and experience, select the most relevant skills (maximum {max_skills}):
            
            Skills: {json.dumps(all_skills, indent=2)}
            Experience: {json.dumps(experiences, indent=2)}
            
            Return ONLY the list of skills, with each skill on a new line (no bullets or numbers).
            """
        
        # Generate skills list using Ollama
        response = self.ollama_client.generate(prompt)
        
        # Parse response into a clean list of skills
        skills = []
        for line in response.strip().split('\n'):
            # Clean the line of any bullets, numbers, or extra characters
            skill = line.strip()
            skill = skill.lstrip('*-0123456789. \t')
            skill = skill.strip('"\'')
            
            if skill and skill not in skills and len(skills) < max_skills:
                skills.append(skill)
        
        return skills
    
    def suggest_hourly_rate(self, portfolio_data, platform="upwork"):
        """
        Suggest an appropriate hourly rate based on portfolio data.
        
        Args:
            portfolio_data (dict): Portfolio information
            platform (str): Target platform (upwork, linkedin, etc.)
            
        Returns:
            int: Suggested hourly rate in USD
        """
        # Only relevant for platforms like Upwork
        if platform.lower() != "upwork":
            return None
        
        # Extract relevant information
        experiences = portfolio_data.get('experience', [])
        
        # Calculate total experience years (simplified)
        total_years = 0
        for exp in experiences:
            duration = exp.get('duration', '')
            # Roughly estimate years from the duration string
            if 'Present' in duration:
                years = 2  # Rough estimate for current position
            else:
                years = 1  # Default for past positions
            
            total_years += years
        
        # Simple heuristic for hourly rate based on experience
        # This is a very simplified approach
        if total_years < 3:
            base_rate = 25
        elif total_years < 5:
            base_rate = 40
        elif total_years < 8:
            base_rate = 55
        else:
            base_rate = 70
        
        # Generate a more nuanced suggestion using the model
        prompt = f"""
        You are an expert in Upwork freelancer pricing strategies.
        Based on the following professional details, suggest an appropriate hourly rate (USD):
        
        Years of experience: {total_years}
        Recent positions: {json.dumps([exp.get('title', '') for exp in experiences[:2]], indent=2)}
        
        Consider:
        1. The calculated base rate: ${base_rate}/hr
        2. Market rates for similar professionals
        3. Value-based pricing principles
        
        Return ONLY a single integer number (no $ symbol, text, or explanation).
        """
        
        try:
            rate_response = self.ollama_client.generate(prompt).strip()
            
            # Extract just the number
            import re
            rate_match = re.search(r'(\d+)', rate_response)
            if rate_match:
                suggested_rate = int(rate_match.group(1))
                
                # Apply reasonable bounds
                if suggested_rate < 15:
                    suggested_rate = 15
                elif suggested_rate > 150:
                    suggested_rate = 150
                    
                return suggested_rate
            else:
                return base_rate
                
        except Exception as e:
            logging.warning(f"Error generating hourly rate: {str(e)}")
            return base_rate
            
    def analyze_current_profile(self, current_profile_data, portfolio_data, platform="linkedin"):
        """
        Analyze current profile data against portfolio data and provide improvement suggestions.
        
        Args:
            current_profile_data (dict): Current profile information from the platform
            portfolio_data (dict): Portfolio information
            platform (str): Target platform (linkedin, etc.)
            
        Returns:
            dict: Improvement suggestions and content
        """
        if platform.lower() == "linkedin":
            prompt = f"""
            You are an expert LinkedIn profile optimizer.
            Compare the current LinkedIn profile with the portfolio data and suggest improvements:
            
            Current LinkedIn Profile:
            {json.dumps(current_profile_data, indent=2)}
            
            Portfolio Data:
            {json.dumps(portfolio_data, indent=2)}
            
            Analyze the following aspects:
            1. Headline - is it keyword-rich and impactful?
            2. About section - does it tell a compelling story?
            3. Experience - are achievements quantified and relevant?
            4. Skills - are the most relevant skills listed?
            
            For each suggested change, provide the exact text that should be used.
            Format your response as a JSON with these keys:
            {{
                "headline": "suggested headline text",
                "about": "suggested about text",
                "experiences": [{{
                    "title": "position title",
                    "company": "company name",
                    "description": "detailed description with achievements"
                }}],
                "skills_to_add": ["skill1", "skill2"]
            }}
            """
            
            try:
                response = self.ollama_client.generate(prompt)
                
                # Extract JSON from response
                import re
                json_match = re.search(r'({.*})', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    suggestions = json.loads(json_str)
                    return suggestions
                else:
                    # Create a basic structure if JSON extraction fails
                    return {
                        "headline": self.generate_title(portfolio_data, platform="linkedin"),
                        "about": self.generate_overview(portfolio_data, platform="linkedin"),
                        "experiences": [],
                        "skills_to_add": self.select_skills(portfolio_data, platform="linkedin", max_skills=10)
                    }
                    
            except Exception as e:
                logging.error(f"Error analyzing profile: {str(e)}")
                # Return basic suggestions on failure
                return {
                    "headline": self.generate_title(portfolio_data, platform="linkedin"),
                    "about": self.generate_overview(portfolio_data, platform="linkedin"),
                    "experiences": [],
                    "skills_to_add": self.select_skills(portfolio_data, platform="linkedin", max_skills=10)
                }
        else:
            return {
                "error": f"Profile analysis not supported for platform: {platform}"
            }