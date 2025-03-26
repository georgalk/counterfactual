import streamlit as st
import matplotlib.pyplot as plt

def draw_question_marked_rectangle(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8, fill=False, edgecolor="black", linewidth=2))
    ax.text(0.5, 0.5, "?", fontsize=30, ha="center", va="center", fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

def three_doors():
    st.header("Ερώτηση 2")
    st.markdown("""
    Φαντάσου ότι βρίσκεσαι σε ένα τηλεπαιχνίδι και σου δίνεται η επιλογή ανάμεσα σε τρεις πόρτες.

    Πίσω από μία πόρτα βρίσκεται ένα αυτοκίνητο ενώ πίσω από τις άλλες δύο, τίποτα.
    Ποια είναι η πιθανότητα το αυτοκίνητο να βρίσκεται πίσω από την πόρτα 1, 2 ή 3;
    """)

    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []

    if "submitted_choices" not in st.session_state:
        st.session_state["submitted_choices"] = False
    if "submitted_explanation" not in st.session_state:
        st.session_state["submitted_explanation"] = False

    col1, col2, col3 = st.columns(3)

    fig1, ax1 = plt.subplots(figsize=(2, 2))
    draw_question_marked_rectangle(ax1)
    col1.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(2, 2))
    draw_question_marked_rectangle(ax2)
    col2.pyplot(fig2)

    fig3, ax3 = plt.subplots(figsize=(2, 2))
    draw_question_marked_rectangle(ax3)
    col3.pyplot(fig3)

    choices = ["", "0%", "50% (1/2)", "33.3% (1/3)", "100%", "Δεν μπορεί να οριστεί"]

    if not st.session_state["submitted_choices"]:
        choice1 = col1.selectbox("Πόρτα 1", choices, key="dropdown1")
        choice2 = col2.selectbox("Πόρτα 2", choices, key="dropdown2")
        choice3 = col3.selectbox("Πόρτα 3", choices, key="dropdown3")

        if st.button("Υποβολή", key="submit_choices"):
            correct = (
                choice1 == "33.3% (1/3)" and
                choice2 == "33.3% (1/3)" and
                choice3 == "33.3% (1/3)"
            )
            st.session_state["responses"].append({
                "task": "three_doors",
                "door_1": choice1,
                "door_2": choice2,
                "door_3": choice3,
                "correct": "Yes" if correct else "No"
            })

            if correct:
                st.session_state["page"] += 1
            else:
                st.session_state["submitted_choices"] = True
            st.rerun()

    if st.session_state["submitted_choices"]:
        st.write("### Θα συμφωνούσατε με την παρακάτω δήλωση;")
        st.write("'... η πιθανότητα είναι 1/3 για κάθε πόρτα.'")

        agree_choice = st.selectbox("Επιλέξτε την απάντησή σας:", ["", "Ναι, Μάλλον ναι", "Όχι, Μάλλον όχι"], key="agree_dropdown")

        if st.button("Υποβολή", key="submit_explanation") and not st.session_state["submitted_explanation"]:
            if agree_choice:
                st.session_state["responses"].append({
                    "task": "three_doors",
                    "question": "Agreement with probability statement",
                    "response": agree_choice
                })
                st.session_state["submitted_explanation"] = True
                st.session_state["page"] += 1
                st.rerun()
            else:
                st.warning("⚠️ Χρειάζεται μια απάντηση για να συνεχίσεις.")
