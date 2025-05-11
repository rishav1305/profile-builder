import logging
import json
import sys
from profile_builder import ProfileBuilder

# Force logging to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(sys.stdout)])

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_sample_portfolio():
    """Load sample portfolio data for testing."""
    # This is a sample portfolio in JSON format
    sample_data = {
        "basic_info": {
            "name": "Alex Johnson",
            "title": "Data Engineer & ML Specialist"
        },
        "about": {
            "summary": "Data professional with expertise in building scalable data pipelines and ML solutions",
            "interests": ["Machine Learning", "Cloud Architecture", "Data Analytics"]
        },
        "experience": [
            {
                "title": "Senior Data Engineer",
                "company": "Tech Innovations Inc.",
                "duration": "2021-Present",
                "description": "Led development of cloud-based ETL pipelines processing 5TB of data daily"
            },
            {
                "title": "Data Scientist",
                "company": "Data Insights Corp",
                "duration": "2018-2021",
                "description": "Implemented ML models for customer segmentation improving conversion by 23%"
            },
            {
                "title": "Software Engineer",
                "company": "WebSolutions Ltd",
                "duration": "2016-2018",
                "description": "Developed backend services for data processing applications"
            }
        ],
        "education": [
            {
                "degree": "MS in Computer Science",
                "institution": "Stanford University",
                "year": "2016"
            },
            {
                "degree": "BS in Computer Engineering",
                "institution": "University of California, Berkeley",
                "year": "2014"
            }
        ],
        "skills": {
            "technical": [
                "Python", "SQL", "Apache Spark", "TensorFlow", 
                "AWS", "Kubernetes", "Docker", "Airflow", 
                "Kafka", "MongoDB", "PostgreSQL", "Git",
                "Django", "Flask", "React", "JavaScript"
            ],
            "soft": [
                "Project Management", "Team Leadership", "Communication",
                "Problem Solving", "Agile Development"
            ]
        },
        "projects": [
            {
                "name": "Healthcare Predictive Analytics Platform",
                "duration": "8 months",
                "technologies": ["Python", "TensorFlow", "AWS", "Docker", "MongoDB"],
                "role": "Lead Data Scientist",
                "achievements": "Reduced patient readmission rates by 15% through predictive modeling; Implemented real-time monitoring system for patient health indicators"
            },
            {
                "name": "E-commerce Recommendation Engine",
                "duration": "6 months",
                "technologies": ["Python", "Apache Spark", "PostgreSQL", "AWS"],
                "role": "Data Engineer",
                "achievements": "Increased average order value by 18% with personalized recommendations; Scaled system to handle 1M+ daily users"
            }
        ]
    }
    return sample_data

def test_profile_builder_with_deepseek():
    """Test the ProfileBuilder with deepseek-r1 model integration."""
    print("\n=== Testing ProfileBuilder with deepseek-r1 integration ===\n")
    
    try:
        # Load sample portfolio data
        print("Loading sample portfolio data...")
        portfolio_data = load_sample_portfolio()
        
        # Initialize ProfileBuilder for Upwork with the sample data
        print("Initializing ProfileBuilder with deepseek-r1...")
        profile_builder = ProfileBuilder(platform="upwork", portfolio_data=portfolio_data, model="deepseek-r1")
        
        # Generate title directly
        print("\nTesting title generation...")
        title = profile_builder._generate_title_for_upwork()
        print(f"Generated title: {title}")
        
        # Generate overview directly
        print("\nTesting overview generation...")
        overview = profile_builder._generate_overview_for_upwork()
        print(f"Generated overview: {overview}")
        
        # Select skills directly
        print("\nTesting skill selection...")
        skills = profile_builder._select_skills_for_upwork()
        print(f"Selected skills: {skills}")
        
        # Suggest hourly rate directly
        print("\nTesting hourly rate suggestion...")
        rate = profile_builder._suggest_hourly_rate()
        print(f"Suggested hourly rate: ${rate} per hour")
        
        print("\n=== Individual tests completed successfully ===\n")
        
        # Try building the full profile
        print("Building complete Upwork profile with deepseek-r1 model...\n")
        result = profile_builder.build()
        
        # Display the results
        print(f"\n=== Generated Title ===\n{result['title']}")
        print(f"\n=== Generated Overview ===\n{result['overview']}")
        print(f"\n=== Selected Skills ===\n{', '.join(result['skills'])}")
        print(f"\n=== Suggested Hourly Rate ===\n${result['hourly_rate']} per hour")
        
        print("\n=== Full profile build completed successfully ===\n")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        print("\n=== Test failed ===\n")

if __name__ == "__main__":
    test_profile_builder_with_deepseek()
