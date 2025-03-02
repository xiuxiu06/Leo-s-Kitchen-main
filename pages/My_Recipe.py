# pages/recipe_detail.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Recipe Details - Leo's Food App", page_icon="🐱", layout="wide")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="🏠 Home", icon="🏠")
st.sidebar.page_link("pages/about_me.py", label="ℹ️ About Me")
st.sidebar.page_link("pages/my_recipes.py", label="📊 My Recipes")
st.sidebar.page_link("pages/chatbot.py", label="🤖 Chat Bot")
st.sidebar.page_link("pages/post_meal.py", label="📝 Share Your Meal")

# Get recipe ID from query parameters (would be implemented in a real app)
# For demo purposes, let's create a sample recipe
recipe = {
    "id": 1,
    "name": "Protein-Packed Overnight Oats",
    "user": "@HealthyChef",
    "user_profile_pic": "https://api.placeholder.com/100/100",
    "date_posted": "February 28, 2025",
    "image": "https://api.placeholder.com/800/600",
    "category": "Breakfast",
    "description": "A delicious high-protein breakfast that you can prepare the night before. Perfect for busy mornings when you need a nutritious start to your day without spending time cooking.",
    "rating": 4.8,
    "reviews": 124,
    "protein": 32,
    "carbs": 45,
    "fat": 12,
    "calories": 420,
    "fiber": 8,
    "sugar": 6,
    "sodium": 120,
    "prep_time": "5 min",
    "cook_time": "0 min",
    "total_time": "5 min + overnight",
    "servings": 1,
    "ingredients": [
        "1/2 cup rolled oats",
        "1 scoop vanilla protein powder",
        "1 tablespoon chia seeds",
        "1 tablespoon almond butter",
        "1/2 cup almond milk",
        "1/4 cup Greek yogurt",
        "1/2 banana, sliced",
        "1/4 cup berries",
        "1 teaspoon honey or maple syrup (optional)"
    ],
    "instructions": [
        "In a jar or container, mix oats, protein powder, and chia seeds.",
        "Add almond milk and Greek yogurt, then stir until well combined.",
        "Stir in almond butter and sweetener if using.",
        "Seal the container and refrigerate overnight or for at least 4 hours.",
        "Before serving, top with sliced banana and berries."
    ],
    "tags": ["high-protein", "meal-prep", "vegetarian", "quick", "no-cook"],
    "saved_count": 342,
    "likes": 518,
    "similar_recipes": [
        {"id": 2, "name": "Protein Pancakes", "image": "https://api.placeholder.com/150/150"},
        {"id": 3, "name": "Greek Yogurt Bowl", "image": "https://api.placeholder.com/150/150"},
        {"id": 4, "name": "Protein Smoothie", "image": "https://api.placeholder.com/150/150"}
    ]
}

# --- RECIPE DETAIL PAGE ---

# Top section: Image and basic info
col_img, col_info = st.columns([3, 2], gap="large")

with col_img:
    st.image(recipe["image"], use_column_width=True)
    
    # Action buttons
    btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
    with btn_col1:
        st.button("❤️ Like", key="like_btn")
    with btn_col2:
        st.button("🔖 Save", key="save_btn")
    with btn_col3:
        st.button("📤 Share", key="share_btn")
    with btn_col4:
        st.button("🖨️ Print", key="print_btn")

with col_info:
    st.title(recipe["name"])
    
    # User and date info
    st.markdown(f"Posted by {recipe['user']} on {recipe['date_posted']}")
    
    # Rating
    st.markdown(f"⭐ {recipe['rating']} ({recipe['reviews']} ratings)")
    
    # Description
    st.markdown(recipe["description"])
    
    # Tags
    st.markdown("**Tags:** " + ", ".join([f"#{tag}" for tag in recipe["tags"]]))
    
    # Recipe stats
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    with stats_col1:
        st.markdown(f"**Prep time:**  \n{recipe['prep_time']}")
    with stats_col2:
        st.markdown(f"**Cook time:**  \n{recipe['cook_time']}")
    with stats_col3:
        st.markdown(f"**Servings:**  \n{recipe['servings']}")

# Nutrition information
st.subheader("Nutrition Information")
macro_cols = st.columns(4)

with macro_cols[0]:
    st.metric("Protein", f"{recipe['protein']}g")
with macro_cols[1]:
    st.metric("Carbs", f"{recipe['carbs']}g")
with macro_cols[2]:
    st.metric("Fat", f"{recipe['fat']}g")
with macro_cols[3]:
    st.metric("Calories", f"{recipe['calories']}")

# Macro pie chart
nutrition_data = pd.DataFrame({
    'Nutrient': ['Protein', 'Carbs', 'Fat'],
    'Grams': [recipe['protein'], recipe['carbs'], recipe['fat']],
    'Calories': [recipe['protein'] * 4, recipe['carbs'] * 4, recipe['fat'] * 9]
})

chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    fig = px.pie(nutrition_data, values='Grams', names='Nutrient', 
                 title='Macronutrient Distribution (grams)',
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c'])
    st.plotly_chart(fig, use_container_width=True)

with chart_col2:
    fig = px.pie(nutrition_data, values='Calories', names='Nutrient', 
                 title='Calorie Distribution',
                 color_discrete_sequence=['#1f77b4', '#ff7f0e', '#2ca02c'])
    st.plotly_chart(fig, use_container_width=True)

# Ingredients and Instructions
ingredients_col, instructions_col = st.columns(2)

with ingredients_col:
    st.subheader("Ingredients")
    for item in recipe["ingredients"]:
        st.checkbox(item)

with instructions_col:
    st.subheader("Instructions")
    for i, step in enumerate(recipe["instructions"]):
        st.markdown(f"{i+1}. {step}")

# Comments section
st.subheader("Comments")
with st.form("comment_form"):
    comment_text = st.text_area("Leave a comment", placeholder="Share your thoughts or ask a question...")
    submit_comment = st.form_submit_button("Post Comment")

if submit_comment and comment_text:
    st.success("Comment posted successfully!")

# Sample comments
st.markdown("**@FitnessFoodie** • 2 days ago  \nMade this yesterday and loved it! I added a tablespoon of cocoa powder for a chocolate version. Delicious!")

st.markdown("**@ProteinQueen** • 5 days ago  \nThis has become my go-to breakfast! So convenient and keeps me full until lunch.")

# Similar recipes
st.subheader("You might also like")
similar_cols = st.columns(3)

for i, similar in enumerate(recipe["similar_recipes"]):
    with similar_cols[i]:
        st.image(similar["image"], use_column_width=True)
        st.markdown(f"**{similar['name']}**")
        st.button("View Recipe", key=f"similar_{i}")
