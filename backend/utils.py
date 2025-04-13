import os
import json
from datetime import datetime

def ensure_dir(directory):
    """Ensure a directory exists, create if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        
def save_results(results, output_dir, filename):
    """Save analysis results to a JSON file"""
    ensure_dir(output_dir)
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2)
        
def load_results(filepath):
    """Load results from a JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)
        
def get_timestamp():
    """Get current timestamp in a readable format"""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S") 