
import streamlit as st
import pandas as pd

# Load data (updated with all sections and extras)
data = [
    {"Section": "Bathroom", "Size": "Half", "Price": 50},
    {"Section": "Bathroom", "Size": "Full", "Price": 95},
    {"Section": "Bathroom", "Size": "Master", "Price": 120},
    {"Section": "Bedroom", "Size": "Regular", "Price": 40},
    {"Section": "Bedroom", "Size": "Large", "Price": 60},
    {"Section": "Closet", "Size": "Standard", "Price": 30},
    {"Section": "Dining Room", "Size": "Standard", "Price": 70},
    {"Section": "Hallway", "Size": "Standard", "Price": 25},
    {"Section": "Laundry Room", "Size": "Standard", "Price": 45},
    {"Section": "Office", "Size": "Standard", "Price": 60},
    {"Section": "Stairs", "Size": "Standard", "Price": 35},
    {"Section": "Kitchen", "Size": "Regular", "Price": 70},
    {"Section": "Kitchen", "Size": "Large", "Price": 100},
]

kitchen_extras = {
    "Oven": 40,
    "Fridge": 80,
    "Stove": 60,
    "Microwave": 20,
    "Range Hood": 50,
}

df = pd.DataFrame(data)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'quantity_value' not in st.session_state:
    st.session_state.quantity_value = 1

st.title("Cleaning Quote Calculator")
st.write("Select the areas, sizes, quantities, and kitchen extras to generate a cleaning quote in real time.")

# Select section
section = st.selectbox("Choose a section", df['Section'].unique())

# Select size
available_sizes = df[df['Section'] == section]['Size'].unique()
size = st.selectbox("Choose a size", available_sizes)

# Quantity input
quantity = st.number_input("Quantity", min_value=1, step=1, key="quantity_value")

# Price calculation
price = df[(df['Section'] == section) & (df['Size'] == size)]['Price'].values[0]
total_price = price * quantity
st.markdown(f"### Price: ${price} x {quantity} = ${total_price}")

# Kitchen extras selection
selected_extras = []
kitchen_extras_total = 0
if section == "Kitchen" and size in ["Regular", "Large"]:
    st.subheader("Kitchen Extras")
    for extra, extra_price in kitchen_extras.items():
        selected = st.checkbox(f"Add {extra} (${extra_price})", key=f"chk_{extra}")
        if selected:
            qty = st.number_input(f"Quantity for {extra}", min_value=1, step=1, key=f"qty_{extra}")
            selected_extras.append({"Extra": extra, "Unit Price": extra_price, "Quantity": qty, "Total": extra_price * qty})
            kitchen_extras_total += extra_price * qty

# Callback to reset quantity
def reset_quantity():
    st.session_state.quantity_value = 1

# Add to quote
if st.button("Add to Quote", on_click=reset_quantity):
    st.session_state.cart.append({
        "Section": section,
        "Size": size,
        "Quantity": quantity,
        "Unit Price": price,
        "Total": total_price
    })
    for extra in selected_extras:
        st.session_state.cart.append({
            "Section": f"Kitchen Extra - {extra['Extra']}",
            "Size": "",
            "Quantity": extra["Quantity"],
            "Unit Price": extra["Unit Price"],
            "Total": extra["Total"]
        })
    st.rerun()

# Display quote with delete buttons
if st.session_state.cart:
    st.subheader("Current Quote")
    for i, item in enumerate(st.session_state.cart):
        cols = st.columns([4, 2, 2, 2, 2, 1])
        cols[0].write(item['Section'])
        cols[1].write(item['Size'])
        cols[2].write(item['Quantity'])
        cols[3].write(f"${item['Unit Price']}")
        cols[4].write(f"${item['Total']}")
        if cols[5].button("❌", key=f"del_{i}"):
            st.session_state.cart.pop(i)
            st.rerun()

    grand_total = sum(item['Total'] for item in st.session_state.cart)
    st.markdown(f"## Total: ${grand_total}")

# Reset entire cart
if st.button("Reset Quote"):
    st.session_state.cart = []
    st.session_state.quantity_value = 1
    st.rerun()
