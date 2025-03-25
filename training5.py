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
        "Probability (p)": probability_strings,
        "Lottery A": [optionA] * len(probability_strings),
        "Lottery B": [f"£{optionB} with probability {p_str}" for p_str in probability_strings]
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

            c_A_text.write(df.loc[i, 'Lottery A'])
            c_A_check.checkbox(
                "A",
                value=(st.session_state.choices[i] == 'A'),
                key=f"a_check_{i}",
                on_change=on_select_A,
                args=(i,)
            )

            c_B_text.write(df.loc[i, 'Lottery B'])
            c_B_check.checkbox(
                "B",
                value=(st.session_state.choices[i] == 'B'),
                key=f"b_check_{i}",
                on_change=on_select_B,
                args=(i,)
            )

        # First button to hide checkboxes and show confidence slider
        if st.button("Proceed", key="proceed_confidence"):
            if None not in st.session_state.choices:  # Ensure all selections are made
                st.session_state["choices_submitted"] = True  # Hide checkboxes

                # ✅ Save choices in session state
                st.session_state["responses"].append({
                    "Stage": st.session_state["stage"],
                    "Choices": st.session_state["choices"].copy()  # Store the selections
                })

                st.rerun()
            else:
                st.error("⚠️ Please make a selection for all probabilities before proceeding.")

    # ✅ Step 2: Show confidence slider after choices are submitted
    if st.session_state["choices_submitted"] and not st.session_state["confidence_submitted"]:
        st.subheader("How confident do you feel about your choices?")

        st.session_state["confidence"] = st.select_slider(
            "Move the slider to indicate your confidence (0 = Not confident, 7 = Very confident)",
            options=list(range(0, 8)),  # ✅ Likert scale: 0 to 10
            value=3,  # Default midpoint confidence
            key="confidence_slider"
        )

        # Second submit button to finalize confidence and proceed
        if st.button("Submit", key="submit_final"):
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
                    st.success("You have completed both betting rounds!")
                    st.session_state["page"] += 1  # ✅ Move to the next page after both rounds
                    st.rerun()  # ✅ Refresh the app to display the next page
            else:
                st.warning("⚠️ Please select a confidence level before proceeding.")


def training5():
    """
    Initializes the training task and calls `matching_probability()`
    """

    # ✅ Initialize session state variables
    if "stage" not in st.session_state:
        st.session_state["stage"] = 1  # Start at Stage 1 (betting on Red)
    if "choices" not in st.session_state or not isinstance(st.session_state["choices"], list):
        st.session_state["choices"] = []  # Ensure choices is an empty list
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.session_state["responses"] = []  # ✅ Ensure responses storage is initialized as a list

    st.header("Question Training 3")
    st.markdown("""
    Suppose now you are faced with a situation in which you have no information about the relative proportions of the three colors in the urn.

    In other words, you only know that there are 9 balls inside the urn with red, black, and yellow colors.

    You will be presented with three scenarios—hypotheses that specify different possible numbers of red balls in the urn, each of which can be either true or false. 
    For each scenario, what do you believe is the probability of drawing a red ball, P(R), and the probability of drawing a black ball, P(B)?
    """)

    st.subheader(f"Scenario 1: There are 5 Red balls and 4 Black and Yellow balls - Stage {st.session_state['stage']}")

    col1, col2 = st.columns(2)
    col1, col2 = st.columns(2)

    with col1:
        image_path = st.session_state.get("ellsberg5", "default_image.png")
        st.image(image_path, use_container_width=True)

    with col2:
        color_bet = "Red" if st.session_state["stage"] == 1 else "Black"
        st.markdown(f"""
        With **Option A**, you win £10 if a **{color_bet}** ball is drawn from the urn, otherwise nothing.

        With **Option B**, you win £10 with some probability, otherwise nothing.  
        """)

    probability_strings = ["0 out of 9 (0%)", "1 out of 9 (11.1%)", "2 out of 9 (22.2%)", "3 out of 9 (33.3%)",
                           "4 out of 9 (44.4%)",
                           "5 out of 9 (55.6%)", "6 out of 9 (66.7%)", "7 out of 9 (77.8%)", "8 out of 9 (88.9%)",
                           "9 out of 9 (100%)"]
    probability_floats = [i / 9 for i in range(10)]

    optionA_label = "Red ball from the urn" if st.session_state["stage"] == 1 else "Black ball from the urn"

    # ✅ Run Matching Probability Function
    matching_probability(optionA_label, "20", probability_strings, probability_floats)
