import streamlit as st
from processor import process_file
from io import BytesIO

# This is the main Streamlit app file. It handles the user interface for uploading
# the REDCap Excel file and downloading the processed wide (landscape) format file.

# load CSS for styling
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


st.set_page_config(page_title="REDCap Wide Converter", layout="centered")

st.title("REDCap Excel Converter")
st.write("Upload your Excel file **make sure it's named 'input.xlsx'** and then download the converted version!")

uploaded_file = st.file_uploader(
    "Upload Excel file",
    type=["xlsx"]
)

if uploaded_file is not None:
    try:
        output_df = process_file(uploaded_file)

        buffer = BytesIO()
        output_df.to_excel(buffer, index=False)
        buffer.seek(0)

        st.success("File processed successfully!")

        st.download_button(
            label="Download processed file",
            data=buffer,
            file_name="output_wide.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error("Something went wrong:")
        st.exception(e)

# Made with ❤️ by Zuhal