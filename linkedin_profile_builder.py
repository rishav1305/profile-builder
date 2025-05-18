import argparse
import logging
import json
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from portfolio_extractor import PortfolioExtractor
from deepseek_integration import DeepseekProfileGenerator
from linkedin_scraper import LinkedInScraper
from profile_logger import ProfileLogger

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("linkedin_profile_builder.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class LinkedInProfileBuilder:
    """Class to build and optimize LinkedIn profiles using AI."""
    
    def __init__(self, headless=False, portfolio_url=None):
        """Initialize the LinkedIn Profile Builder."""
        self.headless = headless
        self.portfolio_url = portfolio_url or "https://rishavchatterjee.com/"
        self.profile_data = None
        self.deepseek = DeepseekProfileGenerator()
        self.linkedin_scraper = LinkedInScraper(headless=headless)
        self.profile_logger = ProfileLogger()
    
    def extract_portfolio(self):
        """Extract portfolio data from the portfolio URL."""
        logger.info(f"Extracting portfolio data from {self.portfolio_url}")
        
        try:
            # Always get fresh data for the LinkedIn profile builder
            extractor = PortfolioExtractor(
                url=self.portfolio_url,
                use_cache=False  # Ensure we get fresh data
            )
            self.profile_data = extractor.extract()
            logger.info(f"Portfolio data extracted successfully, timestamp: {self.profile_data.get('last_updated')}")
            return True
        except Exception as e:
            logger.error(f"Error extracting portfolio data: {str(e)}")
            return False
    
    def build_linkedin_profile(self, credentials=None, profile_url=None):
        """
        Main method to build and optimize a LinkedIn profile.
        
        Args:
            credentials (dict): LinkedIn credentials (username, password)
            profile_url (str, optional): LinkedIn profile URL to optimize
        
        Returns:
            dict: Results of the profile building process
        """
        if not self.profile_data:
            if not self.extract_portfolio():
                return {"status": "error", "message": "Failed to extract portfolio data"}
        
        result = {
            "status": "content_generated",
            "timestamp": datetime.now().isoformat(),
            "changes": {}
        }
        
        try:
            # Generate optimized LinkedIn content using deepseek
            logger.info("Generating optimized LinkedIn profile content")
            headline = self.deepseek.generate_title(self.profile_data, platform="linkedin")
            about = self.deepseek.generate_overview(self.profile_data, platform="linkedin")
            skills = self.deepseek.select_skills(self.profile_data, platform="linkedin", max_skills=15)
            
            # Store generated content in result
            result["headline"] = headline
            result["about"] = about
            result["skills"] = skills
            
            # If credentials provided, attempt to update LinkedIn profile
            if credentials and credentials.get('username') and credentials.get('password'):
                logger.info("Credentials provided, attempting to update LinkedIn profile")
                
                # First scrape existing profile
                current_profile = self.linkedin_scraper.scrape_profile(profile_url, credentials)
                
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=self.headless)
                    context = browser.new_context(viewport={"width": 1280, "height": 800})
                    page = context.new_page()
                    
                    try:
                        # Login to LinkedIn
                        page.goto('https://www.linkedin.com/login')
                        page.fill('#username', credentials['username'])
                        page.fill('#password', credentials['password'])
                        page.click('button[type="submit"]')
                        page.wait_for_navigation()
                        
                        # Analyze current profile vs portfolio data
                        logger.info("Analyzing current LinkedIn profile")
                        suggestions = self.deepseek.analyze_current_profile(current_profile, self.profile_data)
                        
                        # Update the profile
                        changes = self.linkedin_scraper.update_linkedin_profile(page, suggestions)
                        
                        # Store changes in result
                        result["status"] = "profile_updated"
                        result["changes"] = changes
                        
                        # Get the profile URL
                        page.goto('https://www.linkedin.com/in/me/')
                        time.sleep(2)
                        profile_url = page.url
                        result["profile_url"] = profile_url
                        
                        # Log the changes
                        self.profile_logger.log_profile_update("linkedin", profile_url, changes)
                        
                    except Exception as e:
                        logger.error(f"Error updating LinkedIn profile: {str(e)}")
                        result["status"] = "error"
                        result["message"] = str(e)
                    
                    finally:
                        browser.close()
            
            return result
            
        except Exception as e:
            logger.error(f"Error in LinkedIn profile building: {str(e)}")
            return {"status": "error", "message": str(e)}

def main():
    """Main function to run the LinkedIn profile builder."""
    parser = argparse.ArgumentParser(description="LinkedIn Profile Builder")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    parser.add_argument("--portfolio", help="URL of portfolio to extract data from")
    args = parser.parse_args()
    
    logger.info("Starting LinkedIn Profile Builder")
    
    # Create builder instance
    builder = LinkedInProfileBuilder(
        headless=args.headless,
        portfolio_url=args.portfolio
    )
    
    # Extract portfolio data
    if not builder.extract_portfolio():
        logger.error("Failed to extract portfolio data. Exiting.")
        return
    
    # Ask for LinkedIn credentials
    print("\nEnter your LinkedIn credentials to update your profile automatically.")
    print("(Leave blank to generate content without updating your profile)")
    username = input("LinkedIn Email/Username: ")
    password = input("LinkedIn Password: ")
    
    credentials = None
    if username and password:
        credentials = {"username": username, "password": password}
    
    # Build LinkedIn profile
    result = builder.build_linkedin_profile(credentials)
    
    if result["status"] == "profile_updated":
        print("\n✅ LinkedIn profile successfully updated!")
        print(f"Profile URL: {result.get('profile_url')}")
        
        # Show what was changed
        changes = result.get("changes", {})
        if changes.get("headline"):
            print("\n📝 Updated Headline:")
            print(f"Before: {changes['headline']['before']}")
            print(f"After:  {changes['headline']['after']}")
        
        if changes.get("about"):
            print("\n📝 Updated About Section")
            print("About section updated with optimized content")
        
        if changes.get("skills_added"):
            print("\n📝 Added Skills:")
            print(", ".join(changes["skills_added"]))
            
    elif result["status"] == "content_generated":
        print("\n✅ LinkedIn profile content generated successfully!")
        print("\nHere's the generated content you can use to update your profile manually:")
        
        print("\n📝 Optimized Headline:")
        print(result["headline"])
        
        print("\n📝 Optimized About Section:")
        print(result["about"])
        
        print("\n📝 Recommended Skills:")
        print(", ".join(result["skills"]))
        
    else:
        print(f"\n❌ Error: {result.get('message', 'Unknown error')}")
    
    print("\nCheck the log file for more details: linkedin_profile_builder.log")

if __name__ == "__main__":
    main()
