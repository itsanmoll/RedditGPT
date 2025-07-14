import os
import requests

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

def get_persona_from_llm(prompt: str):
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_API_URL = os.getenv('GROQ_API_URL', 'https://api.groq.com/openai/v1/chat/completions')
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'llama3-70b-8192',
        'messages': [
            {"role": "user", "content": prompt}
        ],
        'max_tokens': 1024,
        'temperature': 0.7
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error calling Groq LLM API: {e}")
        return "[Error generating persona]" 