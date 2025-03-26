import streamlit as st
import pandas as pd

def matching_probability(optionA, optionB, probability_strings, probability_floats):
    """
    Displays a risk preference elicitation task where users choose between two lotteries.
    """

    if len(probability_strings) != len(probability_floats):
        st.error("Error: Probability string and float lists must be the same length!")
        return

    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []

    if "choices" not in st.session_state or len(st.session_state["choices"]) != len(probability_strings):
        st.session_state["choices"] = [None] * len(probability_strings)

    if "choices_submitted" not in st.session_state:
        st.session_state["choices_submitted"] = False

    if "confidence" not in st.session_state:
        st.session_state["confidence"] = None

    if "confidence_submitted" not in st.session_state:
        st.session_state["confidence_submitted"] = False

    df = pd.DataFrame({
        "Πιθανότητα (p)": probability_strings,
        "Λοταρία A": [optionA] * len(probability_strings),
        "Λοταρία B": [f"€{optionB} με πιθανότητα {p_str}" for p_str in probability_strings]
    })

    def enforce_monotonic(index, choice):
        if choice == 'B':
            for i in range(len(st.session_state.choices)):
                st.session_state.choices[i] = 'B' if i >= index else 'A'
        else:
            st.session_state.choices[index] = 'A'
            for i in range(index):
                if st.session_state.choices[i] == 'B':
                    st.session_state.choices[i] = 'A'
            for i in range(index + 1, len(st.session_state.choices)):
                if st.session_state.choices[i] == 'B':
                    st.session_state.choices[i] = None

    def on_select_A(index):
        enforce_monotonic(index, 'A')

    def on_select_B(index):
        enforce_monotonic(index, 'B')

    # Step 1: Choices
    if not st.session_state["choices_submitted"]:
        for i in range(len(df)):
            c1, c2, c3, c4 = st.columns([4, 1.5, 1.5, 4])
            c1.write(df.loc[i, 'Λοταρία A'])
            c2.checkbox("A", value=(st.session_state.choices[i] == 'A'), key=f"a_check_{i}", on_change=on_select_A, args=(i,))
            c4.write(df.loc[i, 'Λοταρία B'])
            c3.checkbox("B", value=(st.session_state.choices[i] == 'B'), key=f"b_check_{i}", on_change=on_select_B, args=(i,))

        if st.button("Υποβολή", key="proceed_confidence"):
            if None not in st.session_state.choices:
                st.session_state["choices_submitted"] = True
                st.session_state["responses"].append({
                    "task": "matching_probability",
                    "scenario": st.session_state["scenario"],
                    "stage": st.session_state["stage"],
                    "choices": st.session_state["choices"].copy()
                })
                st.rerun()
            else:
                st.warning("⚠️ Χρειάζεται μια απάντηση για να συνεχίσεις.")

    # Step 2: Confidence
    if st.session_state["choices_submitted"] and not st.session_state["confidence_submitted"]:
        st.subheader("Πόσο σίγουρος/η νιώθεις για την επιλογή σου;")
        st.session_state["confidence"] = st.select_slider(
            "Μετακίνησε την μπάρα για να δείξεις πόσο σίγουρος/η είσαι (0 = Καθόλου, 7 = Πολύ)",
            options=list(range(0, 8)),
            value=3,
            key="confidence_slider"
        )

        if st.button("Υποβολή", key="submit_final"):
            if st.session_state["confidence"] is not None:
                st.session_state["confidence_submitted"] = True
                st.session_state["responses"][-1]["confidence"] = st.session_state["confidence"]

                # Go to next stage or scenario
                if st.session_state["stage"] == 1:
                    st.session_state["stage"] = 2
                    st.session_state["choices"] = [None] * len(probability_strings)
                    st.session_state["choices_submitted"] = False
                    st.session_state["confidence_submitted"] = False
                    st.rerun()
                else:
                    if st.session_state["scenario"] < 3:
                        st.session_state["scenario"] += 1
                        st.session_state["stage"] = 1
                        st.session_state["choices"] = [None] * len(probability_strings)
                        st.session_state["choices_submitted"] = False
                        st.session_state["confidence_submitted"] = False
                        st.rerun()
                    else:
                        st.session_state["page"] += 1
                        st.rerun()

def training3():
    """
    Initializes the training task and calls `matching_probability()`
    """
    if "scenario" not in st.session_state:
        st.session_state["scenario"] = 1
    if "stage" not in st.session_state:
        st.session_state["stage"] = 1
    if "choices" not in st.session_state or not isinstance(st.session_state["choices"], list):
        st.session_state["choices"] = []
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []

    scenario_data = {
        1: {"balls": 3, "image": "ellsberg3"},
        2: {"balls": 5, "image": "ellsberg5"},
        3: {"balls": 1, "image": "ellsberg1"},
    }

    current_scenario = scenario_data[st.session_state["scenario"]]
    st.header("Ερώτηση 6")
    st.markdown(f"""
        Υπόθεσε τώρα ότι βρίσκεσαι σε μια κατάσταση όπου δεν έχεις καμία πληροφορία σχετικά με τις αναλογίες των τριών χρωμάτων στο κουτί.

        Γνωρίζεις μόνο ότι υπάρχουν 9 μπάλες μέσα στο κουτί με κόκκινο, μαύρο και κίτρινο χρώμα.

        Θα σου παρουσιάσουμε τρία σενάρια και θα σου ζητηθεί να στοιχηματίσεις τόσο σε κόκκινες όσο και σε μαύρες μπάλες.

        Βρίσκεσαι στο Σενάριο {st.session_state["scenario"]}, όπου το κουτί περιέχει {current_scenario["balls"]} κόκκινες μπάλες.
    """)

    st.subheader(f"Σενάριο {st.session_state['scenario']}: {current_scenario['balls']} Κόκκινες μπάλες")

    col1, col2 = st.columns(2)
    with col1:
        image_path = st.session_state.get(current_scenario["image"], "default_image.png")
        st.image(image_path, use_container_width=True)

    with col2:
        color_bet = "Κόκκινη" if st.session_state["stage"] == 1 else "Μαύρη"
        st.markdown(f"""
            Με την **Επιλογή Α**, κερδίζεις €10 αν τραβηχτεί μια **{color_bet}** μπάλα από το κουτί— διαφορετικά δεν κερδίζεις τίποτα.

            Με την **Επιλογή Β**, κερδίζεις €10 με κάποια πιθανότητα — διαφορετικά δεν κερδίζεις τίποτα.

            Για κάθε γραμμή, επίλεξε αν προτιμάς να κερδίσεις €10 αν τραβήξεις την αντίστοιχη μπάλα ή αν προτιμάς μια λοταρία.
        """)

    # Generate labels
    probability_strings = [f"{i} απο 9 ({round((i / 9) * 100, 1)}%)" for i in range(10)]
    probability_floats = [i / 9 for i in range(10)]

    optionA_label = f"{color_bet} μπάλα από το κουτί"
    matching_probability(optionA_label, "10", probability_strings, probability_floats)
