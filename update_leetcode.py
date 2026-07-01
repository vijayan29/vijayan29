#!/usr/bin/env python3
"""
Script to update LeetCode stats in README.md
Fetches solved problems from LeetCode API and updates the README automatically
"""

import requests
import re
import os
import sys

LEETCODE_USERNAME = 'VIJAYAN_G'
README_PATH = 'README.md'

def fetch_leetcode_stats(username):
    """
    Fetch LeetCode stats using the unofficial LeetCode stats API
    Returns dict with total_solved, total_questions, easy, medium, hard
    """
    url = f'https://leetcode-stats-api.herokuapp.com/{username}'
    
    try:
        print(f"📊 Fetching LeetCode stats for: {username}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        stats = {
            'total_solved': data.get('totalSolved', 0),
            'total_questions': data.get('totalQuestions', 0),
            'easy': data.get('easySolved', 0),
            'medium': data.get('mediumSolved', 0),
            'hard': data.get('hardSolved', 0)
        }
        
        print(f"✅ Successfully fetched stats!")
        print(f"   Total Solved: {stats['total_solved']}/{stats['total_questions']}")
        print(f"   Easy: {stats['easy']} | Medium: {stats['medium']} | Hard: {stats['hard']}")
        
        return stats
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching LeetCode stats: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"❌ Error parsing response: {e}")
        return None


def update_readme(stats):
    """
    Update README.md with the latest LeetCode stats
    Replaces content between LEETCODE_SOLVED markers
    """
    
    if not stats:
        print("⚠️  Skipping README update - no stats available")
        return False
    
    # Check if README exists
    if not os.path.exists(README_PATH):
        print(f"❌ README file not found at {README_PATH}")
        return False
    
    try:
        # Read current README
        with open(README_PATH, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Create the new stats line
        new_stat = f"**Solved: {stats['total_solved']} / {stats['total_questions']} problems** (Easy: {stats['easy']} | Medium: {stats['medium']} | Hard: {stats['hard']})"
        
        # Replace content between markers using regex
        pattern = r'<!-- LEETCODE_SOLVED_START -->.*?<!-- LEETCODE_SOLVED_END -->'
        replacement = f'<!-- LEETCODE_SOLVED_START -->\n{new_stat}\n<!-- LEETCODE_SOLVED_END -->'
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # Check if anything changed
        if new_content == content:
            print("⚠️  No markers found in README - make sure to add them!")
            print("   Add this to your README:")
            print("   <!-- LEETCODE_SOLVED_START -->")
            print("   <!-- LEETCODE_SOLVED_END -->")
            return False
        
        # Write updated README
        with open(README_PATH, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f"✅ README.md updated successfully!")
        return True
        
    except IOError as e:
        print(f"❌ Error reading/writing README: {e}")
        return False


def main():
    """Main function"""
    print("=" * 50)
    print("🚀 LeetCode README Stats Updater")
    print("=" * 50)
    print()
    
    # Fetch stats
    stats = fetch_leetcode_stats(LEETCODE_USERNAME)
    
    if not stats:
        print("Failed to fetch LeetCode stats")
        sys.exit(1)
    
    print()
    
    # Update README
    if update_readme(stats):
        print()
        print("=" * 50)
        print("✨ Update completed successfully!")
        print("=" * 50)
        sys.exit(0)
    else:
        print()
        print("=" * 50)
        print("❌ Failed to update README")
        print("=" * 50)
        sys.exit(1)


if __name__ == '__main__':
    main()
