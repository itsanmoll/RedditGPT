import os
import praw
from datetime import datetime

def fetch_user_content(username: str, limit: int = 50):
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'RedditPersonaScript/0.1')
    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )
        user = reddit.redditor(username)
        posts = []
        for submission in user.submissions.new(limit=limit):
            posts.append({
                'type': 'post',
                'title': submission.title,
                'body': submission.selftext,
                'subreddit': str(submission.subreddit),
                'url': submission.url,
                'permalink': f"https://www.reddit.com{submission.permalink}",
                'created_utc': datetime.utcfromtimestamp(submission.created_utc).isoformat()
            })
        comments = []
        for comment in user.comments.new(limit=limit):
            comments.append({
                'type': 'comment',
                'body': comment.body,
                'subreddit': str(comment.subreddit),
                'permalink': f"https://www.reddit.com{comment.permalink}",
                'created_utc': datetime.utcfromtimestamp(comment.created_utc).isoformat()
            })
        return {'posts': posts, 'comments': comments}
    except Exception as e:
        print(f"Error fetching Reddit data: {e}")
        return {'posts': [], 'comments': []} 