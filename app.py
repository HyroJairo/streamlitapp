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

/* Tile container */
.tile-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding: 20px;
    max-width: 450px;
    margin: 0 auto;
}

/* Base tile styling */
.tile {
    border-radius: 25px;
    padding: 25px 30px;
    color: white;
    font-weight: 600;
    font-size: 1.6rem;
    text-align: left;
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    cursor: pointer;
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-left: 15px;
}

.tile::before {
    content: '';
    position: absolute;
    left: -15px;
    top: 50%;
    transform: translateY(-50%);
    width: 30px;
    height: 30px;
    background-color: #333;
    border-radius: 50%;
    z-index: 10;
}

.tile:hover {
    transform: translateX(5px);
    box-shadow: 0 12px 35px rgba(0,0,0,0.2);
}

/* Tile gradients */
.tile-music {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.tile-movies {
    background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%);
}

.tile-tvshows {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.tile-videogames {
    background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
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
    is_expanded = st.session_state.expanded_tile == tile_name
    
    # Create columns for tile interaction
    col1, col2 = st.columns([10, 1])
    
    with col1:
        # Tile click button (invisible)
        if st.button("", key=f"tile_{tile_name}", help=f"Click to expand {tile_name}"):
            if st.session_state.expanded_tile == tile_name:
                st.session_state.expanded_tile = None
                st.session_state.show_add_form[tile_name] = False
            else:
                st.session_state.expanded_tile = tile_name
                # Close add forms for all tiles
                for category in st.session_state.show_add_form.keys():
                    st.session_state.show_add_form[category] = False
            st.rerun()
    
    # Tile HTML
    expanded_class = " expanded" if is_expanded else ""
    
    st.markdown(f"""
    <div class="tile {tile_class}{expanded_class}" style="margin-top: -50px; pointer-events: none;">
        <div class="tile-title">{tile_name}</div>
        <div class="tile-content">
    """, unsafe_allow_html=True)
    
    # If this tile is expanded, show the content inside
    if is_expanded:
        # Show add form if requested
        if st.session_state.show_add_form[tile_name]:
            st.markdown('<div class="add-form">', unsafe_allow_html=True)
            
            with st.form(f"add_{tile_name.lower().replace(' ', '_')}", clear_on_submit=True):
                new_item = st.text_input("", 
                                       placeholder=f"Enter {tile_name.lower()} title...",
                                       key=f"input_{tile_name}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Add", use_container_width=True):
                        if new_item.strip():
                            new_entry = {
                                'id': str(uuid.uuid4()),
                                'title': new_item.strip(),
                                'added': datetime.now()
                            }
                            st.session_state.media_data[tile_name].append(new_entry)
                            st.session_state.show_add_form[tile_name] = False
                            st.success(f"Added '{new_item}' to {tile_name}!")
                            st.rerun()
                
                with col2:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.session_state.show_add_form[tile_name] = False
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Display existing items
        if st.session_state.media_data[tile_name]:
            st.markdown('<div class="item-list">', unsafe_allow_html=True)
            
            for item in st.session_state.media_data[tile_name]:
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f'<div class="item-text">{item["title"]}</div>', unsafe_allow_html=True)
                
                with col2:
                    if st.button("🗑️", key=f"delete_{item['id']}", help="Delete"):
                        st.session_state.media_data[tile_name] = [
                            i for i in st.session_state.media_data[tile_name] 
                            if i['id'] != item['id']
                        ]
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty-state">No items added yet</div>', unsafe_allow_html=True)
        
        # Add section with plus button in lower left and close button in lower right
        st.markdown('<div class="add-section">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("+", key=f"add_{tile_name}", help="Add new item"):
                st.session_state.show_add_form[tile_name] = True
                st.rerun()
        
        with col3:
            if st.button("Close", key=f"close_{tile_name}"):
                st.session_state.expanded_tile = None
                st.session_state.show_add_form[tile_name] = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
