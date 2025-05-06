import logging
import json
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from ollama_integration import OllamaClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProfileBuilder:
    """
    Class to build professional profiles on remote work platforms
    using portfolio data and Ollama for intelligent content generation.
    """
    
    def __init__(self, platform, portfolio_data, credentials=None):
        self.platform = platform.lower()
        self.portfolio_data = portfolio_data
        self.credentials = credentials or {}
        self.ollama_client = OllamaClient()
        
        # Map platform names to their respective builder methods
        self.platform_map = {
            'upwork': self._build_upwork_profile
        }
    
    def build(self):
        """Build profile on the selected platform."""
        if self.platform not in self.platform_map:
            raise ValueError(f"Platform '{self.platform}' is not supported")
        
        # Call the appropriate builder method for the platform
        return self.platform_map[self.platform]()
    
    def _build_upwork_profile(self):
        """Build a profile on Upwork."""
        logging.info("Building Upwork profile")
        
        # Use Ollama to generate optimized content for Upwork
        title = self._generate_title_for_upwork()
        overview = self._generate_overview_for_upwork()
        skills = self._select_skills_for_upwork()
        hourly_rate = self._suggest_hourly_rate()
        
        # For POC, we'll just return the generated content
        # In a real implementation, this would use Playwright to fill out forms
        result = {
            'title': title,
            'overview': overview,
            'skills': skills,
            'hourly_rate': hourly_rate,
            'status': 'content_generated'
        }
        
        # If credentials are provided, attempt to fill out the profile
        if self.credentials.get('username') and self.credentials.get('password'):
            try:
                self._fill_upwork_profile(result)
                result['status'] = 'profile_updated'
            except Exception as e:
                logging.error(f"Error filling Upwork profile: {str(e)}")
                result['error'] = str(e)
        
        return result
    
    def _generate_title_for_upwork(self):
        """Generate a professional title optimized for Upwork."""
        prompt = f"""
        You are an expert in crafting effective Upwork profiles. 
        Based on the following professional information, create a concise and impactful professional title 
        (maximum 70 characters) that would attract clients on Upwork:
        
        Current title: {self.portfolio_data.get('basic_info', {}).get('title', '')}
        Experience: 
        {json.dumps(self.portfolio_data.get('experience', []), indent=2)}
        Skills: 
        {json.dumps(self.portfolio_data.get('skills', {}), indent=2)}
        
        The title should highlight expertise and specialization. Focus on data engineering, analytics, and cloud solutions.
        """
        
        response = self.ollama_client.generate(prompt)
        # Clean up the response to get just the title
        title = response.strip().replace('"', '').split('\n')[0]
        if len(title) > 70:
            title = title[:67] + "..."
        
        return title
    
    def _generate_overview_for_upwork(self):
        """Generate a professional overview optimized for Upwork."""
        prompt = f"""
        You are an expert in crafting effective Upwork profiles. 
        Based on the following professional information, create a compelling overview 
        (between 500-1000 characters) for an Upwork profile:
        
        About: 
        {json.dumps(self.portfolio_data.get('about', {}), indent=2)}
        Experience: 
        {json.dumps(self.portfolio_data.get('experience', []), indent=2)}
        Education: 
        {json.dumps(self.portfolio_data.get('education', []), indent=2)}
        Skills: 
        {json.dumps(self.portfolio_data.get('skills', {}), indent=2)}
        
        The overview should:
        1. Start with a strong opening statement about value proposition
        2. Highlight key achievements with quantifiable results
        3. Emphasize expertise in data engineering, analytics, and cloud solutions
        4. Include a clear call-to-action at the end
        5. Be written in first person
        """
        
        response = self.ollama_client.generate(prompt)
        # Return the generated overview
        return response.strip()
    
    def _select_skills_for_upwork(self):
        """Select the most relevant skills for Upwork based on portfolio data."""
        all_skills = self.portfolio_data.get('skills', {}).get('technical', [])
        
        prompt = f"""
        You are an expert in optimizing Upwork profiles.
        From the following list of skills, select the 10 most marketable skills for an Upwork profile 
        focusing on data engineering, analytics, and cloud solutions. Return ONLY the list of skills, 
        nothing else:
        
        {json.dumps(all_skills)}
        """
        
        response = self.ollama_client.generate(prompt)
        
        # Parse the response to get a clean list of skills
        skills = []
        for line in response.strip().split('\n'):
            skill = line.strip().replace('-', '').replace('*', '').strip()
            if skill and len(skills) < 10:
                skills.append(skill)
        
        return skills
    
    def _suggest_hourly_rate(self):
        """Suggest an appropriate hourly rate for Upwork based on experience level."""
        experience_years = self._calculate_experience_years()
        
        prompt = f"""
        You are an expert in Upwork pricing strategies.
        Based on {experience_years} years of experience in data engineering, analytics, and cloud solutions,
        suggest an appropriate hourly rate (USD) for Upwork that is competitive but values expertise.
        Consider that the professional has worked with enterprise clients and has demonstrated significant ROI.
        Return ONLY the hourly rate as a number, nothing else.
        """
        
        response = self.ollama_client.generate(prompt)
        
        # Parse the rate from the response
        try:
            rate = float(response.strip().replace('$', ''))
            return round(rate, 2)
        except ValueError:
            # Default rate if parsing fails
            return 65.00
    
    def _calculate_experience_years(self):
        """Calculate total years of professional experience."""
        # For the POC, we'll use a simple calculation based on available data
        # In a real implementation, this would parse dates properly
        experience = self.portfolio_data.get('experience', [])
        return len(experience) * 2  # Simple approximation
    
    def _fill_upwork_profile(self, content):
        """Use Playwright to fill out the Upwork profile."""
        logging.info("Attempting to fill Upwork profile through web automation")
        
        # This is a placeholder for the POC
        # In a real implementation, this would use Playwright to:
        # 1. Log in to Upwork
        # 2. Navigate to profile edit page
        # 3. Update the profile sections with the generated content
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            try:
                # Log in to Upwork
                page.goto('https://www.upwork.com/login')
                page.fill('input[name="login[username]"]', self.credentials['username'])
                page.fill('input[name="login[password]"]', self.credentials['password'])
                page.click('button[type="submit"]')
                
                # Wait for login to complete
                page.wait_for_navigation()
                
                # Navigate to profile edit page
                # Note: This is a simplified example - actual selectors would vary
                page.goto('https://www.upwork.com/freelancers/settings/profile')
                
                # Update title
                page.fill('input[name="title"]', content['title'])
                
                # Update overview
                page.fill('textarea[name="overview"]', content['overview'])
                
                # Update skills (simplified)
                # In reality, this would be more complex with dropdowns, etc.
                
                # Save changes
                page.click('button[type="submit"]')
                
                # Wait for confirmation
                page.wait_for_selector('.success-message')
                
                logging.info("Successfully updated Upwork profile")
                
            except PlaywrightTimeoutError as e:
                logging.error(f"Timeout error: {str(e)}")
                raise Exception(f"Timeout while updating profile: {str(e)}")
            except Exception as e:
                logging.error(f"Error filling profile: {str(e)}")
                raise
            finally:
                browser.close()
        
        return True