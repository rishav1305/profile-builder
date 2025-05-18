import logging
import time
import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LinkedInScraper:
    """Class to scrape LinkedIn profiles for analysis and optimization."""
    
    def __init__(self, headless=False):
        """Initialize the LinkedIn scraper with browser options."""
        self.headless = headless
        self.profile_data = {}
        self.changes_made = {}
    
    def scrape_profile(self, profile_url=None, credentials=None):
        """
        Scrape a LinkedIn profile. If credentials are provided, will log in first.
        If profile_url is not provided, will scrape the user's own profile.
        
        Args:
            profile_url (str): URL of the profile to scrape
            credentials (dict): Username and password for LinkedIn
            
        Returns:
            dict: Scraped profile data
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(viewport={"width": 1280, "height": 800})
            page = context.new_page()
            
            try:
                logging.info("Starting LinkedIn profile scraping")
                
                # Log in if credentials provided
                if credentials and credentials.get('username') and credentials.get('password'):
                    self._login(page, credentials)
                
                # Navigate to the profile
                if profile_url:
                    page.goto(profile_url)
                else:
                    # Go to own profile
                    page.goto('https://www.linkedin.com/in/me/')
                
                # Wait for profile to load
                page.wait_for_selector('h1')
                
                # Extract profile data
                self.profile_data = self._extract_profile_data(page)
                
                logging.info("Successfully scraped LinkedIn profile")
                return self.profile_data
                
            except Exception as e:
                logging.error(f"Error scraping LinkedIn profile: {str(e)}")
                raise
            finally:
                browser.close()
    
    def _login(self, page, credentials):
        """Log into LinkedIn using provided credentials."""
        try:
            logging.info("Logging into LinkedIn...")
            page.goto('https://www.linkedin.com/login')
            
            # Fill in login form
            page.fill('#username', credentials['username'])
            page.fill('#password', credentials['password'])
            
            # Submit form
            page.click('button[type="submit"]')
            
            # Wait for navigation to complete
            page.wait_for_navigation()
            
            # Check for successful login by looking for navbar
            try:
                page.wait_for_selector('.global-nav', timeout=5000)
                logging.info("Successfully logged into LinkedIn")
            except PlaywrightTimeoutError:
                # Check if there's a security verification page
                if page.query_selector('.challenge-dialog'):
                    logging.warning("LinkedIn is requesting security verification")
                    raise Exception("LinkedIn security verification required. Please complete it manually.")
                raise Exception("Failed to log in. Check your credentials.")
                
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            raise
    
    def _extract_profile_data(self, page):
        """Extract various sections of profile data."""
        profile_data = {}
        
        # Basic info and headline
        try:
            name = page.query_selector('h1')
            profile_data['name'] = name.inner_text() if name else ""
            
            headline = page.query_selector('div.text-body-medium')
            profile_data['headline'] = headline.inner_text().strip() if headline else ""
        except Exception as e:
            logging.warning(f"Error extracting basic info: {str(e)}")
        
        # About section
        try:
            # Scroll to About section
            page.evaluate("() => { window.scrollBy(0, 300); }")
            time.sleep(1)
            
            about_section = page.query_selector("section:has(div:text('About')) div.display-flex")
            if about_section:
                profile_data['about'] = about_section.inner_text().strip()
            else:
                profile_data['about'] = ""
        except Exception as e:
            logging.warning(f"Error extracting about section: {str(e)}")
            profile_data['about'] = ""
        
        # Experience
        try:
            profile_data['experience'] = self._extract_experience(page)
        except Exception as e:
            logging.warning(f"Error extracting experience: {str(e)}")
            profile_data['experience'] = []
        
        # Education
        try:
            profile_data['education'] = self._extract_education(page)
        except Exception as e:
            logging.warning(f"Error extracting education: {str(e)}")
            profile_data['education'] = []
        
        # Skills
        try:
            profile_data['skills'] = self._extract_skills(page)
        except Exception as e:
            logging.warning(f"Error extracting skills: {str(e)}")
            profile_data['skills'] = []
        
        return profile_data
    
    def _extract_experience(self, page):
        """Extract the experience section."""
        experiences = []
        
        # Scroll to Experience section
        page.evaluate("() => { window.scrollBy(0, 500); }")
        time.sleep(1)
        
        try:
            # First check if we need to click "Show all experiences"
            show_all_button = page.query_selector("section:has(div:text('Experience')) button:text('Show all')")
            if show_all_button:
                show_all_button.click()
                time.sleep(1)
                
            # Get experience items
            exp_section = page.query_selector("section:has(div:text('Experience'))")
            if not exp_section:
                return experiences
                
            exp_items = exp_section.query_selector_all("li.artdeco-list__item")
            
            for item in exp_items:
                try:
                    position = item.query_selector(".t-bold") 
                    company = item.query_selector(".t-normal")
                    dates = item.query_selector(".t-normal.t-black--light")
                    description = item.query_selector(".pv-entity__description")
                    
                    position_text = position.inner_text().strip() if position else ""
                    company_text = company.inner_text().strip() if company else ""
                    dates_text = dates.inner_text().strip() if dates else ""
                    description_text = description.inner_text().strip() if description else ""
                    
                    experiences.append({
                        "title": position_text,
                        "company": company_text,
                        "duration": dates_text,
                        "description": description_text
                    })
                except Exception as e:
                    logging.warning(f"Error parsing an experience item: {str(e)}")
            
        except Exception as e:
            logging.warning(f"Error in experience extraction: {str(e)}")
            
        return experiences
        
    def _extract_education(self, page):
        """Extract the education section."""
        education = []
        
        # Scroll to Education section
        page.evaluate("() => { window.scrollBy(0, 300); }")
        time.sleep(1)
        
        try:
            # First check if we need to click "Show all education"
            show_all_button = page.query_selector("section:has(div:text('Education')) button:text('Show all')")
            if show_all_button:
                show_all_button.click()
                time.sleep(1)
                
            # Get education items
            edu_section = page.query_selector("section:has(div:text('Education'))")
            if not edu_section:
                return education
                
            edu_items = edu_section.query_selector_all("li.artdeco-list__item")
            
            for item in edu_items:
                try:
                    school = item.query_selector(".t-bold")
                    degree = item.query_selector(".t-normal")
                    dates = item.query_selector(".t-normal.t-black--light")
                    
                    school_text = school.inner_text().strip() if school else ""
                    degree_text = degree.inner_text().strip() if degree else ""
                    dates_text = dates.inner_text().strip() if dates else ""
                    
                    education.append({
                        "school": school_text,
                        "degree": degree_text,
                        "date_range": dates_text
                    })
                except Exception as e:
                    logging.warning(f"Error parsing an education item: {str(e)}")
            
        except Exception as e:
            logging.warning(f"Error in education extraction: {str(e)}")
            
        return education
    
    def _extract_skills(self, page):
        """Extract the skills section."""
        skills = []
        
        # Scroll to Skills section
        page.evaluate("() => { window.scrollBy(0, 700); }")
        time.sleep(1)
        
        try:
            # First check if we need to click "Show all skills"
            show_all_button = page.query_selector("section:has(div:text('Skills')) button:text('Show all')")
            if show_all_button:
                show_all_button.click()
                time.sleep(1)
                
            # Get skills items
            skills_section = page.query_selector("section:has(div:text('Skills'))")
            if not skills_section:
                return skills
            
            # In expanded view
            skill_items = skills_section.query_selector_all(".artdeco-modal__content .pv-skill-category-entity__name")
            
            # If no expanded view, try compact view
            if not skill_items or len(skill_items) == 0:
                skill_items = skills_section.query_selector_all(".pv-skill-category-entity__name")
            
            for item in skill_items:
                try:
                    skill_text = item.inner_text().strip()
                    if skill_text and skill_text not in skills:
                        skills.append(skill_text)
                except Exception as e:
                    logging.warning(f"Error parsing a skill item: {str(e)}")
            
        except Exception as e:
            logging.warning(f"Error in skills extraction: {str(e)}")
            
        return skills

    def update_linkedin_profile(self, page, suggestions):
        """
        Update a LinkedIn profile with the provided suggestions.
        
        Args:
            page: Playwright page object
            suggestions (dict): Profile improvements to apply
            
        Returns:
            dict: Changes that were made to the profile
        """
        changes = {"timestamp": datetime.now().isoformat()}
        
        try:
            # Update headline if provided
            if suggestions.get("headline"):
                old_headline = self.profile_data.get("headline", "")
                if self._update_headline(page, suggestions["headline"]):
                    changes["headline"] = {"before": old_headline, "after": suggestions["headline"]}
            
            # Update about section if provided
            if suggestions.get("about"):
                old_about = self.profile_data.get("about", "")
                if self._update_about(page, suggestions["about"]):
                    changes["about"] = {"before": old_about, "after": suggestions["about"]}
            
            # Update skills if provided
            if suggestions.get("skills_to_add"):
                added_skills = self._add_skills(page, suggestions["skills_to_add"])
                if added_skills:
                    changes["skills_added"] = added_skills
            
            return changes
            
        except Exception as e:
            logging.error(f"Error updating LinkedIn profile: {str(e)}")
            return changes
    
    def _update_headline(self, page, new_headline):
        """Update the LinkedIn headline."""
        try:
            logging.info("Updating LinkedIn headline...")
            
            # Navigate to edit intro section
            page.click('button[aria-label="Edit intro"]')
            page.wait_for_selector('input[id="single-line-text-form-component-headline"]')
            
            # Clear and update headline
            headline_input = page.query_selector('input[id="single-line-text-form-component-headline"]')
            headline_input.fill("")
            headline_input.fill(new_headline)
            
            # Save changes
            page.click('button[aria-label="Save"]')
            page.wait_for_timeout(2000)  # Wait for save to complete
            
            logging.info(f"Successfully updated headline to: {new_headline}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to update headline: {str(e)}")
            return False
    
    def _update_about(self, page, new_about):
        """Update the LinkedIn about section."""
        try:
            logging.info("Updating LinkedIn about section...")
            
            # Navigate to About section
            page.goto('https://www.linkedin.com/in/me/edit/about/')
            page.wait_for_load_state('networkidle')
            
            # Click edit button
            page.click('button[aria-label="Edit summary"]')
            
            # Clear and update about section
            about_input = page.query_selector('div[aria-label="Text editor for About"]')
            
            # Use evaluate to clear and update about text
            page.evaluate("""(element, value) => {
                element.textContent = '';
                const dataTransfer = new DataTransfer();
                dataTransfer.setData('text/plain', value);
                element.dispatchEvent(new ClipboardEvent('paste', {
                    clipboardData: dataTransfer,
                    bubbles: true
                }));
            }""", about_input, new_about)
            
            # Save changes
            page.click('button[aria-label="Save"]')
            page.wait_for_timeout(2000)  # Wait for save to complete
            
            logging.info("Successfully updated about section")
            return True
            
        except Exception as e:
            logging.error(f"Failed to update about section: {str(e)}")
            return False
    
    def _add_skills(self, page, skills_to_add, max_skills=10):
        """Add skills to LinkedIn profile."""
        added_skills = []
        
        try:
            logging.info("Adding skills to LinkedIn profile...")
            
            # Navigate to Skills section
            page.goto('https://www.linkedin.com/in/me/edit/skills/')
            page.wait_for_load_state('networkidle')
            
            # Get current skills to avoid duplicates
            current_skills_lower = [s.lower() for s in self.profile_data.get('skills', [])]
            
            # Add each skill that's not already in the profile
            for skill in skills_to_add[:max_skills]:  # Limit to max_skills
                if skill.lower() not in current_skills_lower:
                    try:
                        # Click Add skill button
                        page.click('button[aria-label="Add skill"]')
                        
                        # Fill in skill name
                        page.fill('input[aria-label="Skill"]', skill)
                        
                        # Wait for and select the first suggestion
                        page.wait_for_selector('ul[role="listbox"] li', timeout=5000)
                        page.click('ul[role="listbox"] li:first-child')
                        
                        # Click Add button to confirm skill
                        page.click('button[aria-label="Add"]')
                        page.wait_for_timeout(500)  # Brief pause
                        
                        added_skills.append(skill)
                        logging.info(f"Added skill: {skill}")
                    except Exception as e:
                        logging.warning(f"Failed to add skill '{skill}': {str(e)}")
            
            if added_skills:
                # Save all changes
                page.click('button[aria-label="Save"]')
                page.wait_for_timeout(2000)  # Wait for save
            
            logging.info(f"Successfully added {len(added_skills)} skills")
            return added_skills
            
        except Exception as e:
            logging.error(f"Failed to add skills: {str(e)}")
            return added_skills
