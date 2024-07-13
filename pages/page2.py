import streamlit as st

def show():
    st.title("Page 2: User Input")
    
    st.write("This page demonstrates various ways to get user input.")

    # Text input
    user_name = st.text_input("Enter your name", "")
    if user_name:
        st.write(f"Hello, {user_name}!")

    # Number input
    number = st.number_input("Enter a number", min_value=0, max_value=100, value=50)
    st.write(f"You entered: {number}")

    # Slider
    age = st.slider("Select your age", 0, 100, 25)
    st.write(f"You selected: {age}")

    # Select box
    option = st.selectbox(
        'What is your favorite color?',
        ('Red', 'Green', 'Blue', 'Yellow'))
    st.write(f'Your favorite color is {option}')

    # Multi-select
    options = st.multiselect(
        'What are your favorite fruits?',
        ['Apples', 'Bananas', 'Oranges', 'Strawberries', 'Mangoes'],
        ['Apples', 'Bananas'])
    st.write(f'You selected: {", ".join(options)}')

    # Button
    if st.button('Click me!'):
        st.write('You clicked the button!')