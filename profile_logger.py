import os
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProfileLogger:
    """Class to handle logging of profile updates for dashboard display."""
    
    def __init__(self, log_dir="logs"):
        """Initialize the profile logger with a directory for storing logs."""
        self.log_dir = log_dir
        self._ensure_log_dir_exists()
    
    def _ensure_log_dir_exists(self):
        """Create the log directory if it doesn't exist."""
        os.makedirs(self.log_dir, exist_ok=True)
    
    def log_profile_update(self, platform, profile_url, changes):
        """
        Log a profile update to the appropriate log file.
        
        Args:
            platform (str): The platform that was updated (e.g., linkedin, upwork)
            profile_url (str): URL of the updated profile
            changes (dict): Dictionary containing the changes that were made
            
        Returns:
            bool: True if logging was successful, False otherwise
        """
        try:
            # Ensure timestamp exists
            if "timestamp" not in changes:
                changes["timestamp"] = datetime.now().isoformat()
            
            # Add platform and URL
            changes["platform"] = platform
            changes["profile_url"] = profile_url
            
            # Create log file name based on platform and date
            date_str = datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(self.log_dir, f"{platform}_updates.json")
            
            # Read existing logs if the file exists
            entries = []
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    try:
                        entries = json.load(f)
                    except json.JSONDecodeError:
                        logging.warning(f"Failed to parse {log_file}, creating new log file")
                        entries = []
            
            # Append new entry
            entries.append(changes)
            
            # Write updated logs
            with open(log_file, 'w') as f:
                json.dump(entries, f, indent=2)
            
            logging.info(f"Successfully logged {platform} profile update")
            return True
            
        except Exception as e:
            logging.error(f"Error logging profile update: {str(e)}")
            return False
    
    def get_recent_logs(self, platform=None, limit=10):
        """
        Get recent logs for the specified platform, or all platforms if None.
        
        Args:
            platform (str, optional): Platform to filter logs by
            limit (int): Maximum number of log entries to return
            
        Returns:
            list: Recent log entries
        """
        all_logs = []
        
        try:
            # Get all log files if no platform specified, otherwise just that platform's log
            log_files = []
            if platform:
                log_file = os.path.join(self.log_dir, f"{platform}_updates.json")
                if os.path.exists(log_file):
                    log_files.append(log_file)
            else:
                for filename in os.listdir(self.log_dir):
                    if filename.endswith("_updates.json"):
                        log_files.append(os.path.join(self.log_dir, filename))
            
            # Read all log files
            for log_file in log_files:
                try:
                    with open(log_file, 'r') as f:
                        logs = json.load(f)
                        all_logs.extend(logs)
                except Exception as e:
                    logging.warning(f"Error reading log file {log_file}: {str(e)}")
            
            # Sort logs by timestamp (newest first)
            all_logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            
            # Return only the specified number of logs
            return all_logs[:limit]
            
        except Exception as e:
            logging.error(f"Error retrieving logs: {str(e)}")
            return []
