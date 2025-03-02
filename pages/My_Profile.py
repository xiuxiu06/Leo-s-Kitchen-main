# pages/profile.py
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# Page configuration
st.set_page_config(page_title="My Profile - Leo's Food App", page_icon="🐱", layout="wide")

# --- SIDEBAR NAVIGATION ---
# st.sidebar.title("Navigation")
# st.sidebar.page_link("app.py", label="🏠 Home", icon="🏠")
# st.sidebar.page_link("pages/about_me.py", label="ℹ️ About Me")
# st.sidebar.page_link("pages/my_recipes.py", label="📊 My Recipes")
# st.sidebar.page_link("pages/chatbot.py", label="🤖 Chat Bot")
# st.sidebar.page_link("pages/post_meal.py", label="📝 Share Your Meal")
# st.sidebar.page_link("pages/profile.py", label="👤 My Profile")
# st.sidebar.page_link("pages/auth.py", label="🔑 Login/Register")

# Initialize database connection
def get_db_connection():
    conn = sqlite3.connect('food_app.db', check_same_thread=False)
    return conn

# Check authentication status
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("Please log in to view your profile")
    st.button("Go to Login Page", on_click=lambda: st.switch_page("pages/auth.py"))
else:
    # Get user data
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT username, email, full_name, bio, profile_pic, date_joined, is_premium 
        FROM users WHERE id = ?
    """, (st.session_state.user_id,))
    
    user_data = c.fetchone()
    
    if not user_data:
        st.error("User data not found. Please try logging in again.")
    else:
        username, email, full_name, bio, profile_pic, date_joined, is_premium = user_data
        
        # --- PROFILE HEADER ---
        profile_header_col1, profile_header_col2 = st.columns([1, 3])
        
        with profile_header_col1:
            if profile_pic:
                st.image(profile_pic, width=200)
            else:
                st.image("https://api.placeholder.com/200/200", width=200)
                
        with profile_header_col2:
            if is_premium:
                st.title(f"{username} 🌟")
                st.caption("Premium Member")
            else:
                st.title(username)
                
            st.write(f"**Member since:** {date_joined}")
            st.write(f"**Full Name:** {full_name or 'Not set'}")
            
            if bio:
                st.write(f"**About me:** {bio}")
                
            # Edit profile button
            st.button("Edit Profile")
        
        # --- TABS FOR DIFFERENT SECTIONS ---
        tab1, tab2, tab3 = st.tabs(["My Stats", "My Recipes", "Saved Recipes"])
        
        with tab1:
            st.subheader("Nutrition Summary")
            
            # Mock data for user's nutrition history
            dates = pd.date_range(start='2025-02-01', end='2025-03-01')
            nutrition_data = pd.DataFrame({
                'Date': dates,
                'Protein': [round(100 + i*1.5) for i in range(len(dates))],
                'Carbs': [round(150 - i) for i in range(len(dates))],
                'Fat': [round(50 + i*0.5) for i in range(len(dates))],
                'Calories': [round(1800 + i*10) for i in range(len(dates))]
            })
            
            # Nutrition trend chart
            st.subheader("Your Macro Trends")
            fig = px.line(nutrition_data, x='Date', y=['Protein', 'Carbs', 'Fat'], 
                          title='Daily Macro Nutrients (Last 30 Days)')
            st.plotly_chart(fig, use_container_width=True)
            
            # Calorie tracking
            st.subheader("Calorie Tracking")
            fig2 = px.bar(nutrition_data, x='Date', y='Calories', 
                          title='Daily Calorie Intake (Last 30 Days)')
            st.plotly_chart(fig2, use_container_width=True)
            
            # Weekly summary stats
            st.subheader("Weekly Summary")
            weekly_data = nutrition_data.tail(7)
            
            avg_col1, avg_col2, avg_col3, avg_col4 = st.columns(4)
            with avg_col1:
                st.metric("Avg. Protein", f"{round(weekly_data['Protein'].mean())}g", 
                          f"{round(weekly_data['Protein'].mean() - weekly_data['Protein'].iloc[0])}g")
            with avg_col2:
                st.metric("Avg. Carbs", f"{round(weekly_data['Carbs'].mean())}g", 
                          f"{round(weekly_data['Carbs'].mean() - weekly_data['Carbs'].iloc[0])}g")
            with avg_col3:
                st.metric("Avg. Fat", f"{round(weekly_data['Fat'].mean())}g", 
                          f"{round(weekly_data['Fat'].mean() - weekly_data['Fat'].iloc[0])}g")
            with avg_col4:
                st.metric("Avg. Calories", f"{round(weekly_data['Calories'].mean())}", 
                          f"{round(weekly_data['Calories'].mean() - weekly_data['Calories'].iloc[0])}")
        
        with tab2:
            st.subheader("My Shared Recipes")
            
            # Mock data for user's recipes
            user_recipes = [
                {"name": "Protein Pancakes", "date": "Feb 28, 2025", "likes": 24, "comments": 3, 
                 "image": "https://api.placeholder.com/300/200"},
                {"name": "Chicken Avocado Wrap", "date": "Feb 20, 2025", "likes": 18, "comments": 2, 
                 "image": "https://api.placeholder.com/300/200"},
                {"name": "Greek Yogurt Bowl", "date": "Feb 15, 2025", "likes": 32, "comments": 5, 
                 "image": "https://api.placeholder.com/300/200"}
            ]
            
            for i, recipe in enumerate(user_recipes):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    st.image(recipe["image"], use_column_width=True)
                    
                with col2:
                    st.subheader(recipe["name"])
                    st.write(f"Posted on: {recipe['date']}")
                    st.write(f"❤️ {recipe['likes']} likes • 💬 {recipe['comments']} comments")
                    
                    action_col1, action_col2, action_col3 = st.columns(3)
                    with action_col1:
                        st.button("View Recipe", key=f"view_{i}")
                    with action_col2:
                        st.button("Edit", key=f"edit_{i}")
                    with action_col3:
                        st.button("Delete", key=f"delete_{i}")
                        
                st.divider()
            
            st.button("Create New Recipe", on_click=lambda: st.switch_page("pages/post_meal.py"))
        
        with tab3:
            st.subheader("Recipes You've Saved")
            
            # Mock data for saved recipes
            saved_recipes = [
                {"name": "Banana Protein Muffins", "author": "@HealthyBaker", "date_saved": "Mar 1, 2025", 
                 "image": "https://api.placeholder.com/300/200"},
                {"name": "Quinoa Salad Bowl", "author": "@NutritionChef", "date_saved": "Feb 25, 2025", 
                 "image": "https://api.placeholder.com/300/200"},
                {"name": "Low-Carb Pizza", "author": "@KetoKing", "date_saved": "Feb 20, 2025", 
                 "image": "https://api.placeholder.com/300/200"},
                {"name": "Protein Ice Cream", "author": "@FitnessFoodie", "date_saved": "Feb 18, 2025", 
                 "image": "https://api.placeholder.com/300/200"}
            ]
            
            saved_grid_cols = st.columns(2)
            
            for i, recipe in enumerate(saved_recipes):
                with saved_grid_cols[i % 2]:
                    st.image(recipe["image"], use_column_width=True)
                    st.subheader(recipe["name"])
                    st.write(f"By {recipe['author']} • Saved on {recipe['date_saved']}")
                    
                    view_col, unsave_col = st.columns(2)
                    with view_col:
                        st.button("View Recipe", key=f"saved_view_{i}")
                    with unsave_col:
                        st.button("Unsave", key=f"saved_unsave_{i}")
                    
                    st.write("")  # Add some spacing
