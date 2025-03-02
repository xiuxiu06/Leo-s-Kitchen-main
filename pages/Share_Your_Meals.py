# pages/post_meal.py
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Share Your Meal - Leo's Food App", page_icon="🐱", layout="wide")

# --- SIDEBAR NAVIGATION ---
# st.sidebar.title("Navigation")
# st.sidebar.page_link("app.py", label="🏠 Home", icon="🏠")
# st.sidebar.page_link("pages/about_me.py", label="ℹ️ About Me")
# st.sidebar.page_link("pages/my_recipes.py", label="📊 My Recipes")
# st.sidebar.page_link("pages/chatbot.py", label="🤖 Chat Bot")
# st.sidebar.page_link("pages/post_meal.py", label="📝 Share Your Meal")

# --- SHARE MEAL FORM ---
st.title("Share Your Meal 📝")
st.write("Fill out the form below to share your meal with the community!")

with st.form("meal_form"):
    # Basic meal information
    col1, col2 = st.columns(2)
    
    with col1:
        meal_name = st.text_input("Meal Name", placeholder="e.g., Protein-Packed Breakfast Bowl")
        meal_category = st.selectbox("Category", ["Breakfast", "Lunch", "Dinner", "Snacks", "Desserts"])
        meal_tags = st.text_input("Tags (comma separated)", placeholder="e.g., high-protein, keto, vegan")
    
    with col2:
        meal_description = st.text_area("Description", placeholder="Describe your meal in a few sentences...")
        recipe_url = st.text_input("Recipe URL (optional)", placeholder="Link to full recipe if available")
    
    # Image upload
    st.subheader("Meal Image")
    uploaded_image = st.file_uploader("Upload an image of your meal", type=["jpg", "jpeg", "png"])
    
    # Show a preview if image is uploaded
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Image Preview", use_column_width=True)
    
    # Nutrition information
    st.subheader("Nutrition Information")
    
    macro_col1, macro_col2, macro_col3, macro_col4 = st.columns(4)
    
    with macro_col1:
        protein = st.number_input("Protein (g)", min_value=0, value=20)
    
    with macro_col2:
        carbs = st.number_input("Carbs (g)", min_value=0, value=30)
    
    with macro_col3:
        fat = st.number_input("Fat (g)", min_value=0, value=10)
    
    with macro_col4:
        calories = st.number_input("Calories", min_value=0, value=protein*4 + carbs*4 + fat*9)
    
    # Additional macros (collapsible)
    with st.expander("Additional Nutrition Info (Optional)"):
        add_col1, add_col2, add_col3 = st.columns(3)
        
        with add_col1:
            fiber = st.number_input("Fiber (g)", min_value=0, value=0)
            sugar = st.number_input("Sugar (g)", min_value=0, value=0)
        
        with add_col2:
            sodium = st.number_input("Sodium (mg)", min_value=0, value=0)
            cholesterol = st.number_input("Cholesterol (mg)", min_value=0, value=0)
        
        with add_col3:
            saturated_fat = st.number_input("Saturated Fat (g)", min_value=0, value=0)
            trans_fat = st.number_input("Trans Fat (g)", min_value=0, value=0)
    
    # Ingredients and Instructions
    st.subheader("Ingredients")
    ingredients = st.text_area("List your ingredients (one per line)", height=150, 
                               placeholder="1 cup oats\n2 scoops protein powder\n1 tbsp peanut butter")
    
    st.subheader("Instructions")
    instructions = st.text_area("Recipe instructions", height=150,
                                placeholder="1. Mix oats and protein powder\n2. Add water and microwave for 2 minutes\n3. Top with peanut butter")
    
    # Submit button
    submitted = st.form_submit_button("Share Your Meal")

if submitted:
    # Calculate actual calories from macros
    calculated_calories = protein * 4 + carbs * 4 + fat * 9
    
    # Success message
    st.success("Your meal has been shared successfully!")
    
    # Show a preview of how it will appear in the feed
    st.subheader("Preview:")
    
    preview_col1, preview_col2 = st.columns([1, 2])
    
    with preview_col1:
        if uploaded_image is not None:
            st.image(uploaded_image, use_column_width=True)
        else:
            st.image("https://api.placeholder.com/400/300", use_column_width=True)
    
    with preview_col2:
        st.markdown(f"### {meal_name}")
        st.markdown(f"**Category:** {meal_category}")
        st.markdown(f"**Description:** {meal_description}")
        
        st.markdown("#### Nutrition Facts")
        st.markdown(f"**Protein:** {protein}g | **Carbs:** {carbs}g | **Fat:** {fat}g | **Calories:** {calories}")
        
        if recipe_url:
            st.markdown(f"[View Full Recipe]({recipe_url})")
