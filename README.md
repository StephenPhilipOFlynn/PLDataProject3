Premier League Tactical Analysis, which runs in the Code Institute mock terminal on Heroku.

Users can look at one of four questions, or alternatively look up a brief tactical profile of each team in the 2018/2019 premier league season.
The concept of this project is that it is the summer of the 2019 season, and you are the data scientist for a new promoted premier league league team.
The manager of your team has asked you to provide some insight into four questions they have. 

The four questions are:
1. Which referees are most likely to give red cards? Who should our players be particularly careful with to not push the edges of fair play?
2. If winning a game at half time, what is the likelihood of winning that game? This information could allow the manager to consider resting certain key players during busy periods.
3. Which teams are most reliant on long ball passes in their style of play? This could influence team selection, favouring players with aerial ability.
4. Which teams are most reliant on counter attacking goals in their style of play?

The manager has also asked for a mechanism to show a short tactical overview about each specific team.

Features
- Data is taken from two spreadsheets of premier league football data from the 2018/2019 season.
- The user is prompted to check 1 of 4 questions, or to press 5 for the tactical summary of a particular team's style of play.
- Input validation, the user is informed if they have selected a tactical question or team correctly or incorrectly.

Future Features
- Further tactical questions can be added. For example, an analysis of a team's propensity to cross the ball.
- Further insights could be added to each team profile.

Testing
I have manually tested the project by doing the following:
- Passed the code through a PEP8 linter and confirmed there are no significant problems
- Tested in my local terminal and the Code Institute Heroku terminal

Bugs
- Certain data fields needed to be cleaned to remove commas in numerical fields, which caused the programme to not correctly run.
- Some calculations returned incorrect values as concatenated strings. This was caught in testing, and the data turned into floats and integers so that the resulting calculations were correct.

Deployment
Steps for deployment:
- Steps for deployment:
- Fork or clone this repository
- Create a new Heroku app
- Set the build packs to Python and NodeJS in that order
- Link the Heroku app to the repository
- Click on deploy

Credits
- Code Institute Love Sandwiches for general guidance, including on linking google sheets, including command line inputs and functions.
- Code Institute for the deployment terminal.
- Datacamp.com for guidance on working with lists and data frames.
- Datacamp.com for sample data set 1. Dataset 1 was used for the analysis of conversion of matches if winning at half time, and of referees red card rates.
- https://app.datacamp.com/workspace/sample-datasets
- Original source for dataset 1 is data world.
- https://data.world/chas/2018-2019-premier-league-matches
- Data set 2 was from Kaggle which was used for calculations on playing styles.  This includes the analysis of counter attacks, long balls, and team profiles.
- https://www.kaggle.com/datasets/thesiff/premierleague1819

