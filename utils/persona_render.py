import streamlit as st
import json
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any
import base64
from io import BytesIO

class PersonaRenderer:
    def __init__(self):
        self.colors = {
            'orange': '#FF8C42',
            'dark_gray': '#2C3E50',
            'light_gray': '#BDC3C7',
            'red': '#E74C3C',
            'white': '#FFFFFF'
        }
    
    def render_lucas_style_persona(self, persona: Dict[str, Any]):
        """Render a Lucas Mellor style persona card"""
        
        # Custom CSS for Lucas-style layout
        st.markdown("""
        <style>
        .lucas-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            overflow: hidden;
            margin: 20px 0;
        }
        
        .lucas-header {
            background: linear-gradient(135deg, #FF8C42 0%, #FF6B35 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .lucas-name {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            text-decoration: underline;
            text-decoration-color: white;
            text-decoration-thickness: 3px;
        }
        
        .lucas-username {
            font-size: 1.2rem;
            opacity: 0.9;
            margin: 10px 0;
        }
        
        .lucas-content {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 30px;
            padding: 30px;
            background: white;
        }
        
        .lucas-section {
            background: white;
        }
        
        .lucas-section h3 {
            color: #FF8C42;
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 15px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .lucas-demo-item {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            padding: 5px 0;
            border-bottom: 1px solid #ECF0F1;
        }
        
        .lucas-demo-label {
            font-weight: 600;
            color: #2C3E50;
            text-transform: uppercase;
            font-size: 0.9rem;
        }
        
        .lucas-demo-value {
            color: #34495E;
            font-weight: 400;
        }
        
        .lucas-trait-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 10px 0;
        }
        
        .lucas-trait-name {
            font-weight: 600;
            color: #2C3E50;
            min-width: 100px;
        }
        
        .lucas-bar-container {
            flex: 1;
            height: 8px;
            background: #ECF0F1;
            border-radius: 4px;
            margin: 0 10px;
            overflow: hidden;
        }
        
        .lucas-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #2C3E50 0%, #34495E 100%);
            border-radius: 4px;
            transition: width 0.3s ease;
        }
        
        .lucas-personality-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin: 20px 0;
        }
        
        .lucas-personality-item {
            background: #BDC3C7;
            padding: 8px 15px;
            border-radius: 20px;
            text-align: center;
            font-weight: 600;
            color: white;
            font-size: 0.9rem;
        }
        
        .lucas-list-item {
            margin: 10px 0;
            padding-left: 15px;
            position: relative;
            color: #2C3E50;
            line-height: 1.4;
        }
        
        .lucas-list-item:before {
            content: "•";
            position: absolute;
            left: 0;
            color: #FF8C42;
            font-weight: bold;
        }
        
        .lucas-quote {
            background: #E74C3C;
            color: white;
            padding: 25px;
            border-radius: 0 0 15px 15px;
            text-align: center;
            font-size: 1.1rem;
            font-style: italic;
            font-weight: 500;
            margin-top: 20px;
        }
        
        .lucas-motivations {
            margin: 20px 0;
        }
        
        .lucas-motivation-item {
            display: flex;
            align-items: center;
            margin: 12px 0;
        }
        
        .lucas-motivation-label {
            min-width: 120px;
            font-weight: 600;
            color: #2C3E50;
            font-size: 0.9rem;
            text-transform: uppercase;
        }
        
        .lucas-motivation-bar {
            flex: 1;
            height: 20px;
            background: #ECF0F1;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }
        
        .lucas-motivation-fill {
            height: 100%;
            background: linear-gradient(90deg, #2C3E50 0%, #34495E 100%);
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Main container
        st.markdown('<div class="lucas-container">', unsafe_allow_html=True)
        
        # Header
        name = persona.get('name', 'Unknown User')
        username = persona.get('username', 'unknown')
        
        st.markdown(f"""
        <div class="lucas-header">
            <h1 class="lucas-name">{name}</h1>
            <p class="lucas-username">@{username}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Content grid
        st.markdown('<div class="lucas-content">', unsafe_allow_html=True)
        
        # Column 1: Demographics + Personality + Motivations
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Demographics
            st.markdown('<div class="lucas-section">', unsafe_allow_html=True)
            demo = persona.get('demographics', {})
            
            demo_html = """
            <div class="lucas-demo-item">
                <span class="lucas-demo-label">AGE</span>
                <span class="lucas-demo-value">{}</span>
            </div>
            <div class="lucas-demo-item">
                <span class="lucas-demo-label">OCCUPATION</span>
                <span class="lucas-demo-value">{}</span>
            </div>
            <div class="lucas-demo-item">
                <span class="lucas-demo-label">STATUS</span>
                <span class="lucas-demo-value">{}</span>
            </div>
            <div class="lucas-demo-item">
                <span class="lucas-demo-label">LOCATION</span>
                <span class="lucas-demo-value">{}</span>
            </div>
            <div class="lucas-demo-item">
                <span class="lucas-demo-label">TIER</span>
                <span class="lucas-demo-value">{}</span>
            </div>
            <div class="lucas-demo-item">
                <span class="lucas-demo-label">ARCHETYPE</span>
                <span class="lucas-demo-value">{}</span>
            </div>
            """.format(
                demo.get('age', 'Unknown'),
                demo.get('occupation', 'Unknown'),
                demo.get('status', 'Unknown'),
                demo.get('location', 'Unknown'),
                demo.get('tier', 'Unknown'),
                demo.get('archetype', 'Unknown')
            )
            
            st.markdown(demo_html, unsafe_allow_html=True)
            
            # Personality traits as grid
            st.markdown('<h3>PERSONALITY</h3>', unsafe_allow_html=True)
            personality = persona.get('personality', {})
            
            if personality:
                traits_html = '<div class="lucas-personality-grid">'
                for trait, score in list(personality.items())[:4]:  # Show top 4 traits
                    traits_html += f'<div class="lucas-personality-item">{trait}</div>'
                traits_html += '</div>'
                st.markdown(traits_html, unsafe_allow_html=True)
            
            # Motivations
            st.markdown('<h3>MOTIVATIONS</h3>', unsafe_allow_html=True)
            motivations = persona.get('motivations', {})
            
            if motivations:
                motivations_html = '<div class="lucas-motivations">'
                for motivation, score in motivations.items():
                    width_percent = int(score * 100)
                    motivations_html += f"""
                    <div class="lucas-motivation-item">
                        <div class="lucas-motivation-label">{motivation}</div>
                        <div class="lucas-motivation-bar">
                            <div class="lucas-motivation-fill" style="width: {width_percent}%;"></div>
                        </div>
                    </div>
                    """
                motivations_html += '</div>'
                st.markdown(motivations_html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Behavior & Habits
            st.markdown('<div class="lucas-section">', unsafe_allow_html=True)
            st.markdown('<h3>BEHAVIOUR & HABITS</h3>', unsafe_allow_html=True)
            
            behaviors = persona.get('behaviors', [])
            behaviors_html = ""
            for behavior in behaviors:
                behaviors_html += f'<div class="lucas-list-item">{behavior}</div>'
            
            st.markdown(behaviors_html, unsafe_allow_html=True)
            
            # Goals & Needs
            st.markdown('<h3>GOALS & NEEDS</h3>', unsafe_allow_html=True)
            goals = persona.get('goals', [])
            goals_html = ""
            for goal in goals:
                goals_html += f'<div class="lucas-list-item">{goal}</div>'
            
            st.markdown(goals_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            # Frustrations
            st.markdown('<div class="lucas-section">', unsafe_allow_html=True)
            st.markdown('<h3>FRUSTRATIONS</h3>', unsafe_allow_html=True)
            
            frustrations = persona.get('frustrations', [])
            frustrations_html = ""
            for frustration in frustrations:
                frustrations_html += f'<div class="lucas-list-item">{frustration}</div>'
            
            st.markdown(frustrations_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Close content grid
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Quote section at bottom
        quote = persona.get('quote', 'I want to spend less time ordering and more time enjoying.')
        st.markdown(f"""
        <div class="lucas-quote">
            "{quote}"
        </div>
        """, unsafe_allow_html=True)
        
        # Close main container
        st.markdown('</div>', unsafe_allow_html=True)