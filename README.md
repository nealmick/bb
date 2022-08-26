# Basket Ball!


This project has many functions. 
Gets today's games and displays them with live scores.
Keeps track of user predictions metrics such as loss/gain and correct/incorrect.

The model was trained over a data set containing the last 20 years of NBA games.  Each game in the data set is broken down to the 3 best players on each team.



The main function of this project is to predict future games.  Future games are identified by the teams playing and the date.  The season averages of the players for each team are gathered and the data is then prepared. The model loads the weights from training and makes a single prediction.  The prediction is in the form of a sigmoid function. That is a number in the range of 0 to 1.  0 being the away team and 1 being the home team winning.  The prediction is then stored along with the dataset used for the model to predict.  Then once the game is finished and the score is final the prediction can be marked as correct or not.

#### Django apps:
1. bb - main django app
2. etc - code for index page
3. predict - logic for all predictons
4. users - handles all the users


#### other files:
1. checkpoints - stores trained weights
2. CSV - stores indevidual csv files for each prediction made
3. OBJ - stores pickle data files for quick loading player stats

*under development*
check dev server here:

http://njm.rocks:8000/home/

