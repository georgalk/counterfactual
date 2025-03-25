import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Load Google Sheets API credentials correctly
credentials = st.secrets["gcp_service_account"]

# ✅ Authenticate with Google Sheets
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    return client

# ✅ Function to append data to Google Sheets
def append_to_google_sheets(df, sheet_name="ellsberg data"):
    """Appends DataFrame data as new rows to Google Sheets."""
    try:
        client = authenticate_google_sheets()
        sheet = client.open(sheet_name).sheet1  # Select the first sheet

        # ✅ Convert lists in DataFrame to comma-separated strings
        for col in df.columns:
            df[col] = df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

        # Convert DataFrame to list of lists
        data = df.values.tolist()

        # Append new data
        sheet.append_rows(data)
        return True
    except Exception as e:
        st.error(f"❌ Failed to save data to Google Sheets: {e}")
        return False

# ✅ Final Page Function
def final_page():
    """Final page for displaying and appending responses to Google Sheets."""
    st.title("Τέλος")
    st.write("Ευχαριστούμε πολύ για την συμμετοχή σου στο πείραμα αυτό. Μπορείς τώρα να κλείσεις την σελίδα.")

    # ✅ Ensure `responses` is a dictionary
    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], dict):
        st.warning("No responses found.")
        return

    # ✅ Convert `st.session_state["responses"]` into a single-row DataFrame
    df = pd.DataFrame([st.session_state["responses"]])  # Convert dict to DataFrame with one row
    st.write(df)  # Show responses in the UI

    # ✅ Append to Google Sheets
    if st.button("Save to Google Sheets"):
        if append_to_google_sheets(df):
            st.success("✅ Responses successfully appended to Google Sheets!")
        else:
            st.error("❌ Failed to save responses. Please try again.")

    # ✅ Allow CSV download
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Responses as CSV",
        data=csv_data,
        file_name="user_responses.csv",
        mime="text/csv"
    )

    # ✅ Restart button
    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
