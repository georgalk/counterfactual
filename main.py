import streamlit as st
import plotly.graph_objects as go
import time
import random

from welcome import welcome
from ellsberg1 import ellsberg_task
from ellsberg2 import ellsberg_task2
from matching_probability import matching_probability
from lotteries import display_lotteries
from training1 import training1
from training2 import training2
from training3 import training3
from monty_hall import three_doors
from demographics import demographic_page
from final_page import final_page

# --- Initialize session state ---
if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
    st.session_state["responses"] = []

if "page" not in st.session_state:
    st.session_state["page"] = 0

# --- Assign and save version once ---
if "version" not in st.session_state:
    random_number = random.uniform(0, 1)
    st.session_state["version"] = "colours" if random_number <= 0.5 else "gray"

    st.session_state["responses"].append({
        "task": "version_assignment",
        "version": st.session_state["version"]
    })

    # Assign image paths based on version
    if st.session_state["version"] == "colours":
        st.session_state["ellsberg1"] = "images/ellsberg1.png"
        st.session_state["ellsberg3"] = "images/ellsberg3.png"
        st.session_state["ellsberg5"] = "images/ellsberg5.png"
    else:
        st.session_state["ellsberg1"] = "images/ellsberg1_gray.png"
        st.session_state["ellsberg3"] = "images/ellsberg3_gray.png"
        st.session_state["ellsberg5"] = "images/ellsberg5_gray.png"

# --- Page routing logic ---
def show_page(page):
    pages = {
        0: welcome,
        1: ellsberg_task,
        2: three_doors,
        3: lambda: display_lotteries(10, 0, 1 / 2, 15, -5, 1 / 2),
        4: training1,
        5: training2,
        6: training3,
        7: ellsberg_task2,
        8: demographic_page,
        9: final_page
    }
    return pages.get(page, lambda: st.error("Invalid page number"))()

# --- Show the current page ---
show_page(st.session_state["page"])
