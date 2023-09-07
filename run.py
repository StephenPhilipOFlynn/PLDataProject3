# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Premier League Data')

fulldataset = SHEET.worksheet('Sheet1')

data = fulldataset.get_all_values()
#check data type
data_type = type(data)
#data is a list, turn into dataframe
df = pd.DataFrame(data)
#skip row 1 with includes spreadsheet titles
df = df.iloc[1:]
#rename columns to access data correctly
df.columns = ['Div', 'Date', 'H_Team', 'A_Team', 'FT_H_Gls', 'FT_A_Gls', 
'FT_Result', 'HT_H_Gls', 'HT_A_Gls', 'HT_Result', 'Ref', 'H_Shts', 'A_Shts', 'H_Shts_Trgt', 
'A_Shts_Trgt', 'H_Fouls', 'A_Fouls', 'H_Corners', 'A_Corners', 'H_Yellow', 'A_Yellow', 'H_Red', 'A_Red']
#count referee appearances to begin working out which referee gives out most cards
referee_appearances = df['Ref'].value_counts()
#convert from concatenated strings to integers
df['H_Red'] = df['H_Red'].astype(int)
df['A_Red'] = df['A_Red'].astype(int)
#create new column total reds cards per match
df["Ttl_Mtch_Red"] = df[['H_Red', 'A_Red']].sum(axis=1)
print(df.loc[206])
