#!/usr/bin/env python3
"""
Convert run_clubs.json to run_clubs_v2.json with improved structure.
Main change: meetup_time and meetup_day become an array of meetup objects.
"""

import json
import re
from datetime import datetime

def parse_meetup_days(day_string):
    """Parse meetup day string into individual days."""
    # Handle special cases
    if "Monday-Saturday" in day_string:
        return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    elif "Weekdays" in day_string:
        return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    # Split by comma and clean up
    days = [d.strip() for d in day_string.split(",")]
    return days

def clean_time_string(time_str):
    """Remove day names from time strings."""
    clean = time_str
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
        clean = clean.replace(f"{day} ", "")
    # Also handle special cases
    clean = clean.replace("Weekdays ", "")
    clean = clean.replace("Mon ", "").replace("Wed ", "").replace("Sat ", "")
    clean = clean.replace("Monday-Thursday ", "")
    clean = clean.replace("Wednesday ", "").replace("Saturday ", "")
    return clean.strip()

def parse_meetup_times(time_string, days):
    """Parse meetup time string and match with days."""
    # Handle complex time formats
    meetups = []
    
    # Special cases first
    if "Weekdays 5:30 AM, Saturday 7:00 AM" in time_string:
        # F3/FiA Greenville case
        weekday_times = ["5:30 AM"] * 5  # Mon-Fri
        saturday_time = ["7:00 AM"]
        times = weekday_times + saturday_time
    elif "Mon 6PM, Wed 6AM & 6PM, Sat 7AM" in time_string:
        # Fleet Feet case - need to match days properly
        return [
            {"day": "Monday", "time": "6:00 PM"},
            {"day": "Wednesday", "time": "6:00 AM"},
            {"day": "Wednesday", "time": "6:00 PM"},
            {"day": "Saturday", "time": "7:00 AM"}
        ]
    elif "Saturday 5:30-9:00 AM, Wednesday 5:30-7:00 PM" in time_string:
        # Black Girls RUN! case
        return [
            {"day": "Saturday", "time": "5:30-9:00 AM"},
            {"day": "Wednesday", "time": "5:30-7:00 PM"}
        ]
    elif "Tuesday 6:00 PM, Wednesday 6:00 PM" in time_string:
        # Trailside Trotters case
        return [
            {"day": "Tuesday", "time": "6:00 PM"},
            {"day": "Wednesday", "time": "6:00 PM"}
        ]
    elif "Tuesday 5:15 AM, Wednesday 5:15 AM" in time_string:
        # WR@D case
        return [
            {"day": "Tuesday", "time": "5:15 AM"},
            {"day": "Wednesday", "time": "5:15 AM"}
        ]
    elif "Tuesday 6:30 PM, Wednesday 8:00 AM, Saturday 8:00 AM" in time_string:
        # Tri-Town Run case
        return [
            {"day": "Tuesday", "time": "6:30 PM"},
            {"day": "Wednesday", "time": "8:00 AM"},
            {"day": "Saturday", "time": "8:00 AM"}
        ]
    elif "Tuesday 5:00 AM, Thursday 5:00 AM" in time_string:
        # Greenwood YMCA case
        return [
            {"day": "Tuesday", "time": "5:00 AM"},
            {"day": "Thursday", "time": "5:00 AM"}
        ]
    elif "Saturday 6:30 AM (6:00 AM Summer)" in time_string:
        # Unity Park Long Run case
        return [
            {"day": "Saturday", "time": "6:30 AM", "note": "6:00 AM during summer"}
        ]
    elif "Last Wednesday of Month" in time_string:
        # Maple Bakery Run case
        return [
            {"day": "Wednesday", "time": "6:00 AM", "frequency": "Last Wednesday of month"}
        ]
    elif "," not in time_string and len(days) == 1:
        # Simple single meetup - clean up the time
        clean_time = time_string
        # Remove day name if it's duplicated in the time string
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            clean_time = clean_time.replace(f"{day} ", "")
        return [{"day": days[0], "time": clean_time}]
    else:
        # Try to split times and match with days
        times = [t.strip() for t in time_string.split(",")]
        
        # If equal number of times and days, match them
        if len(times) == len(days):
            for i, day in enumerate(days):
                meetups.append({"day": day, "time": times[i]})
        else:
            # If only one time but multiple days, use same time for all
            if len(times) == 1:
                for day in days:
                    meetups.append({"day": day, "time": times[0]})
            else:
                # Complex case - clean up day names from time strings
                clean_time = time_string
                for day_name in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                    clean_time = clean_time.replace(f"{day_name} ", "")
                for day in days:
                    meetups.append({"day": day, "time": clean_time})
        
        return meetups
    
    # Match times with days and clean up
    for i, day in enumerate(days):
        if i < len(times):
            clean_time = times[i]
            # Remove day names from time strings
            for day_name in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
                clean_time = clean_time.replace(f"{day_name} ", "")
            meetups.append({"day": day, "time": clean_time})
    
    return meetups

def convert_run_club(club):
    """Convert a single run club to the new format."""
    new_club = club.copy()
    
    # Parse meetup information
    days = parse_meetup_days(club.get("meetup_day", ""))
    meetups = parse_meetup_times(club.get("meetup_time", ""), days)
    
    # Remove old fields
    new_club.pop("meetup_time", None)
    new_club.pop("meetup_day", None)
    
    # Add new meetups array
    new_club["meetups"] = meetups
    
    # Add version info
    if "metadata" not in new_club:
        new_club["last_updated"] = new_club.get("last_known_update", datetime.now().strftime("%Y-%m-%d"))
    
    return new_club

def main():
    # Read the original file
    with open('run_clubs.json', 'r') as f:
        data = json.load(f)
    
    # Convert each club
    new_clubs = []
    for club in data["run_clubs"]:
        new_club = convert_run_club(club)
        new_clubs.append(new_club)
    
    # Create new structure with metadata
    new_data = {
        "version": "2.0",
        "generated_at": datetime.now().isoformat(),
        "total_clubs": len(new_clubs),
        "schema": {
            "description": "Greenville area run clubs with structured meetup times",
            "meetup_structure": "Array of {day, time, note?, frequency?} objects"
        },
        "run_clubs": new_clubs
    }
    
    # Write to new file
    with open('run_clubs_v2.json', 'w') as f:
        json.dump(new_data, f, indent=2)
    
    print(f"✅ Converted {len(new_clubs)} run clubs to v2 format")
    print(f"📄 Created run_clubs_v2.json")
    
    # Print some statistics
    multi_meetup_clubs = [c for c in new_clubs if len(c["meetups"]) > 1]
    print(f"📊 {len(multi_meetup_clubs)} clubs have multiple meetup times")

if __name__ == "__main__":
    main()