import streamlit as st

def training2():
    """Handles the second training question and saves responses."""

    # ✅ Ensure session state for responses (as a list)
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []  # Store all collected responses as a list

    # ✅ UI Elements
    st.header("Ερώτηση 5")
    st.markdown("""
    Αφενός, γνωρίζεις ότι η πιθανότητα να τραβήξεις μία κόκκινη μπάλα είναι 33.3% (3/9), ενώ από την άλλη έχεις κάποια υπόθεση για την πιθανότητα να τραβήξεις μία μαύρη μπάλα.

    Ας υποθέσουμε για λίγο ότι η υπόθεσή σου για την πιθανότητα να τραβήξεις μία μαύρη μπάλα είναι επίσης 33.3% (3/9).

    Θα θεωρούσες την πιθανότητα 33.3% να τραβήξεις μία κόκκινη μπάλα (την οποία γνωρίζεις) πιο αξιόπιστη από την ίδια πιθανότητα για τη μαύρη μπάλα (την οποία υποθέτεις), δεδομένου ότι έχεις λιγότερη βεβαιότητα για τη δεύτερη;

    Με άλλα λόγια, νιώθεις λίγο μεγαλύτερη αβεβαιότητα για το “μαύρο” σε σχέση με το “κόκκινο”, και είναι αυτή η αβεβαιότητα ο λόγος που είσαι λιγότερο πρόθυμος/η να στοιχηματίσεις στο “μαύρο”;
    """)

    # ✅ UI Columns
    col1, col2 = st.columns(2)

    with col1:
        image_path = st.session_state.get("ellsberg3", "default_image.png")
        st.image(image_path, use_container_width=True)

    with col2:
        # Ensure previous selection is tracked
        if "agree_choice_training2" not in st.session_state:
            st.session_state["agree_choice_training2"] = ""

        agree_choice = st.selectbox(
            "Διάλεξε μια απάντηση:",
            ["", "Ναι, Μάλλον ναι", "Όχι, Μάλλον όχι"],
            key="agree_dropdown_training2"
        )

        if st.button("Υποβολή", key="submit_training2"):
            if agree_choice and agree_choice != "":
                st.session_state["agree_choice_training2"] = agree_choice

                # ✅ Append response to the list
                st.session_state["responses"].append({
                    "task": "training2",
                    "Agreement with Probability Comparison": agree_choice
                })

                st.session_state["page"] += 1
                st.rerun()
            else:
                st.warning("⚠️ Χρειάζεται μια απάντηση για να συνεχίσεις.")
