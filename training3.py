import streamlit as st
import pandas as pd


def matching_probability(optionA, optionB, probability_strings, probability_floats):
    """
    Displays a risk preference elicitation task where users choose between two lotteries.
    """

    if len(probability_strings) != len(probability_floats):
        st.error("Error: Probability string and float lists must be the same length!")
        return

    # ✅ Ensure `responses` is a list before using `.append()`
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []  # ✅ Initialize as an empty list

    if "choices" not in st.session_state or len(st.session_state["choices"]) != len(probability_strings):
        st.session_state["choices"] = [None] * len(probability_strings)

    if "choices_submitted" not in st.session_state:
        st.session_state["choices_submitted"] = False  # Tracks if checkboxes should be hidden

    if "confidence" not in st.session_state:
        st.session_state["confidence"] = None  # Stores the confidence level

    if "confidence_submitted" not in st.session_state:
        st.session_state["confidence_submitted"] = False  # Tracks if confidence was submitted

    df = pd.DataFrame({
        "Πιθανότητα (p)": probability_strings,
        "Λοταρία A": [optionA] * len(probability_strings),
        "Λοταρία B": [f"£{optionB} με πιθανότητα {p_str}" for p_str in probability_strings]
    })

    def enforce_monotonic(index, choice):
        """Enforces a single switch from A to B in the choice selection."""
        if choice == 'B':
            for i in range(len(st.session_state.choices)):
                st.session_state.choices[i] = 'B' if i >= index else 'A'
        else:
            st.session_state.choices[index] = 'A'
            for i in range(index):
                if st.session_state.choices[i] == 'B':
                    st.session_state.choices[i] = 'A'
            for i in range(index + 1, len(probability_strings)):
                if st.session_state.choices[i] == 'B':
                    st.session_state.choices[i] = None

    def on_select_A(index):
        enforce_monotonic(index, 'A')

    def on_select_B(index):
        enforce_monotonic(index, 'B')

    # ✅ Step 1: Show checkboxes if choices have not been submitted
    if not st.session_state["choices_submitted"]:
        for i in range(len(df)):
            c_A_text, c_A_check, c_B_check, c_B_text = st.columns([4, 1.5, 1.5, 4])

            c_A_text.write(df.loc[i, 'Λοταρία A'])
            c_A_check.checkbox(
                "A",
                value=(st.session_state.choices[i] == 'A'),
                key=f"a_check_{i}",
                on_change=on_select_A,
                args=(i,)
            )

            c_B_text.write(df.loc[i, 'Λοταρία B'])
            c_B_check.checkbox(
                "B",
                value=(st.session_state.choices[i] == 'B'),
                key=f"b_check_{i}",
                on_change=on_select_B,
                args=(i,)
            )

        # First button to hide checkboxes and show confidence slider
        if st.button("Υποβολή", key="proceed_confidence"):
            if None not in st.session_state.choices:  # Ensure all selections are made
                st.session_state["choices_submitted"] = True  # Hide checkboxes

                # ✅ Save choices in session state
                st.session_state["responses"].append({
                    "Scenario": st.session_state["scenario"],
                    "Stage": st.session_state["stage"],
                    "Choices": st.session_state["choices"].copy()  # Store the selections
                })

                st.rerun()
            else:
                st.error("⚠️ Χρειάζεται μια απάντηση για να συνεχίσεις.")

    # ✅ Step 2: Show confidence slider after choices are submitted
    if st.session_state["choices_submitted"] and not st.session_state["confidence_submitted"]:
        st.subheader("Πόσο σίγουρος/η νιώθεις για την επιλογή σου;")

        st.session_state["confidence"] = st.select_slider(
            "Μετακίνησε την μπάρα για να δείξεις πόσο σίγουρος/η είσαι (0 = Καθόλου σίγουρος/η, 7 = Πλήρως σίγουρος/η)",
            options=list(range(0, 8)),  # ✅ Likert scale: 0 to 7
            value=3,  # Default midpoint confidence
            key="confidence_slider"
        )

        # Second submit button to finalize confidence and proceed
        if st.button("Υποβολή", key="submit_final"):
            if st.session_state["confidence"] is not None:  # Ensure confidence is set
                st.session_state["confidence_submitted"] = True  # Mark confidence as submitted

                # ✅ Save confidence rating in session state
                st.session_state["responses"][-1]["Confidence"] = st.session_state["confidence"]

                if st.session_state["stage"] == 1:
                    st.session_state["stage"] = 2  # Move to Stage 2 (Betting on Black)
                    st.session_state["choices"] = [None] * len(probability_strings)  # Reset selections
                    st.session_state["choices_submitted"] = False  # Reset checkbox visibility
                    st.session_state["confidence_submitted"] = False  # Reset confidence for next stage
                    st.rerun()
                else:
                    # Move to the next scenario or next page
                    if st.session_state["scenario"] < 3:
                        st.session_state["scenario"] += 1  # Move to the next scenario
                        st.session_state["stage"] = 1  # Reset stage
                        st.session_state["choices"] = [None] * len(probability_strings)
                        st.session_state["choices_submitted"] = False
                        st.session_state["confidence_submitted"] = False
                        st.rerun()
                    else:
                        st.session_state["page"] += 1  # ✅ Move to the next page after all scenarios
                        st.rerun()


def training3():
    """
    Initializes the training task and calls `matching_probability()`
    """

    # ✅ Initialize session state variables
    if "scenario" not in st.session_state:
        st.session_state["scenario"] = 1  # Start at Scenario 1
    if "stage" not in st.session_state:
        st.session_state["stage"] = 1  # Start at Stage 1 (betting on Red)
    if "choices" not in st.session_state or not isinstance(st.session_state["choices"], list):
        st.session_state["choices"] = []  # Ensure choices is an empty list
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []  # ✅ Ensure responses storage is initialized as a list

    scenario_data = {
        1: {"balls": 3, "image": "ellsberg3"},
        2: {"balls": 5, "image": "ellsberg5"},
        3: {"balls": 1, "image": "ellsberg1"},
    }

    current_scenario = scenario_data[st.session_state["scenario"]]

    st.header("Ερώτηση 6")
    st.markdown(f"""
        Υπόθεσε τώρα ότι βρίσκεσαι σε μια κατάσταση όπου δεν έχεις καμία πληροφορία σχετικά με τις αναλογίες των τριών χρωμάτων στο κουτί.

        Με άλλα λόγια, γνωρίζεις μόνο ότι υπάρχουν 9 μπάλες μέσα στο κουτί με κόκκινο, μαύρο και κίτρινο χρώμα.

        Θα σου παρουσιάσουμε τρία σενάρια και Θα σου ζητηθεί να στοιχηματίσεις τόσο σε κόκκινες όσο και σε μαύρες μπάλες.
        Βρίσκεσαι στο Σενάριο {st.session_state["scenario"]}, όπου το κουτί περιέχει {current_scenario["balls"]} κόκκινες μπάλες.

        
        """)

    st.subheader(
        f"Σενάριο  {st.session_state['scenario']}: {current_scenario['balls']} Κόκκινες μπάλες")

    col1, col2 = st.columns(2)

    with col1:
        image_path = st.session_state.get(current_scenario["image"], "default_image.png")
        st.image(image_path, use_container_width=True)

    with col2:
        color_bet = "Κόκκινη" if st.session_state["stage"] == 1 else "Μαύρη"
        st.markdown(f"""
            Με την **Επιλογή Α**, κερδίζεις €10 αν τραβηχτεί μια **{color_bet}** μπάλα από το κουτί— διαφορετικά δεν κερδίζεις τίποτα.

            Με την **Επιλογή Β**, κερδίζεις €10 με κάποια πιθανότητα — διαφορετικά δεν κερδίζεις τίποτα.
            
            Για κάθε γραμμή χρειάζεται να επιλέξεις εαν προτιμάς να κερδίσεις €10 εαν τραβήξεις την αντίστοιχη μπάλα απο το κουτί, διαφορετικά τίποτα,  ή εαν προτιμάς μια λοταρία στην οποία κερδίζεις €10 με την δεδομένη πιθανότητα, διαφορετικά τίποτα.  
            """)

    probability_strings = [f"{i} απο 9 ({round((i / 9) * 100, 1)}%)" for i in range(10)]
    probability_floats = [i / 9 for i in range(10)]

    optionA_label = f"{color_bet} μπάλα απο το κουτί"

    # ✅ Run Matching Probability Function
    matching_probability(optionA_label, "10", probability_strings, probability_floats)
