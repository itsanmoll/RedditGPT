import streamlit as st
import os
from core.config import config
from core.reddit_scraper import RedditScraper
from core.llm_utils import PersonaAnalyzer
from utils.file_handler import FileHandler

# Page config
st.set_page_config(
    page_title="Reddit Persona Analyzer",
    page_icon="🔍",
    layout="wide"
)

def main():
    st.title("🔍 Reddit User Persona Analyzer")
    st.markdown("**BeyondChats AI/LLM Engineer Assignment**")
    
    # Sidebar
    st.sidebar.header("Setup")
    st.sidebar.info("""
    **Required Environment Variables:**
    - REDDIT_CLIENT_ID
    - REDDIT_CLIENT_SECRET  
    - REDDIT_USER_AGENT
    - GROQ_API_KEY ⚡ (Free!)
    """)
    
    # Check config
    try:
        config.validate()
        st.sidebar.success("✅ Configuration valid")
    except ValueError as e:
        st.sidebar.error(f"❌ {e}")
        st.error("Please set up environment variables first!")
        return
    
    # Main interface
    st.header("Analyze Reddit Profile")
    
    # Example URLs
    with st.expander("Example URLs"):
        st.code("https://www.reddit.com/user/kojied/")
        st.code("https://www.reddit.com/user/Hungry-Move-6603/")
    
    # Input
    profile_url = st.text_input(
        "Reddit Profile URL:",
        placeholder="https://www.reddit.com/user/username/"
    )
    
    # Settings
    col1, col2 = st.columns(2)
    with col1:
        posts_limit = st.slider("Posts to analyze", 10, 50, 25)
    with col2:
        comments_limit = st.slider("Comments to analyze", 10, 50, 25)
    
    if st.button("🚀 Analyze Profile", type="primary"):
        if not profile_url:
            st.error("Please enter a Reddit profile URL")
            return
        
        # Initialize services
        scraper = RedditScraper()
        analyzer = PersonaAnalyzer()
        file_handler = FileHandler()
        
        # Extract username
        username = scraper.extract_username(profile_url)
        if not username:
            st.error("Invalid Reddit profile URL")
            return
        
        # Progress
        progress = st.progress(0)
        status = st.empty()
        
        try:
            # Step 1: Scrape data
            status.text("🔍 Scraping Reddit data...")
            progress.progress(25)
            
            config.MAX_POSTS = posts_limit
            config.MAX_COMMENTS = comments_limit
            user_data = scraper.get_user_data(username)
            
            # Step 2: Show summary
            progress.progress(50)
            status.text("📊 Processing data...")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Posts", len(user_data['posts']))
            with col2:
                st.metric("Comments", len(user_data['comments']))
            with col3:
                st.metric("Total Karma", user_data['user_info']['comment_karma'] + user_data['user_info']['link_karma'])
            
            # Step 3: Analyze
            progress.progress(75)
            status.text("🧠 Analyzing persona...")
            
            persona_data = analyzer.analyze_persona(user_data)
            
            # Step 4: Save and display
            progress.progress(100)
            status.text("✅ Complete!")
            
            # Save file
            filepath = file_handler.save_persona(username, persona_data, user_data)
            
            # Display results
            st.header("📋 Persona Analysis")
            st.write(persona_data['analysis'])
            
            # Download button
            with open(filepath, 'r', encoding='utf-8') as f:
                st.download_button(
                    label="📥 Download Report",
                    data=f.read(),
                    file_name=os.path.basename(filepath),
                    mime="text/plain"
                )
            
            # Show sample data
            with st.expander("📝 Sample Posts"):
                for i, post in enumerate(user_data['posts'][:3], 1):
                    st.write(f"**{i}. {post['title']}**")
                    st.write(f"r/{post['subreddit']} | Score: {post['score']}")
                    if post['selftext']:
                        st.write(post['selftext'][:200] + "...")
                    st.divider()
            
            with st.expander("💬 Sample Comments"):
                for i, comment in enumerate(user_data['comments'][:3], 1):
                    st.write(f"**{i}. r/{comment['subreddit']}** (Score: {comment['score']})")
                    st.write(comment['body'][:200] + "...")
                    st.divider()
            
            st.success(f"✅ Analysis saved to: {filepath}")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            progress.progress(0)
            status.text("")

if __name__ == "__main__":
    main()