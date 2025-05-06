import requests
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PortfolioExtractor:
    """
    Class to extract professional information from a portfolio website.
    Currently supports extraction from rishavchatterjee.vercel.app
    """
    
    def __init__(self, url="https://rishavchatterjee.vercel.app/"):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract(self):
        """Extract all relevant information from the portfolio website."""
        logging.info(f"Extracting data from {self.url}")
        
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract each section of information
            basic_info = self._extract_basic_info(soup)
            experience = self._extract_experience(soup)
            education = self._extract_education(soup)
            skills = self._extract_skills(soup)
            about = self._extract_about(soup)
            testimonials = self._extract_testimonials(soup)
            
            # Combine all sections into a single portfolio data object
            portfolio_data = {
                'basic_info': basic_info,
                'about': about,
                'experience': experience,
                'education': education,
                'skills': skills,
                'testimonials': testimonials
            }
            
            logging.info("Portfolio data extracted successfully")
            return portfolio_data
            
        except Exception as e:
            logging.error(f"Error extracting portfolio data: {str(e)}")
            raise
    
    def _extract_basic_info(self, soup):
        """Extract basic personal information."""
        try:
            name = "Rishav Chatterjee"  # Hardcoded based on the portfolio
            email = "rishavchatterjee2024@gmail.com"
            
            # This is a simple extraction - in a real implementation, you'd
            # need more robust parsing logic specific to the site structure
            return {
                'name': name,
                'email': email,
                'title': "Technology Leader",
                'location': "India"
            }
        except Exception as e:
            logging.warning(f"Error extracting basic info: {str(e)}")
            return {}
    
    def _extract_experience(self, soup):
        """Extract professional experience."""
        try:
            # In a real implementation, this would parse the HTML structure
            # For the POC, we'll use the known data
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
        except Exception as e:
            logging.warning(f"Error extracting experience: {str(e)}")
            return []
    
    def _extract_education(self, soup):
        """Extract education information."""
        try:
            return [
                {
                    'institution': 'Delhi Technological University (DTU)',
                    'degree': 'Bachelor\'s Degree',
                    'field': 'Environmental Engineering',
                    'duration': 'Aug 2014 - May 2018',
                    'location': 'Rohini, Delhi'
                }
            ]
        except Exception as e:
            logging.warning(f"Error extracting education: {str(e)}")
            return []
    
    def _extract_skills(self, soup):
        """Extract professional skills."""
        try:
            return {
                'technical': [
                    'SQL', 'Python', 'Data Warehouse', 'ETL Tools',
                    'Cloud Services', 'Analytical Tools', 'Project Management',
                    'Big Data Tools'
                ],
                'soft': ['Communication', 'Leadership', 'Problem Solving']
            }
        except Exception as e:
            logging.warning(f"Error extracting skills: {str(e)}")
            return {}
    
    def _extract_about(self, soup):
        """Extract about me information."""
        try:
            return {
                'summary': "I help companies turn complex datasets into clear, actionable insights through advanced data modeling and visualization. With experience across top firms, I build scalable, interactive dashboards and analytics solutions—leveraging AI tools to boost productivity and drive smarter, data-informed decisions.",
                'highlights': [
                    'Technology Leader with expertise in engineering scalable cloud-based solutions',
                    'Experience with AI to boost productivity and drive innovation',
                    'Specializes in designing scalable data solutions that align tech with business goals'
                ]
            }
        except Exception as e:
            logging.warning(f"Error extracting about: {str(e)}")
            return {}
    
    def _extract_testimonials(self, soup):
        """Extract testimonials."""
        try:
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
        except Exception as e:
            logging.warning(f"Error extracting testimonials: {str(e)}")
            return []

if __name__ == "__main__":
    # Test the extractor
    extractor = PortfolioExtractor()
    data = extractor.extract()
    print(data)