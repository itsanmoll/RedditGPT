# import os
# import praw
# from datetime import datetime

# def fetch_user_content(username: str, limit: int = 50):
#     REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
#     REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
#     REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'RedditPersonaScript/0.1')
#     try:
#         reddit = praw.Reddit(
#             client_id=REDDIT_CLIENT_ID,
#             client_secret=REDDIT_CLIENT_SECRET,
#             user_agent=REDDIT_USER_AGENT
#         )
#         user = reddit.redditor(username)
#         posts = []
#         for submission in user.submissions.new(limit=limit):
#             posts.append({
#                 'type': 'post',
#                 'title': submission.title,
#                 'body': submission.selftext,
#                 'subreddit': str(submission.subreddit),
#                 'url': submission.url,
#                 'permalink': f"https://www.reddit.com{submission.permalink}",
#                 'created_utc': datetime.utcfromtimestamp(submission.created_utc).isoformat()
#             })
#         comments = []
#         for comment in user.comments.new(limit=limit):
#             comments.append({
#                 'type': 'comment',
#                 'body': comment.body,
#                 'subreddit': str(comment.subreddit),
#                 'permalink': f"https://www.reddit.com{comment.permalink}",
#                 'created_utc': datetime.utcfromtimestamp(comment.created_utc).isoformat()
#             })
#         return {'posts': posts, 'comments': comments}
#     except Exception as e:
#         print(f"Error fetching Reddit data: {e}")
#         return {'posts': [], 'comments': []} 

import praw
import re
from typing import Dict, List, Optional
from core.config import config
from datetime import datetime

class RedditScraper:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            user_agent=config.REDDIT_USER_AGENT
        )
    
    def extract_username(self, url: str) -> Optional[str]:
        patterns = [
            r'reddit\.com/u/([^/\?]+)',
            r'reddit\.com/user/([^/\?]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_user_data(self, username: str) -> Dict:
        try:
            user = self.reddit.redditor(username)
            
            # Get user info
            user_info = {
                'username': username,
                'created_utc': user.created_utc,
                'comment_karma': user.comment_karma,
                'link_karma': user.link_karma,
                'account_age_days': (datetime.now().timestamp() - user.created_utc) / 86400
            }
            
            # Get posts
            posts = []
            for submission in user.submissions.new(limit=config.MAX_POSTS):
                posts.append({
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'subreddit': str(submission.subreddit),
                    'score': submission.score,
                    'permalink': f"https://reddit.com{submission.permalink}",
                    'created_utc': submission.created_utc
                })
            
            # Get comments
            comments = []
            for comment in user.comments.new(limit=config.MAX_COMMENTS):
                if hasattr(comment, 'body') and comment.body != '[deleted]':
                    comments.append({
                        'body': comment.body,
                        'subreddit': str(comment.subreddit),
                        'score': comment.score,
                        'permalink': f"https://reddit.com{comment.permalink}",
                        'created_utc': comment.created_utc
                    })
            
            return {
                'user_info': user_info,
                'posts': posts,
                'comments': comments
            }
            
        except Exception as e:
            raise Exception(f"Error scraping Reddit data: {str(e)}")