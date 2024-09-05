
# Define set of utility functions leveraged by the notebooks

## Imports
import streamlit as st

## Define function to print the set of shareable QR codes
def print_qr_codes():
  qr_col_1, qr_col_2, qr_col_3 = st.columns(3, gap="large")
  with qr_col_1:
    st.subheader("View this repository")
    st.image("images/QR-repo.png", caption="This repository")
    st.markdown("[https://github.com/InterWorks/Snowflake-Build-2024---Schema-Evolution](https://github.com/InterWorks/Snowflake-Build-2024---Schema-Evolution)")
  with qr_col_2:
    st.subheader("View my company profile")
    st.image("images/QR-IW-profile.png", caption="My company profile")
    st.markdown("[https://interworks.com/people/chris-hastie](https://interworks.com/people/chris-hastie)")
  with qr_col_3:
    st.subheader("View my LinkedIn profile")
    st.image("images/QR-LinkedIn.png", caption="My LinkedIn profile")
    st.markdown("[https://www.linkedin.com/in/chris-hastie/](https://www.linkedin.com/in/chris-hastie/)")
