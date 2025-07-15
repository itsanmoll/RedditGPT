from groq import Groq
from typing import Dict
import json
from core.config import config
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PersonaAnalyzer:
    def __init__(self):
        try:
            self.client = Groq(api_key=config.GROQ_API_KEY)
            self.model = config.GROQ_MODEL
            logger.info("✅ Groq client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Groq client: {e}")
            raise Exception(f"Failed to initialize Groq client: {str(e)}")

    def analyze_persona(self, user_data: Dict) -> Dict:
        """Analyze user data and return structured JSON persona"""

        # Prepare data for analysis
        posts_text = "\n".join([
            f"POST #{i+1}: {post['title']} (r/{post['subreddit']}, {post['score']} upvotes)\n"
            f"Content: {post['selftext'][:200]}...\n"
            for i, post in enumerate(user_data['posts'][:10])
        ])

        comments_text = "\n".join([
            f"COMMENT #{i+1}: {comment['body'][:200]}... (r/{comment['subreddit']}, {comment['score']} upvotes)\n"
            for i, comment in enumerate(user_data['comments'][:15])
        ])

        # Get top subreddits
        subreddits = {}
        for post in user_data['posts']:
            subreddits[post['subreddit']] = subreddits.get(post['subreddit'], 0) + 1
        for comment in user_data['comments']:
            subreddits[comment['subreddit']] = subreddits.get(comment['subreddit'], 0) + 1

        top_subreddits = sorted(subreddits.items(), key=lambda x: x[1], reverse=True)[:5]

        prompt = f"""
    You are a JSON API that analyzes Reddit users. Return ONLY valid JSON with NO markdown, NO explanations, NO text before or after.

    USER DATA:
    Username: {user_data['user_info']['username']}
    Account Age: {user_data['user_info']['account_age_days']:.0f} days
    Total Karma: {user_data['user_info']['comment_karma'] + user_data['user_info']['link_karma']:,}
    Top Subreddits: {[f"r/{sub} ({count})" for sub, count in top_subreddits]}

    POSTS:
    {posts_text}

    COMMENTS:
    {comments_text}

    {{
    "name": "Reddit User {user_data['user_info']['username']}",
    "username": "{user_data['user_info']['username']}",
    "quote": "A memorable quote that represents this user",
    "demographics": {{
        "age": "25-30",
        "occupation": "Software Developer",
        "location": "Unknown",
        "status": "Unknown",
        "tier": "Active User",
        "archetype": "The Helper"
    }},
    "personality": {{
        "Helpful": 0.8,
        "Analytical": 0.7,
        "Humorous": 0.6,
        "Technical": 0.9,
        "Social": 0.5
    }},
    "motivations": {{
        "Learning": 0.9,
        "Entertainment": 0.7,
        "Social Connection": 0.6,
        "Problem Solving": 0.8,
        "Information Sharing": 0.7,
        "Career Growth": 0.6
    }},
    "behaviors": [
        "Frequently helps others solve technical problems",
        "Shares detailed explanations and code examples",
        "Active in programming and tech communities"
    ],
    "frustrations": [
        "Repetitive questions that could be easily googled",
        "Poor code documentation in projects",
        "Time management between work and learning"
    ],
    "goals": [
        "Become a senior developer within 2 years",
        "Build a personal project that gains traction",
        "Contribute to open source projects"
    ],
    "interests": [
        "Programming", "Technology", "Gaming", "Science Fiction", "Productivity"
    ],
    "confidence_level": {{
        "demographics": "Medium",
        "personality": "High",
        "motivations": "High"
    }},
    "citations": [
        "Quote from post/comment that supports analysis",
        "Another supporting quote",
        "Third piece of evidence"
    ]
    }}
    """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a JSON API. Return ONLY valid JSON. No markdown, no explanations, no text before or after the JSON object."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Lower temperature for consistent JSON
                max_tokens=3000,
                top_p=0.9,
                stop=None
            )

            content = response.choices[0].message.content.strip()
            logger.info(f"Raw LLM response: {content[:100]}...")

            # Aggressive JSON cleaning
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            # Find JSON bounds
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                content = content[start_idx:end_idx]

            # Multiple JSON parsing attempts
            for attempt in range(3):
                try:
                    persona_json = json.loads(content)
                    logger.info(f"✅ JSON parsed successfully on attempt {attempt + 1}")
                    
                    # Add metadata
                    persona_json['metadata'] = {
                        'timestamp': datetime.now().isoformat(),
                        'model_used': self.model,
                        'posts_analyzed': len(user_data['posts']),
                        'comments_analyzed': len(user_data['comments']),
                        'top_subreddits': top_subreddits,
                        'is_json': True
                    }
                    
                    return persona_json
                    
                except json.JSONDecodeError as e:
                    logger.warning(f"JSON parsing attempt {attempt + 1} failed: {e}")
                    
                    if attempt == 0:
                        # Fix trailing commas
                        content = content.replace(',}', '}').replace(',]', ']')
                    elif attempt == 1:
                        # Fix quotes
                        content = content.replace("'", '"')
                    elif attempt == 2:
                        # Last attempt - raise error
                        logger.error(f"❌ All JSON parsing attempts failed")
                        logger.error(f"❌ Final content: {content}")
                        raise Exception(f"Failed to parse JSON after 3 attempts. Raw content: {content[:200]}...")

        except Exception as e:
            logger.error(f"❌ Error analyzing persona: {e}")
            raise Exception(f"Error analyzing persona: {str(e)}")
        
    def get_model_info(self) -> Dict:
        """Get information about the current model"""
        return {
            'provider': 'Groq',
            'model': self.model,
            'api_key_set': bool(config.GROQ_API_KEY)
        }