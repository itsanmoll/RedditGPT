import os
import streamlit as st
import praw
import openai
from datetime import datetime

# --- CONFIGURATION ---
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'RedditPersonaScript/0.1')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# --- REDDIT SCRAPING ---
def fetch_user_content(username: str, limit: int = 50):
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
        st.error(f"Error fetching Reddit data: {e}")
        return {'posts': [], 'comments': []}

# --- LLM PROMPTING ---
def build_prompt(username: str, data):
    prompt = f"""
Given the following Reddit posts and comments from user '{username}', infer their persona. For each trait, cite the supporting post or comment (by quoting a snippet and providing the permalink).

Infer:
- Age group
- Gender (if guessable)
- Interests
- Personality traits
- Writing style
- Possible location

Format:
Trait: Description
Citations:
- [Quote] (permalink)

Reddit Data:
"""
    for post in data['posts']:
        prompt += f"\nPOST: {post['title']}\n{post['body']}\nSubreddit: {post['subreddit']}\nURL: {post['permalink']}\n---"
    for comment in data['comments']:
        prompt += f"\nCOMMENT: {comment['body']}\nSubreddit: {comment['subreddit']}\nURL: {comment['permalink']}\n---"
    return prompt

# --- LLM CALL (OpenAI Example) ---
def get_persona_from_llm(prompt: str):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.7
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"Error calling LLM API: {e}")
        return "[Error generating persona]"

# --- STREAMLIT APP ---
st.set_page_config(page_title="Reddit Persona Generator", page_icon="🤖")
st.title("Reddit Persona Generator 🤖")
st.write("""
Enter a Reddit username to generate a detailed persona using their posts and comments. The app uses OpenAI GPT-3.5 to infer traits and cite supporting content.
""")

with st.form("persona_form"):
    username = st.text_input("Reddit Username", "")
    limit = st.slider("Number of posts/comments to analyze", 10, 100, 50)
    submitted = st.form_submit_button("Generate Persona")

if submitted and username:
    if not (REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET and OPENAI_API_KEY):
        st.error("Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and OPENAI_API_KEY as environment variables.")
    else:
        with st.spinner(f"Fetching Reddit data for user: {username}"):
            data = fetch_user_content(username, limit=limit)
        if not data['posts'] and not data['comments']:
            st.warning("No data found for user or failed to fetch data.")
        else:
            with st.spinner("Building prompt and querying LLM..."):
                prompt = build_prompt(username, data)
                persona = get_persona_from_llm(prompt)
            st.subheader(f"Persona for u/{username}")
            st.code(persona, language="markdown")
            output_filename = f"persona_{username}.txt"
            st.download_button(
                label="Download Persona as .txt",
                data=persona,
                file_name=output_filename,
                mime="text/plain"
            ) 