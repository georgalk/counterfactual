import streamlit as st
import plotly.graph_objects as go


def display_lotteries(A1, A2, p, B1, B2, q):
    st.title("Ερώτηση 3")
    st.markdown(
        f"Σκέψου τις παρακάτω δύο λοταρίες:\n\n"
        f"Η Λοταρία A πληρώνει **€{A1}** με πιθανότητα **{p}** και **€{A2}** με πιθανότητα **{1 - p}**.\n\n"
        f"Η Λοταρία B πληρώνει **€{B1}** με πιθανότητα **{q}** και **€{B2}** με πιθανότητα **{1 - q}**."
    )

    # Create pie charts
    labels_A = [f"€{A1} με", f"€{A2} με"]
    values_A = [p, 1 - p]
    labels_B = [f"€{B1} με", f"€{B2} με"]
    values_B = [q, 1 - q]

    fig_A = go.Figure(data=[go.Pie(
        labels=labels_A,
        values=values_A,
        hole=0,
        text=[f"{label} {int(prob * 100)}%" for label, prob in zip(labels_A, values_A)],
        textinfo='text',
        hoverinfo='skip'  # Optional: disables hover
    )])

    fig_B = go.Figure(data=[go.Pie(
        labels=labels_B,
        values=values_B,
        hole=0,
        text=[f"{label} {int(prob * 100)}%" for label, prob in zip(labels_B, values_B)],
        textinfo='text',
        hoverinfo='skip'
    )])

    fig_A.update_layout(showlegend=False,   font=dict(size=20) )
    fig_B.update_layout(showlegend=False,   font=dict(size=20) )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Λοταρία A")
        st.plotly_chart(fig_A, use_container_width=True)

    with col2:
        st.markdown("### Λοταρία B")
        st.plotly_chart(fig_B, use_container_width=True)

    # ✅ Initialize session state variables
    if "responses" not in st.session_state:
        st.session_state["responses"] = {}  # Store all collected responses

    if "lottery_choice" not in st.session_state:
        st.session_state["lottery_choice"] = None
    if "multiple_choice" not in st.session_state:
        st.session_state["multiple_choice"] = []
    if "free_text_reason" not in st.session_state:
        st.session_state["free_text_reason"] = ""
    if "ask_reason" not in st.session_state:
        st.session_state["ask_reason"] = False
    if "explanation_submitted" not in st.session_state:
        st.session_state["explanation_submitted"] = False
    if "reason_submitted" not in st.session_state:
        st.session_state["reason_submitted"] = False

    # ✅ Lottery selection
    if st.session_state["lottery_choice"] is None:
        st.write("Ποια λοταρία προτιμάς;")
        choice = st.radio("", ["Λοταρία A", "Λοταρία B"], index=None)

        if st.button("Υποβολή", key="submit_choice"):
            if choice is not None:
                st.session_state["lottery_choice"] = choice
                st.session_state["responses"]["Lottery Choice"] = choice  # ✅ Save response
                st.rerun()
            else:
                st.warning("Χρειάζεται μια απάντηση για να συνεχίσεις.")
    #else:
    #    st.success(f"You selected: {st.session_state['lottery_choice']}")


    # ✅ Multiple-choice question after selecting a lottery
    if st.session_state["lottery_choice"] and not st.session_state["explanation_submitted"]:
        st.write("### Τι επηρέασε την απάντηση σου? (Επέλεξε ως 2 επιλογές)")

        options = [
            "Πόσο πιθανό είναι να συμβεί το αποτέλεσμα.",
            "Πόσο πολύ αποτιμώ  το χρηματικό αποτέλεσμα.",
            "Πόσο οικεία ή άνετη είναι η επιλογή για μένα.",
            "Πόσο ριψοκίνδυνη φαίνεται η επιλογή, ανεξάρτητα από την πραγματική πιθανότητα επιτυχίας."
        ]

        selected_options = []
        for option in options:
            if st.checkbox(option, key=f"checkbox_{option}"):
                selected_options.append(option)

        # ✅ Submit multiple-choice selection
        if st.button("Υποβολή", key="submit_explanation"):
            if 1 <= len(selected_options) <= 2:
                st.session_state["multiple_choice"] = selected_options
                st.session_state["responses"]["Factors Considered"] = selected_options  # ✅ Save response
                st.session_state["explanation_submitted"] = True

                # ✅ If both first two options were selected, proceed
                if all(opt in selected_options for opt in options[:2]):
                    st.session_state["next_step_ready"] = True
                    st.session_state["page"] += 1
                else:
                    st.session_state["ask_reason"] = True  # ✅ Ask for reasoning if not both first two options

                st.rerun()
            else:
                st.warning("⚠️ Χρειάζεται να επιλέξεις τουλάχιστον 1 και το πολύ 2 επιλογές για να συνεχίσεις.")

    # ✅ Show free-text input only if reasoning is required and not yet submitted
    if st.session_state.get("ask_reason", False) and not st.session_state["reason_submitted"]:
        st.write("### Γιατί δεν επέλεξες μια απο τις δυο πρώτες επιλογές (Πόσο πιθανό είναι να συμβεί το αποτέλεσμα ή Πόσο πολύ αποτιμώ  το χρηματικό αποτέλεσμα);")

        free_text_input = st.text_area("Λόγος:", value=st.session_state.get("free_text_reason", ""))

        # ✅ Submit free-text explanation
        if st.button("Υποβολή", key="submit_reason"):
            if free_text_input.strip():
                st.session_state["free_text_reason"] = free_text_input
                st.session_state["responses"]["Reasoning"] = free_text_input  # ✅ Save response
                st.session_state["reason_submitted"] = True  # Mark as submitted
                st.session_state["ask_reason"] = False  # Hide reason box
                st.session_state["page"] += 1
                st.rerun()
            else:
                st.warning("⚠️ Παρακαλώ συμπλήρωσε το πεδίο για να συνεχίσεις.")

