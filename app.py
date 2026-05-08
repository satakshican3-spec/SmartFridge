import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="SmartFridge", layout="wide")
st.title("SmartFridge: Waste-Less Kitchen")

SHELF_LIFE = {
    "Milk": 7, "Eggs": 21, "Bread": 5, "Apples": 14,
    "Spinach": 4, "Chicken": 3, "Beef": 3, "Yogurt": 14,
    "Bananas": 5, "Potatoes": 30, "Onions": 30
}

if 'inventory' not in st.session_state:
    st.session_state.inventory = []

st.subheader("Add Groceries")
item = st.selectbox("What did you buy?", list(SHELF_LIFE.keys()))

if st.button("Add to Fridge"):
    expiry_date = datetime.now() + timedelta(days=SHELF_LIFE[item])
    st.session_state.inventory.append({"item": item, "expiry": expiry_date})
    st.rerun()

st.write("---")
st.subheader("Current Inventory & Expiry Predictions")

if not st.session_state.inventory:
    st.info("Your fridge is empty. Add some groceries to start tracking!")

for i, food in enumerate(st.session_state.inventory):
    days_left = (food['expiry'] - datetime.now()).days

    col1, col2 = st.columns([0.8, 0.2])

    if days_left <= 2:
        col1.warning(f"{food['item']} - EXPIRES IN {max(0, days_left)} DAYS")
    else:
        col1.write(f"{food['item']} - Fresh for {days_left} more days")

    if col2.button("Eat / Delete", key=f"del_{i}"):
        st.session_state.inventory.pop(i)
        st.rerun()

st.write("---")
st.subheader("Recipe Suggestions")

current_items = [f['item'] for f in st.session_state.inventory]

if "Milk" in current_items and "Eggs" in current_items and "Bread" in current_items:
    st.success("You have the ingredients for: French Toast")
elif "Beef" in current_items and "Potatoes" in current_items and "Onions" in current_items:
    st.success("You have the ingredients for: Beef Stew")
elif "Eggs" in current_items and "Potatoes" in current_items:
    st.success("You have the ingredients for: Spanish Omelette")
else:
    st.info("Add more items to unlock meal suggestions based on your inventory.")
