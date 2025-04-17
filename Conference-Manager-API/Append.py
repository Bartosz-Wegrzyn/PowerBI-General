import os
import re
import pandas as pd
current_directory = os.getcwd()
folders = [folder for folder in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, folder))]
four_digit_folders = [folder for folder in folders if re.match(r'^\d{4}$', folder)]

def marge_files(FileName):
    df_list = []
    for folder in four_digit_folders:
        data = pd.read_excel(f"./{folder}/{FileName}.xlsx")
        df_list.append(data)
    df = pd.concat(df_list)
    df.drop_duplicates()
    df.to_excel(f"MergedData/{FileName}.xlsx", index=False)


marge_files("d_Events")
marge_files("d_Participants_Categories")
marge_files("f_Participants")
