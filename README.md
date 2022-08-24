# NBA
This is a predictions platform that aims to put you in direct control over a cutting edge neural network.

The model uses the Tensorflow library.

This project has many functions. 
Gets today's games and displays them with live scores.
Keeps track of user predictions metrics such as loss/gain and correct/incorrect.

The model was trained over a data set containing the last 20 years of NBA games.  Each game in the data set is broken down to the 3 best players on each team.



The main function of this project is to predict future games.  Future games are identified by the teams playing and the date.  The season averages of the players for each team are gathered and the data is then prepared.  Before any predictions are made the stats of players can be modified.  The model loads the weights from training and makes a single prediction.  The prediction is in the form of a sigmoid function. That is a number in the range of 0 to 1.  0 being the away team and 1 being the home team winning.  The prediction is then stored along with the dataset used for the model to predict.  Then once the game is finished and the score is final the prediction can be marked as correct or not.



Basket Ball!


*under development*
