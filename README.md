# Reddit Persona Builder

This project generates a detailed persona for any Reddit user by analyzing their posts and comments using an LLM (Groq LLaMA3 via API).

## Project Structure
```
reddit-persona-builder/
├── reddit_persona.py              # Main script to run everything
├── llm_utils.py                   # Handles LLM prompt and API calls (Groq)
├── reddit_scraper.py              # Contains Reddit scraping logic using PRAW
├── personas/
│   ├── persona_kojied.txt         # Sample persona output
│   └── persona_Hungry.txt
├── tests/
│   └── test_basic.py              # (Optional: simple unit tests if time permits)
├── requirements.txt               # All dependencies
├── README.md                      # Setup + usage instructions
├── .env                           # (Optional: to store API keys)
└── .gitignore                     # Ignore .env, __pycache__, etc.
```

## Setup
1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your `.env` file or environment variables:**
   - `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`: [Create a Reddit app](https://www.reddit.com/prefs/apps)
   - `REDDIT_USER_AGENT`: Any string (e.g. `RedditPersonaScript/0.1`)
   - `GROQ_API_KEY`: Your Groq API key
   - `GROQ_API_URL`: (Optional, default is `https://api.groq.com/openai/v1/chat/completions`)

   Example `.env`:
   ```env
   REDDIT_CLIENT_ID=your_id
   REDDIT_CLIENT_SECRET=your_secret
   REDDIT_USER_AGENT=RedditPersonaScript/0.1
   GROQ_API_KEY=your_groq_key
   # GROQ_API_URL=https://api.groq.com/openai/v1/chat/completions
   ```

   To load the .env automatically, use `python-dotenv` or export variables manually.

## Usage
```bash
python reddit_persona.py <reddit_username> [--limit 50]
```
Example:
```bash
python reddit_persona.py kojied --limit 30
```

## Output
- The script creates a file `personas/persona_<username>.txt` with the inferred persona and citations.

## Sample Output
```
Trait: Interests: Technology, AI, and gaming
Citations:
- "I just built a new gaming PC..." (https://www.reddit.com/r/buildapc/comments/xyz123)
- "Anyone else excited about LLaMA3?" (https://www.reddit.com/r/MachineLearning/comments/abc456)

Trait: Writing Style: Informal, humorous
Citations:
- "lol, that cracked me up!" (https://www.reddit.com/r/funny/comments/def789)
...
```

## Notes
- If the script fails to fetch data, check your Reddit API credentials and rate limits.
- For LLM API errors, check your Groq API key and usage limits.
- You can adapt the script to use other LLM providers by modifying `llm_utils.py`.
- The Streamlit app is available as `reddit_persona_app.py` for interactive use.
