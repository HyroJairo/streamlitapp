import streamlit as st
import pandas as pd
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="Rainbow To-Do List",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for light rainbow theme and fluid scrolling
st.markdown("""
<style>
/* Main app styling */
.main .block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

/* Header styling */
.main-header {
    text-align: center;
    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 25%, #fecfef 50%, #a8e6cf 75%, #88d8c0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.subtitle {
    text-align: center;
    color: #666;
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

/* Category tabs */
.category-tabs {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}

/* Category specific colors */
.movies-theme {
    background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
}

.shows-theme {
    background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%);
}

.music-theme {
    background: linear-gradient(135deg, #ffd3a5 0%, #fd9853 100%);
}

.games-theme {
    background: linear-gradient(135deg, #a8c8ec 0%, #7fcdff 100%);
}

/* Todo item styling */
.todo-item {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 1rem;
    margin: 0.5rem 0;
    border-left: 5px solid;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.todo-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.todo-item.completed {
    opacity: 0.7;
    background: rgba(200, 255, 200, 0.3);
}

.todo-item.movies { border-left-color: #ff9a9e; }
.todo-item.shows { border-left-color: #a8e6cf; }
.todo-item.music { border-left-color: #ffd3a5; }
.todo-item.games { border-left-color: #a8c8ec; }

/* Scrollable container */
.scrollable-container {
    max-height: 500px;
    overflow-y: auto;
    padding-right: 10px;
    scrollbar-width: thin;
    scrollbar-color: #ff9a9e #f1f1f1;
}

.scrollable-container::-webkit-scrollbar {
    width: 8px;
}

.scrollable-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

.scrollable-container::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #ff9a9e, #a8e6cf);
    border-radius: 10px;
}

/* Form styling */
.add-form {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Stats cards */
.stats-card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 0.5rem;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom button styling */
.stButton > button {
    background: linear-gradient(135deg, #ff9a9e 0%, #a8e6cf 100%);
    border: none;
    border-radius: 25px;
    color: white;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'todos' not in st.session_state:
    st.session_state.todos = {
        'Movies': [
            {'id': str(uuid.uuid4()), 'task': 'Watch The Shawshank Redemption', 'completed': False, 'created': datetime.now()},
            {'id': str(uuid.uuid4()), 'task': 'Rewatch Inception', 'completed': True, 'created': datetime.now()},
        ],
        'Shows': [
            {'id': str(uuid.uuid4()), 'task': 'Finish Breaking Bad Season 5', 'completed': False, 'created': datetime.now()},
            {'id': str(uuid.uuid4()), 'task': 'Start Stranger Things', 'completed': False, 'created': datetime.now()},
        ],
        'Music': [
            {'id': str(uuid.uuid4()), 'task': 'Listen to new Taylor Swift album', 'completed': False, 'created': datetime.now()},
            {'id': str(uuid.uuid4()), 'task': 'Discover jazz playlist', 'completed': True, 'created': datetime.now()},
        ],
        'Games': [
            {'id': str(uuid.uuid4()), 'task': 'Complete Zelda: Breath of the Wild', 'completed': False, 'created': datetime.now()},
            {'id': str(uuid.uuid4()), 'task': 'Try new indie games', 'completed': False, 'created': datetime.now()},
        ]
    }

if 'current_category' not in st.session_state:
    st.session_state.current_category = 'Movies'

# Header
st.markdown('<h1 class="main-header">🌈 Rainbow To-Do List</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Organize your entertainment goals with style</p>', unsafe_allow_html=True)

# Category selection
categories = ['Movies', 'Shows', 'Music', 'Games']
category_icons = {'Movies': '🎬', 'Shows': '📺', 'Music': '🎵', 'Games': '🎮'}
category_colors = {
    'Movies': '#ff9a9e',
    'Shows': '#a8e6cf', 
    'Music': '#ffd3a5',
    'Games': '#a8c8ec'
}

# Category tabs
cols = st.columns(4)
for i, category in enumerate(categories):
    with cols[i]:
        if st.button(f"{category_icons[category]} {category}", key=f"tab_{category}"):
            st.session_state.current_category = category

# Current category indicator
current_cat = st.session_state.current_category
st.markdown(f"""
<div style="text-align: center; margin: 1rem 0;">
    <h2 style="color: {category_colors[current_cat]}; font-size: 2rem;">
        {category_icons[current_cat]} {current_cat}
    </h2>
</div>
""", unsafe_allow_html=True)

# Stats overview
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_tasks = sum(len(tasks) for tasks in st.session_state.todos.values())
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="color: #ff9a9e; margin: 0;">📋 Total</h3>
        <h2 style="margin: 0.5rem 0;">{total_tasks}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    completed_tasks = sum(len([t for t in tasks if t['completed']]) for tasks in st.session_state.todos.values())
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="color: #a8e6cf; margin: 0;">✅ Done</h3>
        <h2 style="margin: 0.5rem 0;">{completed_tasks}</h2>
    </div>
    """, unsafe_allow_html=True)

with col3:
    pending_tasks = total_tasks - completed_tasks
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="color: #ffd3a5; margin: 0;">⏳ Pending</h3>
        <h2 style="margin: 0.5rem 0;">{pending_tasks}</h2>
    </div>
    """, unsafe_allow_html=True)

with col4:
    category_tasks = len(st.session_state.todos[current_cat])
    st.markdown(f"""
    <div class="stats-card">
        <h3 style="color: {category_colors[current_cat]}; margin: 0;">{category_icons[current_cat]} {current_cat}</h3>
        <h2 style="margin: 0.5rem 0;">{category_tasks}</h2>
    </div>
    """, unsafe_allow_html=True)

# Add new task form
st.markdown('<div class="add-form">', unsafe_allow_html=True)
st.markdown(f"### ➕ Add New {current_cat} Task")

with st.form(f"add_task_form_{current_cat}"):
    new_task = st.text_input("What would you like to add to your list?", 
                            placeholder=f"Enter a new {current_cat.lower()} task...")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        submitted = st.form_submit_button("Add Task ✨")
    
    if submitted and new_task.strip():
        new_todo = {
            'id': str(uuid.uuid4()),
            'task': new_task.strip(),
            'completed': False,
            'created': datetime.now()
        }
        st.session_state.todos[current_cat].append(new_todo)
        st.success(f"Added '{new_task}' to {current_cat}! 🎉")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Display tasks for current category
if st.session_state.todos[current_cat]:
    st.markdown(f"### 📝 Your {current_cat} List")
    
    # Create scrollable container
    st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
    
    # Sort tasks: incomplete first, then completed
    tasks = sorted(st.session_state.todos[current_cat], 
                  key=lambda x: (x['completed'], -x['created'].timestamp()))
    
    for i, todo in enumerate(tasks):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        
        with col1:
            # Checkbox for completion
            checked = st.checkbox("", 
                                value=todo['completed'], 
                                key=f"check_{current_cat}_{todo['id']}")
            
            if checked != todo['completed']:
                # Update completion status
                for task in st.session_state.todos[current_cat]:
                    if task['id'] == todo['id']:
                        task['completed'] = checked
                        break
                st.rerun()
        
        with col2:
            # Task text with styling based on completion
            task_class = "completed" if todo['completed'] else ""
            category_class = current_cat.lower()
            
            task_style = ""
            if todo['completed']:
                task_style = "text-decoration: line-through; opacity: 0.6;"
            
            st.markdown(f"""
            <div class="todo-item {task_class} {category_class}">
                <p style="margin: 0; font-size: 1.1rem; {task_style}">
                    {todo['task']}
                </p>
                <small style="color: #888;">
                    Added: {todo['created'].strftime('%Y-%m-%d %H:%M')}
                </small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Delete button
            if st.button("🗑️", key=f"delete_{current_cat}_{todo['id']}", 
                        help="Delete this task"):
                st.session_state.todos[current_cat] = [
                    t for t in st.session_state.todos[current_cat] 
                    if t['id'] != todo['id']
                ]
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Clear completed tasks button
    completed_in_category = [t for t in st.session_state.todos[current_cat] if t['completed']]
    if completed_in_category:
        st.markdown("---")
        if st.button(f"🧹 Clear Completed {current_cat} Tasks ({len(completed_in_category)})", 
                    key=f"clear_{current_cat}"):
            st.session_state.todos[current_cat] = [
                t for t in st.session_state.todos[current_cat] if not t['completed']
            ]
            st.success(f"Cleared {len(completed_in_category)} completed tasks! ✨")
            st.rerun()

else:
    # Empty state
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem; color: #888;">
        <h1 style="font-size: 4rem; margin: 0;">{category_icons[current_cat]}</h1>
        <h3>No {current_cat.lower()} tasks yet!</h3>
        <p>Add your first task above to get started.</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #888;">
    <p>🌈 Made with ❤️ using Streamlit | Stay organized, stay colorful! ✨</p>
</div>
""", unsafe_allow_html=True)