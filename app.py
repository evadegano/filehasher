import streamlit as st
import base64
import hashlib
import pandas as pd
from pandas.errors import ParserError



def main():
  # add an a title to the app
  st.title("Yo")

  # add a file picker
  uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

  if st.button("Hash in SHA256"):
    if uploaded_file is not None:
      my_hash(uploaded_file, "sha256", hashlib.sha256)

  if st.button("Hash in MD5"):
    if uploaded_file is not None:
      my_hash(uploaded_file, "md5", hashlib.md5)


# hash file data
def my_hash(uploaded_file, col_name, hashingAlgo):
  try:
    df = pd.read_csv(uploaded_file, encoding='latin-1')
  except ParserError:
    df = pd.read_csv(uploaded_file, encoding='latin-1', sep=";")

  df.columns = [col_name]

  # filter out rows with NaN values
  df = df.loc[df[col_name].notnull()]
  # filter out rows that don't contain an email address
  df = df.loc[df[col_name].str.contains("@")]

  # clean row
  df[col_name] = df[col_name].str.lower().str.strip()

  # hash row
  df[col_name] = df[col_name].apply(lambda x: hashingAlgo(x.encode()).hexdigest())

  # export hashed csv
  csv = df.to_csv(index = False)

  # byte conversion necessary for download
  b64 = base64.b64encode(csv.encode()).decode()

  # download file
  href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as <account_name>_init.csv)'
  st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()