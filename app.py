import streamlit as st
import os
import hashlib
import pandas as pd



def main():
  folder_output = "/Users/evadegano/Desktop/GPE"

  # add an a title to the app
  st.title("File Hash")

  targets = [
          "smj",
          "dpam",
      ]

  # add a file picker
  uploaded_file = st.file_uploader("Upload CSV", type=['csv'])

  if st.button("Hash"):
    if uploaded_file is not None:
      for target in targets:
        if target in uploaded_file.name.lower():
            target_output = os.path.join(folder_output, f"{target}_init.csv")
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
  df.to_csv(target_output, index = False)



if __name__ == "__main__":
    main()