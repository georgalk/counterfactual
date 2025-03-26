import streamlit as st

def demographic_page():
    """
    Collects participant demographics and feedback and stores them in responses.
    """

    st.title("Τελευταίες ερωτήσεις")

    # ✅ Ensure responses is a list
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []

    if "page" not in st.session_state:
        st.session_state["page"] = 1

    st.subheader("")

    # Inputs
    age = st.number_input("Ηλικία", min_value=17, max_value=100, step=1, key="age")
    gender = st.selectbox(
        "Φύλο",
        [" ", "Προτιμώ να απαντήσω", "Άνδρας", "Γυναίκα", "Μη δυαδικό", "Άλλο"],
        key="gender"
    )
    field_of_study = st.text_input("Πεδίο σπουδών", key="field_of_study")

    st.subheader("")

    experiment_purpose = st.text_area(
        "Ποιος νομίζεις είναι ο σκοπός του πειράματος;",
        key="experiment_purpose"
    )

    difficulties = st.text_area(
        "Αντιμετώπισες δυσκολίες κατα τη διάρκεια του πειράματος; Έχεις κάποια σχόλια;",
        key="difficulties"
    )

    # Submit
    if st.button("Υποβολή"):
        # ✅ Append to list-based unified response
        st.session_state["responses"].append({
            "task": "demographics",
            "Age": str(age),
            "Gender": gender,
            "Field of Study": field_of_study,
            "Experiment Purpose": experiment_purpose,
            "Difficulties or Comments": difficulties
        })

        st.session_state["page"] += 1
        st.rerun()
