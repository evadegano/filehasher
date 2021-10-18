import streamlit as st
import base64
import os
import hashlib
import pandas as pd



def main():
  # add an a title to the app
  st.title("File Hash")

  # add a file picker
  uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

  # check whether file is for DPAM or SMJ
  targets = [
    "smj",
    "dpam",
  ]

  if st.button("Hash"):
    if uploaded_file is not None:
      for target in targets:
        if target in uploaded_file.name.lower():
            target_output = f"{target}_init.csv"
            my_hash(uploaded_file, target_output)


# hash file data
def my_hash(uploaded_file, target_output):
  df = pd.read_csv(uploaded_file)

  df.columns = ["md5"]

  # filter out rows that don't contain an email address
  df = df.loc[df.md5.str.contains("@")]

  # clean row
  df["md5"] = df.md5.str.lower().str.strip()

  # hash row
  df["md5"] = df.md5.apply(lambda x: hashlib.md5(x.encode()).hexdigest())

  # export hashed csv
  csv = df.to_csv(target_output, index = False)

  # byte conversion necessary for download
  b64 = base64.b64encode(csv.encode()).decode()

  # download file
  href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
  st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()