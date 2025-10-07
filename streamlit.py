import streamlit as st
import requests
def checkCode (language:str,code:str) :
    try :
        payload = {"language":language,"code":user_input}
        api_url = 
        reponse = requests.post(api_url,json=payload)
        reponse.raise_for_status()
        data = reponse.json()
        return data
    except requests.exceptions.RequestException as e :
        st.error(f"Error calling API: {e}")
        return data

st.title("Check for the Syntax,Compilation and Logical Error")
user_input = st.text_area("Enter your code here:")
st.write("You entered:", user_input)
language = st.text("Enter Language")


if st.button("Check Code") :
    checkCode (user_input,language)
    if (user_input.strip() and language.strip()) :
        answer = checkCode(user_input,language)
        if answer :
            st.subheader("Response:")
            st.write(answer)
    
    else :
        st.warning("Please enter a question before searching")