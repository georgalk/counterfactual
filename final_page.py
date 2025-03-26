import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Load Google Sheets API credentials
credentials = st.secrets["gcp_service_account"]

def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    return client

def append_to_google_sheets(df, sheet_name="ellsberg data"):
    try:
        client = authenticate_google_sheets()
        sheet = client.open(sheet_name).sheet1

        for col in df.columns:
            df[col] = df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

        df = df.fillna("")  # Replace NaNs

        sheet.append_rows(df.values.tolist())
        return True
    except Exception as e:
        st.error(f"❌ Failed to save data to Google Sheets: {e}")
        return False

def final_page():
    st.title("Τέλος")
    st.write("Ευχαριστούμε πολύ για την συμμετοχή σου στο πείραμα αυτό. Μπορείς τώρα να κλείσεις την σελίδα.")

    if "responses" not in st.session_state or not isinstance(st.session_state["responses"], list):
        st.warning("No responses found.")
        return

    # ✅ Flatten all responses into one row
    flattened = {}
    for response in st.session_state["responses"]:
        if isinstance(response, dict):
            for key, value in response.items():
                if key in flattened:
                    count = 2
                    new_key = f"{key}_{count}"
                    while new_key in flattened:
                        count += 1
                        new_key = f"{key}_{count}"
                    flattened[new_key] = value
                else:
                    flattened[key] = value

    df = pd.DataFrame([flattened])
    df = df.fillna("")

    st.write(df)

    if st.button("Save to Google Sheets"):
        if append_to_google_sheets(df):
            st.success("✅ Responses successfully appended to Google Sheets!")
        else:
            st.error("❌ Failed to save responses.")

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Responses as CSV", data=csv_data, file_name="user_responses.csv", mime="text/csv")

    if st.button("Restart"):
        st.session_state.clear()
        st.rerun()
