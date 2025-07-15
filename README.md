# RedditGPT: Reddit User Persona Analyzer

RedditGPT is a Streamlit web app that generates a detailed persona for any Reddit user by analyzing their posts and comments using a Large Language Model (LLM, via Groq API). It provides a visual persona card, supporting evidence, and downloadable reports.

---

## Features
- 🔍 **Analyze any Reddit user's public activity** (posts & comments)
- 🧠 **LLM-powered persona inference** (Groq LLaMA3 or compatible)
- 🎨 **Visual persona card** (Streamlit-native, no HTML/CSS leaks)
- 📊 **Raw JSON data** and supporting evidence
- 📥 **Downloadable persona report**
- 📝 **Sample posts and comments**
- ⚡ **Fast, interactive UI with Streamlit**

---

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd RedditGPT
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
You need API credentials for Reddit and Groq:
- `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`: [Create a Reddit app](https://www.reddit.com/prefs/apps)
- `REDDIT_USER_AGENT`: Any string (e.g. `RedditGPT/0.1`)
- `GROQ_API_KEY`: Your Groq API key ([get one here](https://console.groq.com/))

You can set these in your shell, or create a `.env` file:
```env
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
REDDIT_USER_AGENT=RedditGPT/0.1
GROQ_API_KEY=your_groq_key
```

---

## Running the App

Start the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at [http://localhost:8501](http://localhost:8501).

---

## How to Use
1. **Enter a Reddit profile URL** (e.g. `https://www.reddit.com/user/kojied/`)
2. **Adjust the number of posts/comments to analyze** (sliders)
3. Click **"🚀 Analyze Profile"**
4. View the generated persona card, raw JSON, supporting evidence, and download the report.

---

## Output
- **Persona Card:** Visual summary of the user's inferred traits, motivations, behaviors, and more.
- **Raw JSON:** Expandable section with all persona data.
- **Downloadable Report:** Text file with persona analysis, sample posts/comments, and sources, saved in `data/personas/`.
- **Raw User Data:** Saved as JSON in `data/personas/` for reproducibility.

---

## Troubleshooting
- **Missing environment variables:** The app will show an error in the sidebar if any required API keys are missing.
- **Reddit API errors:** Check your Reddit credentials and rate limits.
- **Groq API errors:** Check your Groq API key and usage limits.
- **No persona generated:** The LLM may occasionally fail to return valid JSON; try again or check your API usage.

---

## Project Structure
```
RedditGPT/
├── app.py                  # Streamlit app entry point
├── core/
│   ├── config.py           # Configuration and env loading
│   ├── reddit_scraper.py   # Reddit scraping logic
│   └── llm_utils.py        # LLM prompt and API calls
├── utils/
│   ├── file_handler.py     # File saving utilities
│   ├── persona_render.py   # Persona card rendering (Streamlit-native)
│   └── validators.py       # Input validation
├── data/
│   └── personas/           # Saved persona reports and raw data
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── tests/                  # (Optional) Unit tests
```

---

## Credits
- Built for the BeyondChats AI/LLM Engineer Assignment
- Powered by [Streamlit](https://streamlit.io/), [PRAW](https://praw.readthedocs.io/), and [Groq LLM API](https://console.groq.com/)

---

## License
MIT License (or specify your own)
