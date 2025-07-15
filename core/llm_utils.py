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
        You are an expert user persona analyst. Analyze the Reddit user data and return ONLY a valid JSON object.

        **USER DATA:**
        Username: {user_data['user_info']['username']}
        Account Age: {user_data['user_info']['account_age_days']:.0f} days
        Total Karma: {user_data['user_info']['comment_karma'] + user_data['user_info']['link_karma']:,}
        Top Subreddits: {[f"r/{sub} ({count})" for sub, count in top_subreddits]}

        **POSTS:**
        {posts_text}

        **COMMENTS:**
        {comments_text}

        **RETURN THIS EXACT JSON STRUCTURE:**
        {{
        "name": "Reddit User {user_data['user_info']['username']}",
        "username": "{user_data['user_info']['username']}",
        "quote": "A memorable quote or statement that represents this user",
        "demographics": {{
            "age": "25-30",
            "occupation": "Software Developer",
            "location": "San Francisco, CA",
            "status": "Single",
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

        CRITICAL INSTRUCTIONS:
        - Return ONLY the JSON object, no markdown, no explanations
        - Use values 0.0-1.0 for personality and motivations
        - Base all analysis on actual evidence from the posts/comments
        - If unsure about demographics, use "Unknown" or reasonable estimates
        - Make the quote representative of the user's communication style
        - Fill all arrays with 3-5 relevant items
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert persona analyst. You MUST return only valid JSON, no markdown, no explanations, just the JSON object."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4000,
                top_p=1,
                stop=None
            )

            content = response.choices[0].message.content.strip()

            # Clean JSON response
            if content.startswith('```json'):
                content = content[7:]
            if content.startswith('```'):
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]

            try:
                persona_json = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}")
                logger.error(f"Raw content: {content}")
                return {
                    'analysis': content,
                    'timestamp': datetime.now().isoformat(),
                    'model_used': self.model,
                    'is_json': False,
                    'error': str(e)
                }

            persona_json['metadata'] = {
                'timestamp': datetime.now().isoformat(),
                'model_used': self.model,
                'posts_analyzed': len(user_data['posts']),
                'comments_analyzed': len(user_data['comments']),
                'top_subreddits': top_subreddits,
                'is_json': True
            }

            logger.info(f"✅ JSON persona analysis completed for: {user_data['user_info']['username']}")
            return persona_json

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