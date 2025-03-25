import streamlit as st

def demographic_page():
    """
    Collects participant demographics and feedback and stores them in responses.
    """


    st.title("Τελευταίες ερωτήσεις")


    # ✅ Ensure `st.session_state["responses"]` is a dictionary before storing values
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], dict):
        st.session_state["responses"] = {}

    if "page" not in st.session_state:
        st.session_state["page"] = 1  # Ensure page tracking exists

    st.subheader("")

    # Age input
    age = st.number_input("Ηλικία", min_value=17, max_value=100, step=1, key="age")

    # Gender selection
    gender = st.selectbox(
        "Φύλο",
        [" ","Προτιμώ να απαντήσω", "Άνδρας", "Γυναίκα", "Μη δυαδικό", "Άλλο"],
        key="gender"
    )

    field_of_study = st.text_input("Πεδίο σπουδών", key="field_of_study")

    st.subheader("")

    # Purpose of the experiment (free text)
    experiment_purpose = st.text_area(
        "Ποιος νομίζεις είναι ο σκοπός του πειράματος;",
        key="experiment_purpose"
    )

    # Any difficulties or comments (free text)
    difficulties = st.text_area(
        "Αντιμετώπισες δυσκολίες κατα τη διάρκεια του πειράματος; Έχεις κάποια σχόλια;",
        key="difficulties"
    )

    # ✅ Save responses and move to the next page
    if st.button("Υποβολή"):
        # Ensure session state is a dictionary before updating
        if not isinstance(st.session_state["responses"], dict):
            st.session_state["responses"] = {}

        # Store responses
        st.session_state["responses"].update({
            "Age": str(age),  # Convert to string for consistent formatting
            "Gender": gender,
            "Field of Study": field_of_study,
            "Experiment Purpose": experiment_purpose,
            "Difficulties or Comments": difficulties
        })

        # ✅ Move to the next page
        st.session_state["page"] += 1

        st.rerun()  # Refresh UI to show the next page

