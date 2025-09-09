import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="Media Tracker",
    page_icon="📱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for vertical tile design
st.markdown("""
<style>
/* Global styling */
.stApp {
    background-color: #f0f0f0;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 500px;
    background-color: #f0f0f0;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {visibility: hidden;}

/* Hide all buttons except add and form buttons */
.stButton > button:not([key*="add_"]) {
    display: none !important;
}

/* Show plus buttons and form buttons */
.stButton > button[key*="add_"] {
    display: block !important;
    background: rgba(255, 255, 255, 0.2) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    color: white !important;
    width: 45px !important;
    height: 45px !important;
    border-radius: 50% !important;
    font-size: 1.5rem !important;
    font-weight: bold !important;
    transition: all 0.2s ease !important;
}

.stButton > button[key*="add_"]:hover {
    background: rgba(255, 255, 255, 0.3) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
    transform: scale(1.05) !important;
}

/* Style form submit buttons */
.stForm button {
    display: block !important;
    background: rgba(255, 255, 255, 0.2) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    color: white !important;
    padding: 8px 16px !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* Tile container */
.tile-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 30px 20px;
    max-width: 450px;
    margin: 0 auto;
}

/* Base tile styling with hover expansion */
.tile {
    border-radius: 25px;
    padding: 25px 30px;
    color: white;
    font-weight: 600;
    font-size: 1.6rem;
    text-align: left;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    cursor: pointer;
    transition: all 0.6s ease;
    position: relative;
    overflow: hidden;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-left: 0px;
}

.tile:hover {
    min-height: 300px;
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
}

.tile:hover .tile-content {
    display: flex !important;
    flex-direction: column;
    height: 100%;
    margin-top: 30px;
}

.tile:hover .hover-plus {
    display: block !important;
}

/* Tile gradients */
.tile-music {
    background: linear-gradient(90deg, rgba(42, 123, 155, 1) 0%, rgba(87, 199, 133, 1) 50%, rgba(237, 221, 83, 1) 100%);
}

.tile-movies {
    background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
}

.tile-tvshows {
    background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 35%, #60a5fa 100%);
}

.tile-videogames {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

/* Expanded tile styling */
.tile.expanded {
    min-height: 400px;
    cursor: default;
}

.tile.expanded:hover {
    transform: translateX(0px);
}

/* Tile content */
.tile-content {
    margin-top: 20px;
    display: none;
    flex-grow: 1;
}

.tile.expanded .tile-content {
    display: flex;
    flex-direction: column;
    height: 100%;
}

/* Item list styling */
.item-list {
    flex-grow: 1;
    margin-bottom: 20px;
}

.item {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 12px 15px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.item-text {
    color: white;
    font-weight: 500;
    font-size: 1rem;
}

.delete-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    padding: 6px 10px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.9rem;
    transition: all 0.2s ease;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.delete-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.4);
}

/* Add button (plus sign) */
.add-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
}

.add-btn {
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    color: white;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.5rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}

.add-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: scale(1.05);
}

.close-btn {
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 600;
    transition: all 0.2s ease;
}

.close-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
}

/* Add form styling */
.add-form {
    background: rgba(255, 255, 255, 0.15);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.add-input {
    width: 100%;
    padding: 12px 15px;
    border: none;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.9);
    color: #333;
    font-size: 1rem;
    margin-bottom: 15px;
    box-sizing: border-box;
}

.add-input::placeholder {
    color: #666;
}

.form-buttons {
    display: flex;
    gap: 10px;
}

.form-btn {
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
    font-size: 0.9rem;
}

.form-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
}

/* Style text input for faint line appearance */
.stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 0 !important;
    color: white !important;
    font-size: 1rem !important;
    padding: 8px 0 !important;
    margin-bottom: 15px !important;
}

.stTextInput > div > div > input:focus {
    border-bottom: 2px solid rgba(255, 255, 255, 0.6) !important;
    outline: none !important;
    box-shadow: none !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
}

/* Hide streamlit form elements */
.stForm {
    border: none !important;
    background: none !important;
}

/* Empty state */
.empty-state {
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    font-style: italic;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'media_data' not in st.session_state:
    st.session_state.media_data = {
        'Music': [],
        'Movies': [],
        'TV Shows': [],
        'Videogames': []
    }

if 'expanded_tile' not in st.session_state:
    st.session_state.expanded_tile = None

if 'show_add_form' not in st.session_state:
    st.session_state.show_add_form = {}
    for category in st.session_state.media_data.keys():
        st.session_state.show_add_form[category] = False

# Tile data
tiles = [
    {'name': 'Music', 'class': 'tile-music'},
    {'name': 'Movies', 'class': 'tile-movies'},
    {'name': 'TV Shows', 'class': 'tile-tvshows'},
    {'name': 'Videogames', 'class': 'tile-videogames'}
]

# Create the tile interface
st.markdown('<div class="tile-container">', unsafe_allow_html=True)

for tile in tiles:
    tile_name = tile['name']
    tile_class = tile['class']
    
    # Simple tile HTML with hover expansion
    st.markdown(f"""
    <div class="tile {tile_class}">
        <div class="tile-title">{tile_name}</div>
        <div class="tile-content">
            <div class="hover-plus" style="display: none; position: absolute; bottom: 20px; right: 20px;">
                <div style="background: rgba(255, 255, 255, 0.2); border: 2px solid rgba(255, 255, 255, 0.3); color: white; width: 45px; height: 45px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: bold;">+</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
