import streamlit as st
import plotly.graph_objects as go
import time

time_sleep = 1  # Delay for smoother transitions

# Define scenarios
scenarios = [
    {
        "red_indices": [0, 3, 6],
        "question": "Which one do you prefer?",
        "options": [
            "Να κερδίσω €10 αν η μπάλα είναι 🔴 Κόκκινη, διαφορετικά €0",
            "Να κερδίσω €10 αν η μπάλα είναι ⚫ Μαύρη, διαφορετικά €0"
        ]
    },
    {
        "red_indices": [0, 3, 6],
        "question": "Which one do you prefer?",
        "options": [
            "Να κερδίσω €10 αν η μπάλα είναι 🔴 Κόκκινη Η' 🟡 Κίτρινη, διαφορετικά €0",
            "Να κερδίσω €10 αν η μπάλα είναι ⚫ Μαύρη Η'  🟡 Κίτρινη, διαφορετικά €0"
        ]
    }
]

def ellsberg_task():
    """Ellsberg task logic integrated with global session_state['responses']"""

    if "ellsberg_stage" not in st.session_state:
        st.session_state["ellsberg_stage"] = 0  # Track which question we're on

    # ✅ Ensure unified response storage
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []

    scenario = scenarios[st.session_state["ellsberg_stage"]]

    st.header("Ερώτηση 1")
    st.markdown("""
    Φαντάσου ένα κουτί με 9 μπάλες, όπως αυτό που φαίνεται παρακάτω. Τρεις από τις μπάλες είναι κόκκινες, ενώ οι υπόλοιπες έξι μπορεί να είναι είτε κίτρινες είτε μαύρες σε άγνωστη αναλογία.

    Το λογισμικό έχει προγραμματιστεί να προσομοιώνει την κλήρωση μιας μπάλας από αυτό το κουτί, με τρόπο παρόμοιο με το πώς θα το έκανε ένας άνθρωπος (δηλαδή, τραβώντας μια μπάλα τυχαία), και σου ζητάει να στοιχηματίσεις στο χρώμα αυτής της μπάλας.

    Φαντάσου ότι μία μπάλα έχει επιλεγεί, αλλά το χρώμα της δεν σου έχει αποκαλυφθεί ακόμη.
    """)

    col1, col2 = st.columns(2)
    with col1:
        ellsberg3 = st.session_state.get("ellsberg3", "default_image.png")
        st.image(ellsberg3, use_container_width=True)

    with col2:
        st.write("Ποια επιλογή προτιμάς;")
        choice = st.radio(
            "",
            scenario["options"],
            index=None,
            key=f"ellsberg_choice_{st.session_state['ellsberg_stage']}"
        )

        if st.button("Υποβολή"):
            if choice is not None:
                # ✅ Save response in unified structure
                st.session_state["responses"].append({
                    "task": "ellsberg1",
                    "question_number": st.session_state["ellsberg_stage"] + 1,
                    "choice": choice
                })

                with st.spinner("Loading next question..."):
                    time.sleep(time_sleep)

                # Move to next stage or page
                if st.session_state["ellsberg_stage"] == 0:
                    st.session_state["ellsberg_stage"] = 1
                else:
                    st.session_state["page"] += 1  # Go to next main page

                st.rerun()
            else:
                st.warning("Χρειάζεται μια απάντηση για να συνεχίσεις.")
