Premier League Tactical Analysis, which runs in the Code Institute mock terminal on Heroku.

Users can look at one of four questions, or alternatively look up a brief tactical profile of each team in the 2018/2019 premier league season.
The concept of this project is that it is the summer of the 2019 season, and you are the data scientist for a new promoted premier league team.
The manager of your team has asked you to provide some insight into four questions they have. 

The four questions are:
1. Which referees are most likely to give red cards? Who should our players be particularly careful with to not push the edges of fair play?
2. If winning a game at half time, what is the likelihood of winning that game? This information could allow the manager to consider resting certain key players during busy periods.
3. Which teams are most reliant on long ball passes in their style of play? This could influence team selection, favouring players with aerial ability.
4. Which teams are most reliant on counter attacking goals in their style of play?

![counter attack example](https://github.com/StephenPhilipOFlynn/PLDataProject3/assets/124165807/0d93f5e9-8f35-45ea-9b24-252d76b9a5a6)

The manager has also asked for a mechanism to show a short tactical overview about each specific team.

![Team information section](https://github.com/StephenPhilipOFlynn/PLDataProject3/assets/124165807/f8da6ae2-9d48-4681-99c6-21191cfd7e8a)

Features
- Data is taken from two spreadsheets of premier league football data from the 2018/2019 season.
- The user is prompted to check 1 of 4 questions, or to press 5 for the tactical summary of a particular team's style of play.
- By pressing 5, the user then types the name of the team, and 4 tactical metrics are shown from the data set.

- Input validation, the user is informed if they have selected a tactical question or team correctly or incorrectly. The user is reprompted to input if the request is not recognised.

![Start page on terminal - project 3](https://github.com/StephenPhilipOFlynn/PLDataProject3/assets/124165807/547d9c18-322b-4a9f-a9c5-c1a65bb03e6e)

Future Features
- Further tactical questions can be added. For example, an analysis of a team's propensity to cross the ball.
- Further insights could be added to each team profile.

Testing
I have manually tested the project by doing the following:
- Passed the code through a PEP8 linter and confirmed there are no significant problems. Certain lines are over 79 character limit suggestion by Pep8 but below the 99 character upper maximum it mandates.
- Tested the app in my local terminal and the Code Institute Heroku terminal.

Bugs
- Certain data fields needed to be cleaned to remove commas in numerical fields, which caused the programme to not correctly run.
- Some calculations returned incorrect values as concatenated strings. This was caught in testing, and the data turned into floats and integers so that the resulting calculations were correct.

Deployment
Steps for deployment:
- Fork or clone this repository
- Create a new Heroku app
- Set the build packs to Python and NodeJS in that order
- Link the Heroku app to the repository
- Click on deploy

Credits
- Code Institute Love Sandwiches for general guidance, including on linking google sheets, including command line inputs, functions and deployment.
- Code Institute for the heroku deployment terminal.
- Datacamp.com for tutorials on working with lists and data frames.
- Datacamp.com for sample data set 1. Dataset 1 was used for the analysis of conversion of matches if winning at half time, and of referees red card rates.
- https://app.datacamp.com/workspace/sample-datasets
- Original source for dataset 1 is quoted as data world.
- https://data.world/chas/2018-2019-premier-league-matches
- Data set 2 was from Kaggle which was used for calculations on playing styles.  This includes the analysis of counter attacks, long balls, and team profiles.
- https://www.kaggle.com/datasets/thesiff/premierleague1819
- Pep8 checker - https://www.codewof.co.nz/style/python3/
- https://peps.python.org/pep-0008/#indentation

