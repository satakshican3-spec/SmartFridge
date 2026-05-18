import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="SmartFridge: Kitchen Manager", layout="wide")

if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'pantry' not in st.session_state:
    st.session_state.pantry = ["Salt", "Pepper", "Olive Oil", "Garlic Powder"]

st.sidebar.title("SmartFridge Controls")

common_items = ["Milk", "Eggs", "Chicken", "Spinach", "Bread", "Rice", "Butter", "Cheese", "Apples"]

with st.sidebar.form("add_food", clear_on_submit=True):
    st.write("### Add Fresh Items")
    food_choice = st.selectbox("Choose Item", options=["Custom..."] + common_items)
    if food_choice == "Custom...":
        food_item = st.text_input("Enter Item Name")
    else:
        food_item = food_choice

    expiry_date = st.date_input("Expiry Data", value=datetime.now() + timedelta(days=7))

    if st.form_submit_button("Add to Fridge"):
        if food_item:
            st.session_state.inventory.append({
                "Item": food_item,
                "Expiry": str(expiry_date)
            })
            st.rerun()

with st.sidebar.expander("Pantry & Seasonings"):
    new_seasoning = st.text_input("Add Seasoning:")
    if st.button("Add to Pantry"):
        st.session_state.pantry.append(new_seasoning)
    st.write("Current Stock:")
    st.caption(", ".join(st.session_state.pantry))

st.title("SmartFridge: Inventory System")
today = datetime.now().date()

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Items in Fridge", len(st.session_state.inventory))
col_m2.metric("Pantry Basics", len(st.session_state.pantry))
col_m3.metric("Kitchen Status", "Active")

st.write("---")

col_inv, col_recipes = st.columns()

with col_inv:
    st.subheader("Virtual Inventory")
    if not st.session_state.inventory:
        st.info("Your fridge is empty. Log items in the sidebar.")
    else:
        st.session_state.inventory.sort(key=lambda x: x['Expiry'])
        for idx, food in enumerate(st.session_state.inventory):
            exp_date = datetime.strptime(food['Expiry'], "%Y-%m-%d").date()
            
            if exp_date < today:
                color, label = "red", "EXPIRED"
            elif today <= exp_date <= (today + timedelta(days=2)):
                color, label = "orange", "USE SOON"
            else:
                color, label = "green", "FRESH"

            st.markdown(f":{color}[**{food['Item']}**] | {food['Expiry']} | **{label}**")
            if st.button(f"Consume {food['Item']}", key=f"eat_{idx}"):
                st.session_state.inventory.pop(idx)
                st.rerun()

with col_recipes:
    st.subheader("Meal Discovery")
    current_fridge = [i['Item'].lower() for i in st.session_state.inventory]
    current_pantry = [p.lower() for p in st.session_state.pantry]
    
    recipes = {
        "Scrambled Eggs": {"fridge": ["eggs", "butter"], "pantry": ["salt", "pepper"]},
        "Garlic Spinach": {"fridge": ["spinach"], "pantry": ["olive oil", "garlic powder", "salt"]},
        "Simple Fried Rice": {"fridge": ["rice", "eggs"], "pantry": ["pepper"]}
    }

    found = False
    for name, reqs in recipes.items():
        if all(item in current_fridge for item in reqs["fridge"]):
            found = True
            with st.expander(f"{name}"):
                st.write("**Ingredients:** " + ", ".join(reqs["fridge"]))
                missing_pantry = [p for p in reqs["pantry"] if p not in current_pantry]
                if not missing_pantry:
                    st.success("All seasonings available!")
                else:
                    st.warning(f"Need: {', '.join(missing_pantry)}")
    if not found:
        st.write("Add more items to unlock recipes.")

st.write("---")
st.caption("SmartFridge v1.1 | Student Developer Project | Calgary, AB")
