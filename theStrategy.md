Goal
Predict the winners of point spread bets with an accuracy greater than 52.5%.

What is Point Spread Betting?

Point spread betting is a method used to handicap teams in a game by giving them a value such as -2. The spread is used to level the playing field between the teams, making betting more challenging. Example game scores home 110 with -2 spread, to visitor 105 with +2 spread. In the example the home team won against the spread because 108 is greater then 105. Example game scores home 110 with -8 spread, to visitor 105 with +8 spread. In the example the visitor team won against the spread because 102 is less then 105.


Why 52.5%?

The break-even point for most bookmakers is 52.5%, which is the minimum percentage of correct bets needed to cover the 5% fee or vig that they charge. For instance, if you bet $100 on a game, you will win $190.1 or lose $100. If we bet on 100 games and win 52.5 times at $19.1 each, we break even with $1,000.

How Does Our Model Work?

Our model predicts the home and visitor scores and compares them to the point spread to determine the spread winner. The distance between the point spread and the predicted score is known as the margin. Margin is a critical metric that indicates how strong the prediction is. We track margin accuracy in three categories: margin 1, 2, and 3. A game qualifies as a margin 3 game if the predicted score is more than 3 points off the spread. For example, if the predicted score is 115 to 105 with the home team predicted to win by 10, and the spread for the home team is -6, then the margin is 4.

What is Volume and Variance?

Out of 500 games, we expect approximately 350 margin 1 games, 200 margin 2 games, and 100 margin 3 games. Volume refers to the number of games that qualify for betting out of a total number of games. Variance is the likelihood that a certain sequence of wins or losses will occur. The variance determines the risk you are willing to take. If you have $100 and bet $10 on each game, you can afford to lose 10 games in a row.
What does the model predict?

The model predicts the home and vistor scores.

What is the input for each game?
Each games is input the top 7 players by player time for each team, along with there win/loss/streak and point spread provided by FandDuel.

What is the remove player function?
Click on a player's name to remove the player from the input data. This is very usefull if players are injured.

How is the player injury data gathered?
The injury data is gathered from nba.com Injuries have an expiration date set by the doctor, however players may begin playing sooner.

What is the origin of the player season average data?
The season averages are gathered from an api available https://www.balldontlie.io/home.html#introduction

What is the origin of the team and odds data?
The team and odds data are gathered from an api available https://rapidapi.com/tank01/api/tank01-fantasy-stats/

What does margin mean?
Margin is the distance between the predicted outcome and the point spread.

What does export data do?
Export data creates a csv file containing all of your predictions.
