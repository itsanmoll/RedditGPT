import os
import json
from datetime import datetime
from typing import Dict

class FileHandler:
    def __init__(self, output_dir: str = "./data/personas"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_raw_user_data(self, username: str, user_data: Dict):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{username}_raw_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2)
        
        return filepath

    def save_persona(self, username: str, persona_data: Dict, user_data: Dict) -> str:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{username}_persona_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"REDDIT USER PERSONA ANALYSIS\n")
            f.write(f"=" * 50 + "\n\n")
            f.write(f"Username: {username}\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Account Age: {user_data['user_info']['account_age_days']:.0f} days\n")
            f.write(f"Total Karma: {user_data['user_info']['comment_karma'] + user_data['user_info']['link_karma']}\n")
            f.write(f"Posts Analyzed: {len(user_data['posts'])}\n")
            f.write(f"Comments Analyzed: {len(user_data['comments'])}\n\n")
            
            f.write("PERSONA ANALYSIS\n")
            f.write("-" * 30 + "\n\n")
            f.write(persona_data['analysis'])
            
            f.write("\n\n" + "=" * 50 + "\n")
            f.write("DATA SOURCES\n")
            f.write("=" * 50 + "\n\n")
            
            # Recent posts
            f.write("RECENT POSTS:\n")
            for i, post in enumerate(user_data['posts'][:5], 1):
                f.write(f"{i}. {post['title']}\n")
                f.write(f"   r/{post['subreddit']} | Score: {post['score']}\n")
                f.write(f"   {post['permalink']}\n\n")
            
            # Recent comments
            f.write("RECENT COMMENTS:\n")
            for i, comment in enumerate(user_data['comments'][:5], 1):
                f.write(f"{i}. r/{comment['subreddit']} | Score: {comment['score']}\n")
                f.write(f"   {comment['body'][:150]}...\n")
                f.write(f"   {comment['permalink']}\n\n")
        
        return filepath 