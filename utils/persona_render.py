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
        """Render a persona card using only Streamlit-native components (no HTML)."""
        name = persona.get('name', 'Unknown User')
        username = persona.get('username', 'unknown')
        st.header(f"{name}")
        st.caption(f"@{username}")

        col1, col2, col3 = st.columns(3)
        demo = persona.get('demographics', {})
        with col1:
            st.subheader("Demographics")
            st.write(f"**Age:** {demo.get('age', 'Unknown')}")
            st.write(f"**Occupation:** {demo.get('occupation', 'Unknown')}")
            st.write(f"**Status:** {demo.get('status', 'Unknown')}")
            st.write(f"**Location:** {demo.get('location', 'Unknown')}")
            st.write(f"**Tier:** {demo.get('tier', 'Unknown')}")
            st.write(f"**Archetype:** {demo.get('archetype', 'Unknown')}")

            st.subheader("Personality")
            personality = persona.get('personality', {})
            if personality:
                for trait, score in list(personality.items())[:4]:
                    st.write(f"- {trait}: {score}")
            else:
                st.write("No personality traits available.")

            st.subheader("Motivations")
            motivations = persona.get('motivations', {})
            if motivations:
                for motivation, score in motivations.items():
                    st.write(f"- {motivation}: {int(score*100)}%")
            else:
                st.write("No motivations available.")

        with col2:
            st.subheader("Behaviour & Habits")
            behaviors = persona.get('behaviors', [])
            if behaviors:
                for behavior in behaviors:
                    st.write(f"- {behavior}")
            else:
                st.write("No behaviors available.")

            st.subheader("Goals & Needs")
            goals = persona.get('goals', [])
            if goals:
                for goal in goals:
                    st.write(f"- {goal}")
            else:
                st.write("No goals available.")

        with col3:
            st.subheader("Frustrations")
            frustrations = persona.get('frustrations', [])
            if frustrations:
                for frustration in frustrations:
                    st.write(f"- {frustration}")
            else:
                st.write("No frustrations available.")

            st.subheader("Quote")
            quote = persona.get('quote', None)
            if quote:
                st.info(f'"{quote}"')
            else:
                st.write("No quote available.")