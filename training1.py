import streamlit as st
import time

def training1():
    # ✅ Ensure session state for responses
    if "responses" not in st.session_state:
        st.session_state["responses"] = {}  # Store collected responses

    if "selected_answer" not in st.session_state:
        st.session_state["selected_answer"] = ""

    if "free_text_reason" not in st.session_state:
        st.session_state["free_text_reason"] = ""

    if "show_free_text" not in st.session_state:
        st.session_state["show_free_text"] = False  # Controls visibility of free-text box

    if "incorrect_answer_given" not in st.session_state:
        st.session_state["incorrect_answer_given"] = False  # ✅ New state to track incorrect answers

    # ✅ UI Elements
    st.header("Ερώτηση 4")
    st.markdown("""
    Συνεχίζοντας από το παράδειγμα με το κουτί, δεδομένου ότι τα χρηματικά αποτελέσματα για όλες τις επιλογές είναι ακριβώς τα ίδια, η επιλογή σου βασίζεται αποκλειστικά στην πιθανότητα να συμβεί κάθε γεγονός (δηλαδή να επιλεγεί μια μπάλα συγκεκριμένου χρώματος).

    Προφανώς, δεδομένου ότι γνωρίζουμε πως υπάρχουν 3 κόκκινες μπάλες στο κουτί, η πιθανότητα να τραβήξεις μια κόκκινη μπάλα είναι 33.3% (3/9 ή 1/3).  
    
    """)

    col1, col2 = st.columns(2)

    with col1:
        # ✅ Retrieve image path from session state
        image_path = st.session_state.get("ellsberg3", "default_image.png")
        st.image(image_path, use_container_width=True)

    with col2:
        st.markdown("### Ποια πιστεύεις ότι είναι η πιθανότητα να τραβήξεις μια μαύρη μπάλα;")

        # ✅ Dropdown options
        choices = ["", "Λιγότερο απο 33.3% (3/9)", "Ίση με 33.3% (3/9)", "Περισσότερο απο 33.3% (3/9)", "Δεν μπορεί να προσδιοριστεί"]

        # ✅ Show dropdown and submit button only if no incorrect answer was given
        if not st.session_state["incorrect_answer_given"]:
            selected_answer = st.selectbox(
                "",
                choices,
                index=choices.index(st.session_state["selected_answer"]) if st.session_state["selected_answer"] in choices else 0
            )

            # ✅ Button to validate answer
            if st.button("Υποβολή"):
                if selected_answer and selected_answer != "":
                    st.session_state["selected_answer"] = selected_answer  # Store selection
                    st.session_state["responses"]["Selected Probability"] = selected_answer  # ✅ Save response

                    if selected_answer != "Ίση με 33.3% (3/9)":
                        st.session_state["show_free_text"] = True  # Show free-text input if wrong answer
                        st.session_state["incorrect_answer_given"] = True  # ✅ Hide dropdown & button
                    else:
                        st.session_state["show_free_text"] = False  # Hide if correct
                        st.session_state["page"] += 1  # ✅ Move to next step

                    st.rerun()  # ✅ Refresh UI to update changes
                else:
                    st.warning("⚠️ Χρειάζεται μια απάντηση για να συνεχίσεις.")

    # ✅ Show free-text input **only if the answer is NOT "Equal to 3/9"**
    if st.session_state["show_free_text"]:
        st.write(
            f"### Γιατί πιστεύεις ότι η πιθανότητα να τραβηχτεί μια μαύρη μπάλα είναι '{st.session_state['selected_answer']}' δεδομένου ότι η μόνη πληροφορία που έχεις είναι ότι ο αριθμός των μαύρων μπαλών είναι μεταξύ 0 και 6;")

        # ✅ Text area for explanation
        free_text_input = st.text_area(
            "Λόγος:",
            value=st.session_state["free_text_reason"],  # ✅ Maintain session state
            key="free_text_reason_input"
        )

        # ✅ Submit explanation button
        if st.button("Υποβολή"):
            if free_text_input.strip():  # ✅ Ensure user provided input
                st.session_state["free_text_reason"] = free_text_input  # ✅ Save response
                st.session_state["responses"]["Reasoning"] = free_text_input  # ✅ Save response for Google Sheets
                st.session_state["page"] += 1  # ✅ Move to next step
                st.rerun()
            else:
                st.warning("⚠️ Πρέπει να συμπληρώσεις το πεδίο για να συνεχίσεις.")

