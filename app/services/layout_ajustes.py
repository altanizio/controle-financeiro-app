import streamlit as st


def remove_deploy_buttom():
    st.markdown(
        """
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stAppDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """,
        unsafe_allow_html=True,
    )


def remove_page_margin():
    st.markdown(
        """
        <style>
        header.stAppHeader {
            background-color: transparent;
        }
        section.stMain .block-container {
            padding-top: 0rem;
            z-index: 1;
        }
        </style>""",
        unsafe_allow_html=True,
    )
