import streamlit as st

def welcome():
    st.title("Welcome to the Experiment")

    st.markdown("""
    Thank you for participating in this experiment!

    In this study, you will be presented with a series of choices involving coloured balls in an urn and hypothetical rewards.  
    
    Please read each question carefully and make your choices accordingly.
    
    There are no right or wrong answers. 

    Your responses will be anonymous and used strictly for research purposes.  
    The task should take approximately **5–10 minutes** to complete.

    When you're ready to begin, click the button below.
    """)

    if st.button("Start Experiment"):
        st.session_state["page"] += 1  # Move to next page in your navigation logic
        st.rerun()
