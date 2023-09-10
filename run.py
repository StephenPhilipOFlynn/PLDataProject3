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
#rename columns to access data correctly in dataframe
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
#find which referees gave most red cards
ref_red_cards = df.groupby('Ref')['Ttl_Mtch_Red'].sum()
#find out which referee gives the most cards per game
ref_redcards_permatch = ref_red_cards / referee_appearances
# most to least
ref_redcards_permatch_desc = ref_redcards_permatch.sort_values(ascending=False)
topfour_most_red_card_refs = ref_redcards_permatch_desc.head(4)
#print top 4
print("Our players need to be particularly careful with the four referees below to avoid red cards")
print("Fouls while on second yellow cards should be particularly avoided with:")
print(topfour_most_red_card_refs)
#work out relationship between result at half-time, result at full time
#number of games in a season
total_matches = len(df)
#number of matches where result is same at full time as it was at half time
same_match_result = len(df[df['HT_Result'] == df['FT_Result']])
same_result_percentage = (same_match_result / total_matches) * 100
print(f"{same_match_result} of the premier league games finished with the same result at half time and full time.")
print(f"The likelihood that the match result at full time will be the same as the result at half time is: {same_result_percentage}%.")