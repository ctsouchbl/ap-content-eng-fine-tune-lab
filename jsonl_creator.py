import streamlit as st
import json
import pandas as pd

# Page configuration
st.set_page_config(page_title="JSONL Creator for Azure OpenAI", layout="wide")

# Title
st.title("Azure OpenAI Fine-Tuning Dataset Lab 🧪")

# Description
st.markdown("""
This app helps you create JSONL files for fine-tuning Azure OpenAI GPT models. 
Fill in the **System Message**, **User Message**, and **Assistant Message** fields below, then export the data as a `.jsonl` file.
""")

# Data storage
if "data" not in st.session_state:
    st.session_state.data = []

# Input form
with st.form("entry_form"):
    st.subheader("Add New Entry")
    system_message = st.text_area(
        "System Message", 
        placeholder="Enter the system instructions or guidelines here"
    )
    user_message = st.text_area(
        "User Message", 
        placeholder="Enter the user's input message here"
    )
    assistant_message = st.text_area(
        "Assistant Message", 
        placeholder="Enter the assistant's response here"
    )
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        if system_message and user_message and assistant_message:
            entry = {
                "messages": [
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": assistant_message},
                ]
            }
            st.session_state.data.append(entry)
            st.success("Entry added successfully!")
        else:
            st.error("All fields are required.")

# Display current entries
st.subheader("Current Entries")
if st.session_state.data:
    df = pd.DataFrame([
        {
            "System": entry["messages"][0]["content"],
            "User": entry["messages"][1]["content"],
            "Assistant": entry["messages"][2]["content"],
        }
        for entry in st.session_state.data
    ])
    st.table(df)

    # Download JSONL
    st.subheader("Download JSONL File")
    jsonl_data = "\n".join([json.dumps(item) for item in st.session_state.data])
    st.download_button(
        label="Download JSONL",
        data=jsonl_data,
        file_name="fine_tuning_data.jsonl",
        mime="application/jsonl",
    )
else:
    st.info("No entries added yet. Use the form above to add messages.")

# Clear all data
if st.button("Clear All Entries"):
    st.session_state.data = []
    st.success("All entries cleared!")