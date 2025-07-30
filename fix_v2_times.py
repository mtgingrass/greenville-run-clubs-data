#!/usr/bin/env python3
"""
Fix the remaining day names in time strings in run_clubs_v2.json
"""

import json
import re

def clean_time_string(time_str):
    """Remove day names and clean up time strings."""
    clean = time_str
    
    # Remove day names
    days_pattern = r'(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*'
    clean = re.sub(days_pattern, '', clean)
    
    # Remove other patterns
    clean = re.sub(r'Weekdays\s*', '', clean)
    clean = re.sub(r'Mon\s*', '', clean)
    clean = re.sub(r'Wed\s*', '', clean)
    clean = re.sub(r'Sat\s*', '', clean)
    clean = re.sub(r'Monday-Thursday\s*', '', clean)
    
    # Fix any leading dashes or extra spaces
    clean = re.sub(r'^-+\s*', '', clean)
    clean = re.sub(r'\s+', ' ', clean)
    
    return clean.strip()

def fix_meetup_times(clubs):
    """Fix all meetup times in the clubs list."""
    for club in clubs:
        if 'meetups' in club:
            for meetup in club['meetups']:
                if 'time' in meetup:
                    meetup['time'] = clean_time_string(meetup['time'])
    return clubs

def main():
    # Read the v2 file
    with open('run_clubs_v2.json', 'r') as f:
        data = json.load(f)
    
    # Fix the times
    data['run_clubs'] = fix_meetup_times(data['run_clubs'])
    
    # Write back
    with open('run_clubs_v2.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ Fixed time strings in run_clubs_v2.json")

if __name__ == "__main__":
    main()