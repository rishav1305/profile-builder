import logging
import json
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from deepseek_integration import DeepseekProfileGenerator
from ollama_integration import OllamaClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProfileBuilder:
    """
    Class to build professional profiles on remote work platforms
    using portfolio data and Ollama for intelligent content generation.
    """
    
    def __init__(self, platform, portfolio_data, credentials=None, model="deepseek-r1"):
        self.platform = platform.lower()
        self.portfolio_data = portfolio_data
        self.credentials = credentials or {}
        
        # Initialize OllamaClient for basic operations
        self.ollama_client = OllamaClient(model=model)
        
        # Initialize DeepseekProfileGenerator for specialized profile content generation
        self.deepseek_generator = DeepseekProfileGenerator()
        
        # Map platform names to their respective builder methods
        self.platform_map = {
            'upwork': self._build_upwork_profile,
            'linkedin': self._build_linkedin_profile
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
        """Generate a professional title optimized for Upwork using the DeepseekProfileGenerator."""
        logging.info("Generating professional title for Upwork using deepseek-r1")
        return self.deepseek_generator.generate_title(self.portfolio_data, platform="upwork")
    
    def _generate_overview_for_upwork(self):
        """Generate a professional overview optimized for Upwork using the DeepseekProfileGenerator."""
        logging.info("Generating professional overview for Upwork using deepseek-r1")
        return self.deepseek_generator.generate_overview(self.portfolio_data, platform="upwork")
    
    def _select_skills_for_upwork(self):
        """Select the most relevant skills for Upwork based on portfolio data using the DeepseekProfileGenerator."""
        logging.info("Selecting skills for Upwork using deepseek-r1")
        return self.deepseek_generator.select_skills(self.portfolio_data, platform="upwork", max_skills=10)
    
    def _suggest_hourly_rate(self):
        """Suggest an appropriate hourly rate for Upwork based on experience level using the DeepseekProfileGenerator."""
        logging.info("Suggesting hourly rate for Upwork using deepseek-r1")
        return self.deepseek_generator.suggest_hourly_rate(self.portfolio_data, platform="upwork")
    
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
    
    def _build_linkedin_profile(self):
        """Build a profile on LinkedIn."""
        logging.info("Building LinkedIn profile")
        
        # Use Ollama to generate optimized content for LinkedIn
        headline = self._generate_headline_for_linkedin()
        about = self._generate_about_for_linkedin()
        skills = self._select_skills_for_linkedin()
        
        # For POC, we'll just return the generated content
        # In a real implementation, this would use Playwright to fill out forms
        result = {
            'headline': headline,
            'about': about,
            'skills': skills,
            'status': 'content_generated'
        }
        
        # If credentials are provided, attempt to fill out the profile
        if self.credentials.get('username') and self.credentials.get('password'):
            try:
                self._fill_linkedin_profile(result)
                result['status'] = 'profile_updated'
            except Exception as e:
                logging.error(f"Error filling LinkedIn profile: {str(e)}")
                result['error'] = str(e)
        
        return result
        
    def _generate_headline_for_linkedin(self):
        """Generate a professional headline optimized for LinkedIn."""
        prompt = f"""
        You are an expert in crafting effective LinkedIn profiles. 
        Based on the following professional information, create a concise and impactful professional headline 
        (maximum 220 characters) that would attract recruiters and connections on LinkedIn:
        
        Current title: {self.portfolio_data.get('basic_info', {}).get('title', '')}
        Experience: 
        {json.dumps(self.portfolio_data.get('experience', []), indent=2)}
        Skills: 
        {json.dumps(self.portfolio_data.get('skills', {}), indent=2)}
        
        The headline should be professional, highlight expertise and specialization.
        Focus on keywords that are relevant for your industry and role.
        """
        
        response = self.ollama_client.generate(prompt)
        # Clean up the response to get just the headline
        headline = response.strip().replace('"', '').split('\n')[0]
        if len(headline) > 220:
            headline = headline[:217] + "..."
        
        return headline
        
    def _generate_about_for_linkedin(self):
        """Generate a professional about/summary section optimized for LinkedIn."""
        prompt = f"""
        You are an expert in crafting effective LinkedIn profiles. 
        Based on the following professional information, create a compelling summary/about section
        (between 800-2000 characters) for a LinkedIn profile:
        
        About: 
        {json.dumps(self.portfolio_data.get('about', {}), indent=2)}
        Experience: 
        {json.dumps(self.portfolio_data.get('experience', []), indent=2)}
        Education: 
        {json.dumps(self.portfolio_data.get('education', []), indent=2)}
        Skills: 
        {json.dumps(self.portfolio_data.get('skills', {}), indent=2)}
        
        The summary should:
        1. Start with a strong opening statement about your professional identity and value
        2. Highlight key achievements with quantifiable results
        3. Include keywords relevant to your industry for better search visibility
        4. Be written in first person
        5. End with a clear indication of your career goals or interests
        """
        
        response = self.ollama_client.generate(prompt)
        # Return the generated summary
        return response.strip()
        
    def _select_skills_for_linkedin(self):
        """Select the most relevant skills for LinkedIn based on portfolio data."""
        all_skills = self.portfolio_data.get('skills', {}).get('technical', [])
        
        prompt = f"""
        You are an expert in optimizing LinkedIn profiles.
        From the following list of skills, select the 50 most relevant skills for a LinkedIn profile 
        based on the following information. Consider industry trends and SEO for better visibility.
        Return ONLY the list of skills, with each skill on a new line (no bullets or numbers):
        
        Experience: 
        {json.dumps(self.portfolio_data.get('experience', []), indent=2)}
        Skills: 
        {json.dumps(all_skills)}
        """
        
        response = self.ollama_client.generate(prompt)
        
        # Parse the response to get a clean list of skills
        skills = []
        for line in response.strip().split('\n'):
            skill = line.strip().replace('-', '').replace('*', '').strip()
            if skill and len(skills) < 50:  # LinkedIn allows up to 50 skills
                skills.append(skill)
        
        return skills
    
    def _fill_linkedin_profile(self, content):
        """Use Playwright to fill out the LinkedIn profile."""
        logging.info("Attempting to fill LinkedIn profile through web automation")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            try:
                # Log in to LinkedIn
                page.goto('https://www.linkedin.com/login')
                page.fill('#username', self.credentials['username'])
                page.fill('#password', self.credentials['password'])
                page.click('button[type="submit"]')
                
                # Wait for login to complete
                page.wait_for_navigation()
                
                # Navigate to profile edit page
                page.goto('https://www.linkedin.com/in/me/edit/intro/')
                page.wait_for_load_state('networkidle')
                
                # Update headline
                try:
                    # Click on headline pencil icon
                    page.click('button[aria-label="Edit intro"]')
                    headline_input = page.locator('input[id="single-line-text-form-component-headline"]')
                    headline_input.fill(content['headline'])
                    
                    # Save changes
                    page.click('button[aria-label="Save"]')
                    page.wait_for_timeout(1000)  # Wait for save to complete
                except Exception as e:
                    logging.error(f"Error updating headline: {str(e)}")
                
                # Update about/summary section
                try:
                    # Navigate to About section
                    page.goto('https://www.linkedin.com/in/me/edit/about/')
                    page.wait_for_load_state('networkidle')
                    
                    # Find and update the summary textarea
                    page.click('button[aria-label="Edit summary"]')
                    summary_input = page.locator('div[aria-label="Text editor for About"]')
                    summary_input.fill(content['about'])
                    
                    # Save changes
                    page.click('button[aria-label="Save"]')
                    page.wait_for_timeout(1000)  # Wait for save to complete
                except Exception as e:
                    logging.error(f"Error updating about section: {str(e)}")
                
                # Add skills - this is simplified and would need refinement in production
                try:
                    # Navigate to Skills section
                    page.goto('https://www.linkedin.com/in/me/edit/skills/')
                    page.wait_for_load_state('networkidle')
                    
                    # For each skill not already added, try to add it
                    for skill in content['skills'][:10]:  # Limit to first 10 for the POC
                        try:
                            # Click Add skill button
                            page.click('button[aria-label="Add skill"]')
                            
                            # Fill in skill name
                            page.fill('input[aria-label="Skill"]', skill)
                            
                            # Select the first suggestion
                            page.wait_for_selector('ul[role="listbox"] li', timeout=5000)
                            page.click('ul[role="listbox"] li:first-child')
                            
                            # Save the skill
                            page.click('button[aria-label="Add"]')
                            page.wait_for_timeout(500)  # Brief pause between skills
                        except Exception as skill_e:
                            logging.warning(f"Could not add skill '{skill}': {str(skill_e)}")
                except Exception as e:
                    logging.error(f"Error updating skills: {str(e)}")
                
                logging.info("Successfully updated LinkedIn profile")
                
            except PlaywrightTimeoutError as e:
                logging.error(f"Timeout error: {str(e)}")
                raise Exception(f"Timeout while updating profile: {str(e)}")
            except Exception as e:
                logging.error(f"Error filling profile: {str(e)}")
                raise
            finally:
                browser.close()
        
        return True