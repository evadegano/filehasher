import streamlit as st
import base64
import hashlib
import pandas as pd
from pandas.errors import ParserError



def main():
  # add an a title to the app
  st.title("FileHasher")

  # add a file picker
  uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

  if st.button("Hash in MD5"):
    if uploaded_file is not None:
      my_hash(uploaded_file)

  if st.button("Hash in SHA256"):
    if uploaded_file is not None:
      my_hash(uploaded_file)


# hash file data
def my_hash(uploaded_file):
  try:
    df = pd.read_csv(uploaded_file, encoding='latin-1')
  except ParserError:
    df = pd.read_csv(uploaded_file, encoding='latin-1', sep=";")

  df.columns = ["md5"]

  # filter out rows with NaN values
  df = df.loc[df.md5.notnull()]
  # filter out rows that don't contain an email address
  df = df.loc[df.md5.str.contains("@")]

  # clean row
  df["md5"] = df.md5.str.lower().str.strip()

  # hash row
  df["md5"] = df.md5.apply(lambda x: hashlib.md5(x.encode()).hexdigest())

  # export hashed csv
  csv = df.to_csv(index = False)

  # byte conversion necessary for download
  b64 = base64.b64encode(csv.encode()).decode()

  # download file
  href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as <account_name>_init.csv)'
  st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()