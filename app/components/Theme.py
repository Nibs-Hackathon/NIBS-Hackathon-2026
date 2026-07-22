import streamlit as st


def apply_theme():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0b1220;
            color: white;
        }


        div[data-testid="metric-container"] {

            background-color: #111827;
            border-radius: 12px;
            padding: 15px;
            border: 1px solid #1f2937;

        }


        .card {

            background-color: #111827;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #374151;

        }


        </style>
        """,
        unsafe_allow_html=True
    )