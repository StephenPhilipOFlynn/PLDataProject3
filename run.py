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

datasetone = SHEET.worksheet('Sheet1')

data = datasetone.get_all_values()
#check data type
data_type = type(data)
#data is a list, turn into dataframe
df = pd.DataFrame(data)
#skip row 1 with includes spreadsheet titles
df = df.iloc[1:]
#rename columns to access data correctly in dataframe sheet 1
df.columns = ['Div', 'Date', 'H_Team', 'A_Team', 'FT_H_Gls', 'FT_A_Gls', 
'FT_Result', 'HT_H_Gls', 'HT_A_Gls', 'HT_Result', 'Ref', 'H_Shts', 'A_Shts', 'H_Shts_Trgt', 
'A_Shts_Trgt', 'H_Fouls', 'A_Fouls', 'H_Corners', 'A_Corners', 'H_Yellow', 'A_Yellow', 'H_Red', 'A_Red']

#check second dataset accessible in terminal
datasettwo = SHEET.worksheet('Sheet2')
data_two = datasettwo.get_all_values()
#The second data set is also a list. Turn into a dataframe. 
df_two = pd.DataFrame(data_two)
#remove first row with titles for data manipulation
df_two = df_two.iloc[1:]
#rename columns in second dataset for dataframe
df_two.columns = ['team', 'category', 'league_pos', 'games_televised', 'fin_tv_revenue', 'matches_played', 
'games_won', 'games_drawn', 'general_lost', 'goals_scored', 'goals_conceded', 'total_goal_diff', 'total_points', 'squad_size', 'squad_aver_age', 
'squad_overseas', 'fin_team_market', 'fin_market_average', 'total_passes',
'att_passes_through', 'total_passes_long', 'att_passes_back', 'att_crosses', 'attack_corners', 'total_shots', 'total_shots_on_target',
'att_goals_headed', 'att_goals_pen', 'att_goals_box', 'att_goals_outsidebox', 'total_yellow_cards', 'total_red_cards',
'att_goals_counter', 'att_goals_freekick', 'def_saves', 'def_blocks', 'def_intercept', 'def_tackles', 'def_tackles_last_man',
'def_clearances', 'def_headed_clearances', 'def_penalty_conceded', 'att_poss', 'pass_acc']

#Variables for Tactical Question 1
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

#Variables for Tactical Question 2
#work out relationship between match result at half-time, result at full time
#number of games in a season
total_matches = len(df)
#number of matches where result is same at full time as it was at half time
same_match_result = len(df[df['HT_Result'] == df['FT_Result']])
same_result_percentage = (same_match_result / total_matches) * 100
#find the number of games where away team winning at half time wins
away_team_win_both_halfs = df[(df['HT_Result'] == 'A') & (df['FT_Result'] == 'A')]
away_team_win_first_half_only = df[(df['HT_Result'] == 'A') & (df['FT_Result'] != 'A')]
count_away_team_win_both_halves = len(away_team_win_both_halfs)
count_away_team_win_first_half_only = len(away_team_win_first_half_only)
#calculate games being won by away team at half, irregardless of second half result - combine
away_wins_first_half = count_away_team_win_first_half_only + count_away_team_win_both_halves
#calculate percentage of away team conversions
second_half_away_conversion_rate = (count_away_team_win_both_halves / away_wins_first_half) * 100
#SAME ANALYSIS ON HOME TEAM
#find the number of games where home team winning at half time wins
home_team_win_both_halfs = df[(df['HT_Result'] == 'H') & (df['FT_Result'] == 'H')]
home_team_win_first_half_only = df[(df['HT_Result'] == 'H') & (df['FT_Result'] != 'H')]
count_home_team_win_both_halves = len(home_team_win_both_halfs)
count_home_team_win_first_half_only = len(home_team_win_first_half_only)
#calculate games being won by home team at half, irregardless of second half result and combine results
home_wins_first_half = count_home_team_win_first_half_only + count_home_team_win_both_halves
#calculate percentage of home team conversions
second_half_home_conversion_rate = (count_home_team_win_both_halves / home_wins_first_half) * 100

# Variables for Tactical Question 3
#remove commmas in the two columsn to perform mathematical operations
df_two['total_passes'] = df_two['total_passes'].str.replace(',', '')
df_two['total_passes_long'] = df_two['total_passes_long'].str.replace(',', '')
#consider what teams most reliant on long passes. we will compare long passes to total passes for this purpose
#first convert values to integers
df_two['total_passes_long'] = df_two['total_passes_long'].astype(int)
df_two['total_passes'] = df_two['total_passes'].astype(int)
#divide long passes by total passes for each team
df_two['ratio_long_passes'] = df_two['total_passes_long'] / df_two['total_passes']
df_two['perc_long_passes'] = df_two['ratio_long_passes'] * 100
#create separate dataframe of just team and their percentage of long balls
style_of_passing = df_two[['team', 'perc_long_passes']].sort_values(by='perc_long_passes', ascending=False)

# Variables for Tactical Question 4
#first convert to int
#find out which teams were most reliant on counter attacks as a proportion of their total goals
df_two['att_goals_counter'] = df_two['att_goals_counter'].astype(int)
df_two['goals_scored'] = df_two['goals_scored'].astype(int)
df_two['counter_attack_goal_perc'] = (df_two['att_goals_counter'] / df_two['goals_scored']) * 100
most_counterattacking_teams = df_two.sort_values(by='counter_attack_goal_perc', ascending=False).head(5)

def question_1():
    #function to show the results of the data analysis of tactical question 1
    print("Tactical Question 1")
    print("Our players need to be particularly careful with the four referees noted below to avoid red cards")
    print("Fouls while on second yellow cards should be particularly avoided with:")
    print(topfour_most_red_card_refs)

def question_2():
    #function to show the results of the data analysis of tactical question 2
    print("Tactical Question 2")
    print("Considerations for resting players if winning at half time.")
    print(f"{same_match_result} of the premier league games finished with the same result at half time and full time.")
    print(f"The likelihood that the match result at full time will be the same as the result at half time is: {same_result_percentage}%.")
    print(f"When winning at half time, the away team went on to secure victory in {second_half_away_conversion_rate:.2f}% of games.")
    print(f"When winning at half time, the home team went on to secure victory in {second_half_home_conversion_rate:.2f}% of games.")
    print("If winning at half time, consideration should be given to resting important players, particularly if playing at our home ground.")

def question_3():
    #function to show the results of the data analysis of tactical question 3
    print("Tactical Question 3")
    print("Which teams are most reliant on long ball passes in their style of play?")
    print("The following teams are most reliant on long balls in possession:")
    print(style_of_passing.head(5))
    print("The manager should consider relying on our most accomplished aerial players for these games, to deal with the opposition's higher reliance on long balls.")

def question_4():
    #fucntion to show the results of the data analysis of tactical question 4
    print("Tactical Question 4")
    print("Which teams are most reliant on counter attacking goals in their style of play?")
    print("The following teams are most reliant on counter attacks for score goals:")
    print(most_counterattacking_teams[['team', 'counter_attack_goal_perc']])

question_4()

# tactical question 4
#calculate which team most reliant on counter attacks, or quick transitions

#def team_profile():
# print("Please enter one of the team names below to get a short summary of their tactical profile. ")
 #   print("Manchester City, Liverpool, Chelsea, Tottenham, Arsenal, Manchester United, Wolverhampton, Everton, Leicester,")
  #  print("West Ham, Watford, Crystal Palace, Newcastle, Bournemouth, Burnley, Southampton, Brighton, Cardiff, Fulham, Huddersfield")
   # print("eg: Manchester United")
    #chosen_team = input("Enter a team here: ")
    #print(f"The team requested is {chosen_team}")

#team_profile()
#def main ()






