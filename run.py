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
# Check data type
data_type = type(data)
# Data is a list, turn into dataframe
df = pd.DataFrame(data)
# Skip row 1 with includes spreadsheet titles
df = df.iloc[1:]
# Rename columns to access data correctly in dataframe sheet 1
df.columns = ['Div', 'Date', 'H_Team', 'A_Team', 'FT_H_Gls', 'FT_A_Gls',
'FT_Result', 'HT_H_Gls', 'HT_A_Gls', 'HT_Result', 'Ref', 'H_Shts', 'A_Shts',
'H_Shts_Trgt', 'A_Shts_Trgt', 'H_Fouls', 'A_Fouls', 'H_Corners',
'A_Corners', 'H_Yellow', 'A_Yellow', 'H_Red', 'A_Red']

# Check second dataset accessible in terminal
datasettwo = SHEET.worksheet('Sheet2')
data_two = datasettwo.get_all_values()
# The second data set is also a list. Turn into a dataframe.
df_two = pd.DataFrame(data_two)
# Remove first row with titles for data manipulation
df_two = df_two.iloc[1:]
# Rename columns in second dataset for dataframe
df_two.columns = [
    'team', 'category', 'league_pos', 'games_televised',
    'fin_tv_revenue', 'matches_played', 'games_won', 'games_drawn',
    'general_lost', 'goals_scored', 'goals_conceded', 'total_goal_diff',
    'total_points', 'squad_size', 'squad_aver_age', 'squad_overseas',
    'fin_team_market', 'fin_market_average', 'total_passes',
    'att_passes_through', 'total_passes_long', 'att_passes_back',
    'att_crosses', 'attack_corners', 'total_shots', 'total_shots_on_target',
    'att_goals_headed', 'att_goals_pen', 'att_goals_box',
    'att_goals_outsidebox', 'total_yellow_cards', 'total_red_cards',
    'att_goals_counter', 'att_goals_freekick', 'def_saves', 'def_blocks',
    'def_intercept', 'def_tackles', 'def_tackles_last_man', 'def_clearances',
    'def_headed_clearances', 'def_penalty_conceded', 'att_poss', 'pass_acc']

# Variables for Tactical Question 1
# Firstly count referee appearances
referee_appearances = df['Ref'].value_counts()
# Convert from concatenated strings to integers
df['H_Red'] = df['H_Red'].astype(int)
df['A_Red'] = df['A_Red'].astype(int)
# Create new column total reds cards per match
df["Ttl_Mtch_Red"] = df[['H_Red', 'A_Red']].sum(axis=1)
# Find which referees gave most red cards
ref_red_cards = df.groupby('Ref')['Ttl_Mtch_Red'].sum()
# Find out which referee gives the most cards per game
ref_redcards_permatch = ref_red_cards / referee_appearances
# Most to least
ref_redcards_permatch_desc = ref_redcards_permatch.sort_values(ascending=False)
topfour_most_red_card_refs = ref_redcards_permatch_desc.head(4)

# Variables for Tactical Question 2
# Work out relationship between match result at half-time, and full time
# Number of games in a season
total_matches = len(df)
# Number of matches where result is same at full time as it was at half time
same_match_result = len(df[df['HT_Result'] == df['FT_Result']])
same_result_percentage = (same_match_result / total_matches) * 100
# Find the number of games where away team winning at half time wins
away_t_w_both_halfs = df[(df['HT_Result'] == 'A') & (df['FT_Result'] == 'A')]
away_team_win_first_half_only = df[(df['HT_Result'] == 'A') & (df['FT_Result'] != 'A')]
num_away_t_w_both_halves = len(away_t_w_both_halfs)
num_away_team_win_first_half_only = len(away_team_win_first_half_only)
# Calculate games being won by away team at half time
away_wins_first_half = (
    num_away_team_win_first_half_only + num_away_t_w_both_halves)
# Calculate percentage of away team conversions
second_half_away_conversion_rate = (
    (num_away_t_w_both_halves / away_wins_first_half) * 100)

# Same analysis on home team performances
# Find the number of games where home team winning at half time wins
h_t_win_both_halfs = df[(df['HT_Result'] == 'H') & (df['FT_Result'] == 'H')]
h_t_win_first_half_only = df[(df['HT_Result'] == 'H') & (df['FT_Result'] != 'H')]
num_home_team_win_both_halves = len(h_t_win_both_halfs)
num_home_team_win_first_half_only = len(h_t_win_first_half_only)
# Calculate games being won by home team at half time
home_wins_first_half = num_home_team_win_first_half_only + num_home_team_win_both_halves
# Calculate percentage of home team conversions
second_half_home_conversion_rate = (
    (num_home_team_win_both_halves / home_wins_first_half) * 100)

# Variables for Tactical Question 3
# Remove commmas in the two columns to perform mathematical operations
df_two['total_passes'] = df_two['total_passes'].str.replace(',', '')
df_two['total_passes_long'] = df_two['total_passes_long'].str.replace(',', '')
# Consider what teams most reliant on long passes. 
# We will compare long passes to total passes for this purpose
# First convert values to integers
df_two['total_passes_long'] = df_two['total_passes_long'].astype(int)
df_two['total_passes'] = df_two['total_passes'].astype(int)
# Divide long passes by total passes for each team
df_two['ratio_long_passes'] = df_two['total_passes_long'] / df_two['total_passes']
df_two['perc_long_passes'] = df_two['ratio_long_passes'] * 100
# Create separate dataframe of just team and their percentage of long balls
style_of_passing = df_two[['team', 'perc_long_passes']].sort_values(by='perc_long_passes', ascending=False)

# Variables for Tactical Question 4
# First convert to integer
# Find out which teams were most reliant on counter attacks proportionate to total goals
df_two['att_goals_counter'] = df_two['att_goals_counter'].astype(int)
df_two['goals_scored'] = df_two['goals_scored'].astype(int)
df_two['counter_attack_goal_perc'] = (df_two['att_goals_counter'] / df_two['goals_scored']) * 100
most_counterattacking_teams = df_two.sort_values(by='counter_attack_goal_perc', ascending=False).head(5)


def team_specifics(team_name):
    """Retrieve tactical info for specific team"""
    team_info = df_two[df_two['team'] == team_name]

    if not team_info.empty:
        print(f"Tactical info for {team_name}:")
        print(team_info[['att_poss', 'pass_acc', 'perc_long_passes', 'counter_attack_goal_perc']])
    else:
        print(f"{team_name}' not found in the data.")
        print("Please check you have entered a team name correctly")


def question_1():
    """Display calculations from question 1."""
    print("Tactical Question 1")
    print("Our players need to be particularly careful with these four referees")
    print("Overly aggressive play and fouls while on second yellow cards should be avoided with:")
    print(topfour_most_red_card_refs)


def question_2():
    """Display calculations from question 2."""
    print("Tactical Question 2")
    print("Considerations for resting players if winning at half time.")
    print(f"{same_match_result} of the premier league games finished with the same result at half time and full time.")
    print(f"The likelihood that the match result at full time will be the same as the result at half time is: {same_result_percentage}%.")
    print(f"When winning at half time, the away team went on to secure victory in {second_half_away_conversion_rate:.2f}% of games.")
    print(f"When winning at half time, the home team went on to secure victory in {second_half_home_conversion_rate:.2f}% of games.")
    print("If winning at half time, consideration should be given to resting important players, particularly if playing at our home ground.")


def question_3():
    """Display calculations from question 3."""
    print("Tactical Question 3")
    print("Which teams are most reliant on long ball passes in their style of play?")
    print("The following teams are most reliant on long balls in possession:")
    print(style_of_passing.head(5))
    print("The manager should consider relying on our most accomplished aerial players for these games.")
    print("This may assist in dealing with the opposition's higher reliance on long balls.")


def question_4():
    """Display calculations from question 4."""
    print("Tactical Question 4")
    print("Which teams are most reliant on counter attacking goals in their style of play?")
    print("The following teams are most reliant on counter attacks to score goals:")
    print(most_counterattacking_teams[['team', 'counter_attack_goal_perc']])


def tactical_questions():
    """Begins programme asks user to select choice."""
    while True:
        print(" ")
        print("Tactical analysis 2018/2019 Premier League Season")
        print("Hello and welcome. Please choose a tactical question to see the analysis")
        print("1. Referees that are most likely to give red cards.")
        print("2. Considerations for resting players if winning at half time.")
        print("3. Which teams are most reliant on long ball passes in their style of play?")
        print("4. Which teams are most reliant on counter attacking goals in their style of play?")
        print("5. Show tactical information about a specific team.")
        print("6. Reset")

        choose = input("Enter the number of the question to choose or enter 6 to exit: (eg. '1')")

        if choose == '1':
            question_1()
        elif choose == '2':
            question_2()
        elif choose == '3':
            question_3()
        elif choose == '4':
            question_4()
        elif choose == '5':
            print("We have data from last season regarding the following teams:")
            print("Manchester City, Liverpool, Chelsea, Tottenham, Arsenal, Manchester United")
            print("Wolverhampton, Everton, Leicester, West Ham, Watford, Crystal Palace, Newcastle") 
            print("Bournemouth, Burnley, Southampton, Brighton, Cardiff, Fulham, Huddersfield")
            print("eg. Manchester United")
            team_name = input("Please enter the name a team exactly: ")
            team_specifics(team_name)
        elif choose == '6':
            print("Bye for now")
        else:
            print("Invalid choice. Please enter a number from 1 to 6")


tactical_questions()








