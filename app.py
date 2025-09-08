import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="Media Tracker",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern tile design
st.markdown("""
<style>
/* Global styling */
.stApp {
    background-color: #f8f9fa;
}

.main .block-container {
    padding-top: 2rem;
    max-width: 800px;
    background-color: #f8f9fa;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Tile container */
.tile-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    padding: 20px;
    max-width: 600px;
    margin: 0 auto;
}

/* Base tile styling */
.tile {
    border-radius: 20px;
    padding: 30px 25px;
    color: white;
    font-weight: 600;
    font-size: 1.4rem;
    text-align: left;
    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}

.tile:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.15);
}

/* Tile gradients */
.tile-music {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.tile-movies {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.tile-tvshows {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.tile-videogames {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

/* Expanded tile styling */
.tile.expanded {
    grid-column: 1 / -1;
    min-height: 400px;
    padding: 30px;
}

.tile-content {
    margin-top: 20px;
    display: none;
}

.tile.expanded .tile-content {
    display: block;
}

/* Form styling within tiles */
.tile-form {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    margin-top: 15px;
    backdrop-filter: blur(10px);
}

.tile-input {
    width: 100%;
    padding: 12px 15px;
    border: none;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.9);
    color: #333;
    font-size: 1rem;
    margin-bottom: 10px;
}

.tile-button {
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    color: white;
    padding: 10px 20px;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.2s ease;
    margin-right: 10px;
}

.tile-button:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
}

/* Item list styling */
.item-list {
    margin-top: 15px;
}

.item {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 12px 15px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(5px);
}

.item-text {
    color: white;
    font-weight: 500;
}

.item-actions {
    display: flex;
    gap: 8px;
}

.action-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    padding: 5px 10px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.8rem;
    transition: all 0.2s ease;
}

.action-btn:hover {
    background: rgba(255, 255, 255, 0.3);
}

/* Responsive design */
@media (max-width: 768px) {
    .tile-container {
        grid-template-columns: 1fr;
        gap: 15px;
        padding: 15px;
    }
    
    .tile {
        min-height: 100px;
        padding: 25px 20px;
        font-size: 1.2rem;
    }
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

if 'new_item' not in st.session_state:
    st.session_state.new_item = ""

# Tile data
tiles = [
    {'name': 'Music', 'class': 'tile-music'},
    {'name': 'Movies', 'class': 'tile-movies'},
    {'name': 'TV Shows', 'class': 'tile-tvshows'},
    {'name': 'Videogames', 'class': 'tile-videogames'}
]

# Create the tile interface
st.markdown('<div class="tile-container">', unsafe_allow_html=True)

# Create 2x2 grid of tiles
col1, col2 = st.columns(2)

# Row 1
with col1:
    # Music tile
    if st.button("", key="tile_music", help="Click to expand Music"):
        st.session_state.expanded_tile = "Music" if st.session_state.expanded_tile != "Music" else None
        st.rerun()
    
    st.markdown("""
    <div class="tile tile-music" style="margin-top: -50px; pointer-events: none;">
        <div class="tile-title">Music</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Movies tile
    if st.button("", key="tile_movies", help="Click to expand Movies"):
        st.session_state.expanded_tile = "Movies" if st.session_state.expanded_tile != "Movies" else None
        st.rerun()
    
    st.markdown("""
    <div class="tile tile-movies" style="margin-top: -50px; pointer-events: none;">
        <div class="tile-title">Movies</div>
    </div>
    """, unsafe_allow_html=True)

# Row 2
col3, col4 = st.columns(2)

with col3:
    # TV Shows tile
    if st.button("", key="tile_tvshows", help="Click to expand TV Shows"):
        st.session_state.expanded_tile = "TV Shows" if st.session_state.expanded_tile != "TV Shows" else None
        st.rerun()
    
    st.markdown("""
    <div class="tile tile-tvshows" style="margin-top: -50px; pointer-events: none;">
        <div class="tile-title">TV Shows</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    # Videogames tile
    if st.button("", key="tile_videogames", help="Click to expand Videogames"):
        st.session_state.expanded_tile = "Videogames" if st.session_state.expanded_tile != "Videogames" else None
        st.rerun()
    
    st.markdown("""
    <div class="tile tile-videogames" style="margin-top: -50px; pointer-events: none;">
        <div class="tile-title">Videogames</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Show expanded content below the tiles
if st.session_state.expanded_tile:
    tile_name = st.session_state.expanded_tile
    
    st.markdown("---")
    st.markdown(f"## {tile_name}")
    
    # Add new item form
    with st.form(f"add_{tile_name.lower().replace(' ', '_')}", clear_on_submit=True):
        new_item = st.text_input(f"Add new {tile_name.lower()}", 
                               placeholder=f"Enter {tile_name.lower()} title...")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.form_submit_button("Add"):
                if new_item.strip():
                    new_entry = {
                        'id': str(uuid.uuid4()),
                        'title': new_item.strip(),
                        'added': datetime.now()
                    }
                    st.session_state.media_data[tile_name].append(new_entry)
                    st.success(f"Added '{new_item}' to {tile_name}!")
                    st.rerun()
        
        with col2:
            if st.form_submit_button("Close"):
                st.session_state.expanded_tile = None
                st.rerun()
    
    # Display existing items
    if st.session_state.media_data[tile_name]:
        st.markdown(f"### Your {tile_name}")
        
        for item in st.session_state.media_data[tile_name]:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"• {item['title']}")
            
            with col2:
                if st.button("🗑️", key=f"delete_{item['id']}", help="Delete"):
                    st.session_state.media_data[tile_name] = [
                        i for i in st.session_state.media_data[tile_name] 
                        if i['id'] != item['id']
                    ]
                    st.rerun()
    else:
        st.info(f"No {tile_name.lower()} added yet. Add your first item above!")
