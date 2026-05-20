import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="SmartFridge: Nutrition Suite", layout="wide")

# Initialize Session States for persistent data storage
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'pantry' not in st.session_state:
    st.session_state.pantry = ["Salt", "Pepper", "Olive Oil", "Garlic Powder", "Sugar"]
st.sidebar.title("SmartFridge Controls")
common_items = ["Milk", "Eggs", "Chicken", "Spinach", "Bread", "Rice", "Butter", "Cheese", "Apples", "Chocolate", "Potato"]

with st.sidebar.form("add_food", clear_on_submit=True):
    st.write("Register Fresh Assets")
    food_choice = st.selectbox("Select Item", options=["Manual Entry"] + common_items)
    food_item = st.text_input("Item Name") if food_choice == "Manual Entry" else food_choice
    expiry_date = st.date_input("Expiry Date", value=datetime.now() + timedelta(days=7))
    if st.form_submit_button("Log to Inventory"):
        if food_item:
            st.session_state.inventory.append({"Item": food_item, "Expiry": str(expiry_date)})
            st.rerun()

st.title("SmartFridge: Inventory and Nutritional Intelligence")
today_date = datetime.now().date()

st.write("### Meal Discovery Parameters")
pref_col1, pref_col2, pref_col3 = st.columns(3)

with pref_col1:
    meal_type = st.selectbox("Category", ["Main Dish", "Light Snack", "Dessert"])
with pref_col2:
    health_profile = st.selectbox("Nutritional Profile", ["Healthy", "Healthy yet Tasty", "Indulgent"])
with pref_col3:
    st.metric("Pantry Staples", len(st.session_state.pantry))

st.write("---")

col_inv, col_recipes = st.columns(2)

with col_inv:
    st.subheader("Current Stock")
    if not st.session_state.inventory:
        st.info("System memory empty. Please log items via the sidebar.")
    else:
        st.session_state.inventory.sort(key=lambda x: x['Expiry'])
        for idx, food in enumerate(st.session_state.inventory):
            exp_date = datetime.strptime(food['Expiry'], "%Y-%m-%d").date()
            if exp_date < today_date:
                color, label = "red", "EXPIRED"
            elif today_date <= exp_date <= (today_date + timedelta(days=2)):
                color, label = "orange", "URGENT"
            else:
                color, label = "green", "STABLE"
            
            st.markdown(f":{color}[**{food['Item']}**] | Expiry: {food['Expiry']} | Status: {label}")
            if st.button(f"Consume {food['Item']}", key=f"eat_{idx}"):
                st.session_state.inventory.pop(idx)
                st.rerun()

with col_recipes:
    st.subheader("Compatible Recipe Identification")
    current_fridge = [i['Item'].lower() for i in st.session_state.inventory]
    
    recipes = [
        {"name": "Steamed Spinach and Eggs", "type": "Main Dish", "profile": "Healthy", "fridge": ["spinach", "eggs"], "cal": "Low"},
        {"name": "Buttery Fried Eggs", "type": "Main Dish", "profile": "Healthy yet Tasty", "fridge": ["eggs", "butter"], "cal": "Medium"},
        {"name": "Cheesy Potato Bake", "type": "Main Dish", "profile": "Indulgent", "fridge": ["potato", "cheese", "butter"], "cal": "High"},
        {"name": "Organic Apple Slices", "type": "Light Snack", "profile": "Healthy", "fridge": ["apples"], "cal": "Low"},
        {"name": "Chocolate Dipped Fruit", "type": "Dessert", "profile": "Healthy yet Tasty", "fridge": ["apples", "chocolate"], "cal": "Medium"},
        {"name": "Indulgent Chocolate Melt", "type": "Dessert", "profile": "Indulgent", "fridge": ["chocolate", "butter", "milk"], "cal": "High"}
    ]

    match_found = False
    for r in recipes:
        # Check for matching ingredients and user-selected filters
        has_ingredients = all(item in current_fridge for item in r["fridge"])
        if has_ingredients and r["type"] == meal_type and r["profile"] == health_profile:
            match_found = True
            with st.expander(f"Recipe: {r['name']}"):
                st.write(f"Caloric Density: {r['cal']}")
                st.write("Required Assets: " + ", ".join(r["fridge"]))
                st.success("All requirements met.")
    
    if not match_found:
        st.warning(f"No matches found for {health_profile.lower()} {meal_type.lower()} with current inventory.")

st.write("---")
st.caption("SmartFridge v1.2 | Professional Nutrition Suite | Calgary Developer Project")
