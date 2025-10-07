import streamlit as st
def checkCode (user_input:str,language:str) :

st.title("Check for the Syntax,Compilation and Logical Error")
user_input = st.text_area("Enter your code here:")
st.write("You entered:", user_input)
language = st.text("Enter Language")


if st.button("Check Code") :
    checkCode (user_input,language)