#!/usr/bin/env python3
"""
Generate a summary report of the run_clubs_v2.json structure
"""

import json
from collections import defaultdict

def analyze_v2_structure():
    with open('run_clubs_v2.json', 'r') as f:
        data = json.load(f)
    
    clubs = data['run_clubs']
    
    # Statistics
    total_clubs = len(clubs)
    total_meetups = sum(len(club['meetups']) for club in clubs)
    multi_meetup_clubs = [c for c in clubs if len(c['meetups']) > 1]
    
    # Group by meetup count
    meetup_counts = defaultdict(int)
    for club in clubs:
        meetup_counts[len(club['meetups'])] += 1
    
    # Find clubs with special meetup properties
    clubs_with_notes = []
    clubs_with_frequency = []
    
    for club in clubs:
        for meetup in club['meetups']:
            if 'note' in meetup:
                clubs_with_notes.append((club['name'], meetup))
            if 'frequency' in meetup:
                clubs_with_frequency.append((club['name'], meetup))
    
    # Print report
    print(f"📊 Run Clubs v2 Structure Summary")
    print(f"{'='*50}")
    print(f"Total clubs: {total_clubs}")
    print(f"Total meetup times: {total_meetups}")
    print(f"Average meetups per club: {total_meetups/total_clubs:.1f}")
    print(f"\n📅 Meetup Distribution:")
    for count, num_clubs in sorted(meetup_counts.items()):
        print(f"  {count} meetup(s): {num_clubs} clubs")
    
    print(f"\n🏃 Clubs with Multiple Meetups ({len(multi_meetup_clubs)}):")
    for club in multi_meetup_clubs:
        print(f"  - {club['name']} ({len(club['meetups'])} meetups)")
        for meetup in club['meetups']:
            note = f" [{meetup.get('note', '')}]" if 'note' in meetup else ""
            freq = f" ({meetup.get('frequency', '')})" if 'frequency' in meetup else ""
            print(f"    • {meetup['day']} at {meetup['time']}{note}{freq}")
    
    print(f"\n📝 Special Cases:")
    print(f"  - Clubs with notes: {len(clubs_with_notes)}")
    for name, meetup in clubs_with_notes[:3]:  # Show first 3
        print(f"    • {name}: {meetup['note']}")
    
    print(f"  - Clubs with frequency: {len(clubs_with_frequency)}")
    for name, meetup in clubs_with_frequency:
        print(f"    • {name}: {meetup['frequency']}")

if __name__ == "__main__":
    analyze_v2_structure()