import argparse
import os
from reddit_scraper import fetch_user_content
from llm_utils import build_prompt, get_persona_from_llm

def main():
    parser = argparse.ArgumentParser(description="Generate a Reddit user persona using Groq LLM.")
    parser.add_argument('username', help='Reddit username (without /u/)')
    parser.add_argument('--limit', type=int, default=50, help='Number of posts/comments to analyze (default: 50)')
    args = parser.parse_args()

    username = args.username
    limit = args.limit

    print(f"Fetching Reddit data for user: {username}")
    data = fetch_user_content(username, limit=limit)
    if not data['posts'] and not data['comments']:
        print("No data found for user or failed to fetch data.")
        exit(1)

    print("Building prompt and querying Groq LLM...")
    prompt = build_prompt(username, data)
    persona = get_persona_from_llm(prompt)

    os.makedirs('personas', exist_ok=True)
    output_file = os.path.join('personas', f"persona_{username}.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(persona)
    print(f"Persona saved to {output_file}")

if __name__ == "__main__":
    main() 