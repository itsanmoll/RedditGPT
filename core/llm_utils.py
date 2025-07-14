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
        """Analyze user data to create persona using Groq"""
        
        # Prepare data for analysis
        posts_text = "\n".join([
            f"POST #{i+1}:\nTitle: {post['title']}\nContent: {post['selftext'][:300]}...\nSubreddit: r/{post['subreddit']}\nScore: {post['score']}\nLink: {post['permalink']}\n"
            for i, post in enumerate(user_data['posts'][:10])
        ])
        
        comments_text = "\n".join([
            f"COMMENT #{i+1}:\nText: {comment['body'][:250]}...\nSubreddit: r/{comment['subreddit']}\nScore: {comment['score']}\nLink: {comment['permalink']}\n"
            for i, comment in enumerate(user_data['comments'][:15])
        ])
        
        # Get top subreddits for context
        subreddits = {}
        for post in user_data['posts']:
            subreddit = post['subreddit']
            subreddits[subreddit] = subreddits.get(subreddit, 0) + 1
        for comment in user_data['comments']:
            subreddit = comment['subreddit']
            subreddits[subreddit] = subreddits.get(subreddit, 0) + 1
        
        top_subreddits = sorted(subreddits.items(), key=lambda x: x[1], reverse=True)[:10]
        
        prompt = f"""
You are an expert user persona analyst specializing in social media behavior analysis. Analyze the following Reddit user data and create a comprehensive user persona.

**USER PROFILE:**
- Username: {user_data['user_info']['username']}
- Account Age: {user_data['user_info']['account_age_days']:.0f} days
- Comment Karma: {user_data['user_info']['comment_karma']:,}
- Link Karma: {user_data['user_info']['link_karma']:,}
- Total Karma: {user_data['user_info']['comment_karma'] + user_data['user_info']['link_karma']:,}
- Posts Analyzed: {len(user_data['posts'])}
- Comments Analyzed: {len(user_data['comments'])}

**MOST ACTIVE SUBREDDITS:**
{', '.join([f"r/{sub} ({count})" for sub, count in top_subreddits])}

**RECENT POSTS:**
{posts_text}

**RECENT COMMENTS:**
{comments_text}

**ANALYSIS REQUIREMENTS:**
Create a detailed user persona with the following 8 categories. For each category, provide specific insights with direct citations from the user's posts and comments.

**FORMAT YOUR RESPONSE AS:**

## 1. DEMOGRAPHICS
**Age Range:** [Estimated age with confidence level]
**Location:** [Any location indicators found]
**Occupation/Field:** [Any work/study indicators]
**Citations:** [Specific quotes from posts/comments that support these conclusions]

## 2. INTERESTS & HOBBIES
**Primary Interests:** [List main interests identified]
**Hobbies:** [Recreational activities mentioned]
**Expertise Areas:** [Topics they seem knowledgeable about]
**Citations:** [Specific quotes and post titles that show these interests]

## 3. PERSONALITY TRAITS
**Communication Style:** [How they interact - formal, casual, humorous, etc.]
**Social Behavior:** [Helpful, argumentative, supportive, etc.]
**Emotional Patterns:** [Optimistic, analytical, passionate, etc.]
**Citations:** [Specific examples of their communication style]

## 4. VALUES & BELIEFS
**Core Values:** [What seems important to them]
**Political/Social Views:** [Any political or social stances, if apparent]
**Moral Frameworks:** [Their approach to ethical issues]
**Citations:** [Specific statements that reveal their values]

## 5. TECHNOLOGY USAGE
**Tech Savviness:** [Their comfort level with technology]
**Platform Preferences:** [How they use Reddit vs other platforms]
**Digital Behavior:** [Posting patterns, engagement style]
**Citations:** [Examples of their tech-related posts/comments]

## 6. SOCIAL MEDIA BEHAVIOR
**Engagement Style:** [How they interact with others]
**Content Preference:** [What they post/comment about most]
**Community Participation:** [How active they are in communities]
**Citations:** [Examples of their social interactions]

## 7. GOALS & MOTIVATIONS
**Apparent Goals:** [What they seem to be working toward]
**Motivations:** [What drives their Reddit activity]
**Challenges:** [Problems they're trying to solve]
**Citations:** [Posts/comments that reveal their goals]

## 8. CONFIDENCE ASSESSMENT
**High Confidence Traits:** [Traits with strong evidence]
**Medium Confidence Traits:** [Traits with moderate evidence]
**Low Confidence Traits:** [Traits with limited evidence]

**IMPORTANT:** 
- Always include specific citations (direct quotes) from posts and comments
- Include confidence levels (High/Medium/Low) for each trait
- Provide Reddit links when referencing specific content
- Be objective and evidence-based in your analysis
- If information is not available, state "Not enough data" rather than guessing

Analyze thoroughly and provide detailed insights with strong evidence backing.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert user persona analyst with years of experience in social media behavior analysis. You provide detailed, evidence-based insights with specific citations."
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
            
            analysis_content = response.choices[0].message.content
            
            logger.info(f"✅ Persona analysis completed for user: {user_data['user_info']['username']}")
            
            return {
                'analysis': analysis_content,
                'timestamp': datetime.now().isoformat(),
                'model_used': self.model,
                'stats': {
                    'posts_analyzed': len(user_data['posts']),
                    'comments_analyzed': len(user_data['comments']),
                    'top_subreddits': top_subreddits[:5]
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error analyzing persona: {e}")
            raise Exception(f"Error analyzing persona with Groq: {str(e)}")
    
    def get_model_info(self) -> Dict:
        """Get information about the current model"""
        return {
            'provider': 'Groq',
            'model': self.model,
            'api_key_set': bool(config.GROQ_API_KEY)
        }