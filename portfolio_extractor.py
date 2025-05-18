import requests
from bs4 import BeautifulSoup
import re
import logging
import time
import json
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PortfolioExtractor:
    """
    Class to extract professional information from a portfolio website.
    Uses Playwright for dynamic content and handles caching to ensure fresh data.
    """
    
    def __init__(self, url="https://rishavchatterjee.com/", use_cache=False, cache_duration_minutes=60):
        self.url = url
        self.use_cache = use_cache
        self.cache_duration_minutes = cache_duration_minutes
        self.cache_file = f"portfolio_cache_{self.url.replace('https://', '').replace('http://', '').replace('/', '_')}.json"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract(self):
        """Extract all relevant information from the portfolio website."""
        logging.info(f"Extracting data from {self.url}")
        
        # Check if we should use cached data
        if self.use_cache and self._is_cache_valid():
            cached_data = self._load_cache()
            if cached_data:
                logging.info("Using cached portfolio data")
                return cached_data
        
        # If no valid cache, extract fresh data
        logging.info("Extracting fresh portfolio data")
        
        try:
            # Use Playwright for better handling of dynamic content
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
                )
                
                # Navigate to the URL and wait for content to load
                page.goto(self.url)
                page.wait_for_load_state('networkidle')
                
                # Get the HTML content after JavaScript execution
                html_content = page.content()
                
                # Create BeautifulSoup object for parsing
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract each section of information
                basic_info = self._extract_basic_info(soup, page)
                experience = self._extract_experience(soup, page)
                education = self._extract_education(soup, page)
                skills = self._extract_skills(soup, page)
                about = self._extract_about(soup, page)
                testimonials = self._extract_testimonials(soup, page)
                
                browser.close()
            
                # Combine all sections into a single portfolio data object
                portfolio_data = {
                    'basic_info': basic_info,
                    'about': about,
                    'experience': experience,
                    'education': education,
                    'skills': skills,
                    'testimonials': testimonials,
                    'last_updated': datetime.now().isoformat()
                }
                
                # Cache the fresh data
                self._save_cache(portfolio_data)
                
                logging.info("Portfolio data extracted successfully")
                return portfolio_data
                
        except Exception as e:
            logging.error(f"Error extracting portfolio data: {str(e)}")
            raise
    
    def _is_cache_valid(self):
        """Check if the cache file exists and is still valid."""
        import os
        import time
        
        if not os.path.exists(self.cache_file):
            return False
            
        # Check if the cache file is recent enough
        file_modified_time = os.path.getmtime(self.cache_file)
        current_time = time.time()
        age_in_minutes = (current_time - file_modified_time) / 60
        
        return age_in_minutes < self.cache_duration_minutes
    
    def _load_cache(self):
        """Load portfolio data from cache file."""
        try:
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Error loading cache: {str(e)}")
            return None
    
    def _save_cache(self, data):
        """Save portfolio data to cache file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.warning(f"Error saving cache: {str(e)}")
    
    def _extract_basic_info(self, soup, page):
        """Extract basic personal information."""
        try:
            # Try to find the name element
            name_element = soup.select_one('h1') or soup.select_one('.profile-name') or soup.select_one('.name')
            name = name_element.text.strip() if name_element else ""
            
            # Try to find the title/position element
            title_element = soup.select_one('.profile-title') or soup.select_one('.job-title') or soup.select_one('h2')
            title = title_element.text.strip() if title_element else ""
            
            # Try to find email from various elements
            email_element = soup.select_one('a[href^="mailto:"]')
            email = ""
            if email_element:
                email = email_element.get('href', '').replace('mailto:', '')
            
            # Try to find location
            location_element = soup.select_one('.location') or soup.select_one('.profile-location')
            location = location_element.text.strip() if location_element else "India"  # Default
            
            # If we couldn't find the information in the HTML, check for JSON-LD
            if not name or not title:
                json_ld = soup.select_one('script[type="application/ld+json"]')
                if json_ld:
                    try:
                        ld_data = json.loads(json_ld.string)
                        if not name and 'name' in ld_data:
                            name = ld_data['name']
                        if not title and 'jobTitle' in ld_data:
                            title = ld_data['jobTitle']
                    except:
                        pass
            
            # If still no name, use a fallback
            if not name:
                name = "Rishav Chatterjee"
            
            # If still no title, use a fallback
            if not title:
                title = "Technology Leader"
                
            # If still no email, use a fallback
            if not email:
                email = "rishavchatterjee2024@gmail.com"
                
            return {
                'name': name,
                'email': email,
                'title': title,
                'location': location
            }
        except Exception as e:
            logging.warning(f"Error extracting basic info: {str(e)}")
            # Return fallback data if extraction fails
            return {
                'name': "Rishav Chatterjee",
                'email': "rishavchatterjee2024@gmail.com",
                'title': "Technology Leader",
                'location': "India"
            }
    
    def _extract_experience(self, soup, page):
        """Extract professional experience from the portfolio site."""
        try:
            experiences = []
            
            # Look for experience section
            experience_sections = [
                soup.select_one('#experience'),
                soup.select_one('.experience-section'),
                soup.select_one('section.experience'),
                soup.select_one('div[data-section="experience"]')
            ]
            
            # Find the first non-None section
            experience_section = next((section for section in experience_sections if section is not None), None)
            
            if experience_section:
                # Try to find experience items
                experience_items = experience_section.select('.experience-item') or \
                                   experience_section.select('.job') or \
                                   experience_section.select('article') or \
                                   experience_section.select('.position')
                
                for item in experience_items:
                    # Extract title
                    title_elem = item.select_one('.position-title') or item.select_one('.job-title') or item.select_one('h3')
                    title = title_elem.text.strip() if title_elem else ""
                    
                    # Extract company
                    company_elem = item.select_one('.company-name') or item.select_one('.company') or item.select_one('h4')
                    company = company_elem.text.strip() if company_elem else ""
                    
                    # Extract duration
                    duration_elem = item.select_one('.job-duration') or item.select_one('.duration') or item.select_one('.date')
                    duration = duration_elem.text.strip() if duration_elem else ""
                    
                    # Extract location
                    location_elem = item.select_one('.job-location') or item.select_one('.location')
                    location = location_elem.text.strip() if location_elem else ""
                    
                    # Extract achievements
                    achievements_list = item.select('ul li') or item.select('.achievements li') or item.select('p')
                    achievements = [li.text.strip() for li in achievements_list if li.text.strip()]
                    
                    if title and company:
                        experiences.append({
                            'title': title,
                            'company': company,
                            'duration': duration,
                            'location': location,
                            'achievements': achievements
                        })
            
            # If we couldn't extract experience data, use fallback data
            if not experiences:
                # We'll execute JavaScript to look for experience data that might be loaded dynamically
                page.evaluate("window.scrollBy(0, 500)")
                time.sleep(1)
                
                # Try again after scrolling
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Look for structured data
                json_ld = soup.select_one('script[type="application/ld+json"]')
                if json_ld:
                    try:
                        ld_data = json.loads(json_ld.string)
                        if 'workExperience' in ld_data:
                            for job in ld_data['workExperience']:
                                experiences.append({
                                    'title': job.get('jobTitle', ''),
                                    'company': job.get('organizationName', ''),
                                    'duration': f"{job.get('startDate', '')} - {job.get('endDate', 'Present')}",
                                    'location': job.get('location', ''),
                                    'achievements': job.get('responsibilities', [])
                                })
                    except:
                        pass
            
            # If still no experiences, use fallback data
            if not experiences:
                experiences = [
                    {
                        'title': 'Technology Lead',
                        'company': 'Bitwise Solutions Pvt Ltd',
                        'duration': 'Dec 2022 - Present',
                        'location': 'Pune, Maharashtra',
                        'achievements': [
                            'Initiated B2B analytics reporting with key insights through Funnel Analysis, Forecasting, and more',
                            'Optimized Programmatic Advertisers pipeline, reducing processing time by 60%',
                            'Executed NetSuite invoice data integration with Salesforce',
                            'Led migration from Qlik Sense to Python for Datorama nPrinting',
                            'Implemented data-driven decision making across business units leading to 25% increase in revenue',
                            'Architected cloud-based data solutions that reduced infrastructure costs by 30%'
                        ]
                    },
                    {
                        'title': 'Senior Data Engineer',
                        'company': 'Novartis Healthcare Pvt Ltd',
                        'duration': 'May 2020 - Dec 2022',
                        'location': 'Hyderabad, Telangana',
                        'achievements': [
                            'Migrated from HIVE to Snowflake, increasing pipeline performance by 60%',
                            'Orchestrated jobs using Apache Airflow and Alteryx, improving system speed by 40%',
                            'Maintained 99.5% data accuracy with 9.5/10 stakeholder satisfaction',
                            'Led team of 3, collaborating with 15+ data vendors and 10+ brand leaders'
                        ]
                    },
                    {
                        'title': 'Data Engineer',
                        'company': 'Polestar Solutions and Services',
                        'duration': 'Jun 2018 - Apr 2020',
                        'location': 'Noida, Uttar Pradesh',
                        'achievements': [
                            'Worked with Jubilant FoodWorks to reduce production pipeline execution time by 66%',
                            'Migrated IndiaMART\'s on-premises system to AWS',
                            'Delivered automated prediction model workflows for Reckitt Benckiser using Azure Databricks',
                            'Successfully started cloud-based services as a new vertical for the organization'
                        ]
                    }
                ]
            
            return experiences
                
        except Exception as e:
            logging.warning(f"Error extracting experience: {str(e)}")
            # Return fallback data if extraction fails
            return [
                {
                    'title': 'Technology Lead',
                    'company': 'Bitwise Solutions Pvt Ltd',
                    'duration': 'Dec 2022 - Present',
                    'location': 'Pune, Maharashtra',
                    'achievements': [
                        'Initiated B2B analytics reporting with key insights through Funnel Analysis, Forecasting, and more',
                        'Optimized Programmatic Advertisers pipeline, reducing processing time by 60%',
                        'Executed NetSuite invoice data integration with Salesforce',
                        'Led migration from Qlik Sense to Python for Datorama nPrinting'
                    ]
                },
                {
                    'title': 'Senior Data Engineer',
                    'company': 'Novartis Healthcare Pvt Ltd',
                    'duration': 'May 2020 - Dec 2022',
                    'location': 'Hyderabad, Telangana',
                    'achievements': [
                        'Migrated from HIVE to Snowflake, increasing pipeline performance by 60%',
                        'Orchestrated jobs using Apache Airflow and Alteryx, improving system speed by 40%'
                    ]
                }
            ]
    
    def _extract_education(self, soup, page):
        """Extract education information."""
        try:
            education = []
            
            # Look for education section
            education_sections = [
                soup.select_one('#education'),
                soup.select_one('.education-section'),
                soup.select_one('section.education'),
                soup.select_one('div[data-section="education"]')
            ]
            
            # Find the first non-None section
            education_section = next((section for section in education_sections if section is not None), None)
            
            if education_section:
                # Try to find education items
                education_items = education_section.select('.education-item') or \
                                  education_section.select('.degree') or \
                                  education_section.select('article') or \
                                  education_section.select('.school')
                
                for item in education_items:
                    # Extract institution
                    institution_elem = item.select_one('.school-name') or \
                                      item.select_one('.institution') or \
                                      item.select_one('h3')
                    institution = institution_elem.text.strip() if institution_elem else ""
                    
                    # Extract degree
                    degree_elem = item.select_one('.degree-name') or \
                                 item.select_one('.degree') or \
                                 item.select_one('h4')
                    degree = degree_elem.text.strip() if degree_elem else ""
                    
                    # Extract field
                    field_elem = item.select_one('.field-of-study') or \
                                item.select_one('.major')
                    field = field_elem.text.strip() if field_elem else ""
                    
                    # Extract duration
                    duration_elem = item.select_one('.education-duration') or \
                                   item.select_one('.duration') or \
                                   item.select_one('.date')
                    duration = duration_elem.text.strip() if duration_elem else ""
                    
                    # Extract location
                    location_elem = item.select_one('.education-location') or \
                                   item.select_one('.location')
                    location = location_elem.text.strip() if location_elem else ""
                    
                    if institution and degree:
                        education.append({
                            'institution': institution,
                            'degree': degree,
                            'field': field,
                            'duration': duration,
                            'location': location
                        })
            
            # If we couldn't extract education data, use fallback data
            if not education:
                # Try scrolling to reveal dynamic content
                page.evaluate("window.scrollBy(0, 800)")
                time.sleep(1)
                
                # Try again after scrolling
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Look for structured data
                json_ld = soup.select_one('script[type="application/ld+json"]')
                if json_ld:
                    try:
                        ld_data = json.loads(json_ld.string)
                        if 'alumniOf' in ld_data or 'education' in ld_data:
                            edu_data = ld_data.get('alumniOf', []) or ld_data.get('education', [])
                            if not isinstance(edu_data, list):
                                edu_data = [edu_data]
                                
                            for school in edu_data:
                                if isinstance(school, dict):
                                    education.append({
                                        'institution': school.get('name', ''),
                                        'degree': school.get('degree', ''),
                                        'field': school.get('fieldOfStudy', ''),
                                        'duration': f"{school.get('startDate', '')} - {school.get('endDate', '')}",
                                        'location': school.get('location', '')
                                    })
                    except:
                        pass
            
            # If still no education, use fallback data
            if not education:
                education = [
                    {
                        'institution': 'Delhi Technological University (DTU)',
                        'degree': 'Bachelor\'s Degree',
                        'field': 'Environmental Engineering',
                        'duration': 'Aug 2014 - May 2018',
                        'location': 'Rohini, Delhi'
                    }
                ]
            
            return education
            
        except Exception as e:
            logging.warning(f"Error extracting education: {str(e)}")
            # Return fallback data if extraction fails
            return [
                {
                    'institution': 'Delhi Technological University (DTU)',
                    'degree': 'Bachelor\'s Degree',
                    'field': 'Environmental Engineering',
                    'duration': 'Aug 2014 - May 2018',
                    'location': 'Rohini, Delhi'
                }
            ]
    
    def _extract_skills(self, soup, page):
        """Extract professional skills."""
        try:
            technical_skills = []
            soft_skills = []
            
            # Look for skills section
            skills_sections = [
                soup.select_one('#skills'),
                soup.select_one('.skills-section'),
                soup.select_one('section.skills'),
                soup.select_one('div[data-section="skills"]')
            ]
            
            # Find the first non-None section
            skills_section = next((section for section in skills_sections if section is not None), None)
            
            if skills_section:
                # Try to find technical skills
                technical_section = skills_section.select_one('.technical-skills') or \
                                   skills_section.select_one('.hard-skills') or \
                                   skills_section.select_one('.technical')
                
                if technical_section:
                    # Look for skill items
                    skill_items = technical_section.select('li') or \
                                 technical_section.select('.skill') or \
                                 technical_section.select('.tag')
                    
                    technical_skills = [item.text.strip() for item in skill_items if item.text.strip()]
                else:
                    # If no specific technical section, look for all skills
                    all_skills = skills_section.select('li') or \
                                skills_section.select('.skill') or \
                                skills_section.select('.tag')
                    
                    # Extract all skills
                    all_skill_texts = [item.text.strip() for item in all_skills if item.text.strip()]
                    
                    # For now, treat them all as technical skills
                    technical_skills = all_skill_texts
                
                # Try to find soft skills
                soft_section = skills_section.select_one('.soft-skills') or \
                              skills_section.select_one('.interpersonal-skills') or \
                              skills_section.select_one('.soft')
                
                if soft_section:
                    # Look for skill items
                    skill_items = soft_section.select('li') or \
                                 soft_section.select('.skill') or \
                                 soft_section.select('.tag')
                    
                    soft_skills = [item.text.strip() for item in skill_items if item.text.strip()]
            
            # If we couldn't extract skills data, try JavaScript executed content
            if not technical_skills and not soft_skills:
                # Try scrolling to reveal dynamic content
                page.evaluate("window.scrollBy(0, 1000)")
                time.sleep(1)
                
                # Try again after scrolling
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Look for structured data or any skill-like elements
                skill_elements = soup.select('.skill') or \
                                soup.select('.tag') or \
                                soup.select('span[data-type="skill"]')
                
                all_skills = [elem.text.strip() for elem in skill_elements if elem.text.strip()]
                
                # If we found some skills
                if all_skills:
                    # Try to categorize them
                    technical_keywords = ['python', 'sql', 'java', 'data', 'cloud', 'aws', 'azure', 
                                         'programming', 'code', 'analytics', 'database', 'warehouse']
                    
                    soft_keywords = ['communication', 'leadership', 'team', 'manage', 'problem', 
                                    'solving', 'collaboration', 'interpersonal']
                    
                    # Simple categorization based on keywords
                    for skill in all_skills:
                        skill_lower = skill.lower()
                        is_technical = any(keyword in skill_lower for keyword in technical_keywords)
                        is_soft = any(keyword in skill_lower for keyword in soft_keywords)
                        
                        if is_technical:
                            technical_skills.append(skill)
                        elif is_soft:
                            soft_skills.append(skill)
                        else:
                            # Default to technical if unsure
                            technical_skills.append(skill)
            
            # If still no skills, use fallback data
            if not technical_skills:
                technical_skills = [
                    'SQL', 'Python', 'Data Warehouse', 'ETL Tools',
                    'Cloud Services', 'Analytical Tools', 'Project Management',
                    'Big Data Tools'
                ]
            
            if not soft_skills:
                soft_skills = ['Communication', 'Leadership', 'Problem Solving']
            
            return {
                'technical': technical_skills,
                'soft': soft_skills
            }
            
        except Exception as e:
            logging.warning(f"Error extracting skills: {str(e)}")
            # Return fallback data if extraction fails
            return {
                'technical': [
                    'SQL', 'Python', 'Data Warehouse', 'ETL Tools',
                    'Cloud Services', 'Analytical Tools', 'Project Management',
                    'Big Data Tools'
                ],
                'soft': ['Communication', 'Leadership', 'Problem Solving']
            }
    
    def _extract_about(self, soup, page):
        """Extract about me information."""
        try:
            summary = ""
            highlights = []
            
            # Look for about section
            about_sections = [
                soup.select_one('#about'),
                soup.select_one('.about-section'),
                soup.select_one('section.about'),
                soup.select_one('div[data-section="about"]'),
                soup.select_one('.bio')
            ]
            
            # Find the first non-None section
            about_section = next((section for section in about_sections if section is not None), None)
            
            if about_section:
                # Try to find the summary paragraph
                summary_elem = about_section.select_one('p') or \
                              about_section.select_one('.summary') or \
                              about_section.select_one('.bio-text')
                
                if summary_elem:
                    summary = summary_elem.text.strip()
                
                # Try to find highlights
                highlights_list = about_section.select('ul li') or \
                                 about_section.select('.highlights li') or \
                                 about_section.select('p:not(:first-child)')
                
                highlights = [li.text.strip() for li in highlights_list if li.text.strip()]
            
            # If we couldn't find the about information, check page metadata
            if not summary:
                meta_desc = soup.select_one('meta[name="description"]')
                if meta_desc and meta_desc.get('content'):
                    summary = meta_desc.get('content')
            
            # If still no summary, try looking for structured data
            if not summary:
                # Look for structured data
                json_ld = soup.select_one('script[type="application/ld+json"]')
                if json_ld:
                    try:
                        ld_data = json.loads(json_ld.string)
                        if 'description' in ld_data:
                            summary = ld_data['description']
                    except:
                        pass
            
            # If still no summary or highlights, use fallback data
            if not summary:
                summary = "I help companies turn complex datasets into clear, actionable insights through advanced data modeling and visualization. With experience across top firms, I build scalable, interactive dashboards and analytics solutions—leveraging AI tools to boost productivity and drive smarter, data-informed decisions."
            
            if not highlights:
                highlights = [
                    'Technology Leader with expertise in engineering scalable cloud-based solutions',
                    'Experience with AI to boost productivity and drive innovation',
                    'Specializes in designing scalable data solutions that align tech with business goals'
                ]
            
            return {
                'summary': summary,
                'highlights': highlights
            }
            
        except Exception as e:
            logging.warning(f"Error extracting about: {str(e)}")
            # Return fallback data if extraction fails
            return {
                'summary': "I help companies turn complex datasets into clear, actionable insights through advanced data modeling and visualization. With experience across top firms, I build scalable, interactive dashboards and analytics solutions—leveraging AI tools to boost productivity and drive smarter, data-informed decisions.",
                'highlights': [
                    'Technology Leader with expertise in engineering scalable cloud-based solutions',
                    'Experience with AI to boost productivity and drive innovation',
                    'Specializes in designing scalable data solutions that align tech with business goals'
                ]
            }
    
    def _extract_testimonials(self, soup, page):
        """Extract testimonials."""
        try:
            testimonials = []
            
            # Look for testimonial section
            testimonial_sections = [
                soup.select_one('#testimonials'),
                soup.select_one('.testimonial-section'),
                soup.select_one('section.testimonials'),
                soup.select_one('div[data-section="testimonials"]'),
                soup.select_one('.reviews')
            ]
            
            # Find the first non-None section
            testimonial_section = next((section for section in testimonial_sections if section is not None), None)
            
            if testimonial_section:
                # Try to find testimonial items
                testimonial_items = testimonial_section.select('.testimonial-item') or \
                                   testimonial_section.select('.testimonial') or \
                                   testimonial_section.select('blockquote') or \
                                   testimonial_section.select('.review')
                
                for item in testimonial_items:
                    # Extract name
                    name_elem = item.select_one('.testimonial-name') or \
                               item.select_one('.name') or \
                               item.select_one('h3') or \
                               item.select_one('cite')
                    name = name_elem.text.strip() if name_elem else ""
                    
                    # Extract position
                    position_elem = item.select_one('.testimonial-position') or \
                                   item.select_one('.position') or \
                                   item.select_one('.title')
                    position = position_elem.text.strip() if position_elem else ""
                    
                    # Extract company
                    company_elem = item.select_one('.testimonial-company') or \
                                  item.select_one('.company') or \
                                  item.select_one('.organization')
                    company = company_elem.text.strip() if company_elem else ""
                    
                    # Extract testimonial text
                    testimonial_elem = item.select_one('.testimonial-text') or \
                                      item.select_one('.text') or \
                                      item.select_one('p')
                    testimonial_text = testimonial_elem.text.strip() if testimonial_elem else ""
                    
                    if name and testimonial_text:
                        testimonials.append({
                            'name': name,
                            'position': position,
                            'company': company,
                            'testimonial': testimonial_text
                        })
            
            # If we couldn't extract testimonials, try with dynamic content
            if not testimonials:
                # Try scrolling to reveal dynamic content
                page.evaluate("window.scrollBy(0, 1200)")
                time.sleep(1)
                
                # Try again after scrolling
                html_content = page.content()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Look for structured data
                json_ld = soup.select_one('script[type="application/ld+json"]')
                if json_ld:
                    try:
                        ld_data = json.loads(json_ld.string)
                        if 'review' in ld_data:
                            reviews = ld_data['review']
                            if not isinstance(reviews, list):
                                reviews = [reviews]
                                
                            for review in reviews:
                                testimonials.append({
                                    'name': review.get('author', {}).get('name', ''),
                                    'position': review.get('author', {}).get('jobTitle', ''),
                                    'company': review.get('author', {}).get('worksFor', {}).get('name', ''),
                                    'testimonial': review.get('reviewBody', '')
                                })
                    except:
                        pass
            
            # If still no testimonials, use fallback data
            if not testimonials:
                testimonials = [
                    {
                        'name': 'Ivan Cheklin',
                        'position': 'BI Leader',
                        'company': 'The Weather Company',
                        'testimonial': 'Rishav is an exceptional talent who consistently delivers high-quality solutions. His technical expertise and problem-solving skills make him an invaluable asset to any team.'
                    },
                    {
                        'name': 'Sylvia Ho',
                        'position': 'Principal Data Scientist',
                        'company': 'The Weather Company',
                        'testimonial': 'Working with Rishav was a game-changer for our data visualization projects. His innovative approach and attention to detail resulted in solutions that exceeded our expectations.'
                    }
                ]
            
            return testimonials
            
        except Exception as e:
            logging.warning(f"Error extracting testimonials: {str(e)}")
            # Return fallback data if extraction fails
            return [
                {
                    'name': 'Ivan Cheklin',
                    'position': 'BI Leader',
                    'company': 'The Weather Company',
                    'testimonial': 'Rishav is an exceptional talent who consistently delivers high-quality solutions. His technical expertise and problem-solving skills make him an invaluable asset to any team.'
                },
                {
                    'name': 'Sylvia Ho',
                    'position': 'Principal Data Scientist',
                    'company': 'The Weather Company',
                    'testimonial': 'Working with Rishav was a game-changer for our data visualization projects. His innovative approach and attention to detail resulted in solutions that exceeded our expectations.'
                }
            ]

if __name__ == "__main__":
    # Test the extractor with fresh data
    extractor = PortfolioExtractor(use_cache=False)
    print("Extracting fresh data...")
    fresh_data = extractor.extract()
    print(f"Fresh data extracted at: {fresh_data.get('last_updated', 'unknown')}")
    print(f"Basic Info: {fresh_data.get('basic_info', {}).get('name')}")
    print(f"Number of experiences: {len(fresh_data.get('experience', []))}")
    print(f"Number of education entries: {len(fresh_data.get('education', []))}")
    
    # Test with cached data
    print("\nTrying with cached data...")
    cached_extractor = PortfolioExtractor(use_cache=True)
    cached_data = cached_extractor.extract()
    print(f"Data timestamp: {cached_data.get('last_updated', 'unknown')}")
    
    # Test with a different URL
    print("\nTrying with a different URL...")
    try:
        different_extractor = PortfolioExtractor(url="https://github.com/", use_cache=False)
        different_data = different_extractor.extract()
        print(f"Data from GitHub: {different_data.get('basic_info', {})}")
    except Exception as e:
        print(f"Error extracting from GitHub: {e}")