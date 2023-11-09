
# :basketball: [NBA Data Cloud!](https://nbadata.cloud/)

  

The platform acts as a Tensorflow wrapper that empowers you to train, and refine machine learning models with ease. Utilize our extensive historical datasets and live game statistics to develop models that can analyze patterns, forecast game outcomes, and provide a statistical edge.

  

  

<img  src="https://i.imgur.com/KIzXqh6.png"  width="600"  height="400"  />

  

<img  src="https://i.imgur.com/LY7u9xB.png"  width="600"  height="300"  />

  

<img  src="https://i.imgur.com/bisms9b.png"  width="600"  height="350"  />

  

<img  src="https://i.imgur.com/H4ClI69.png"  width="600"  height="300"  />

  

  

# Install:

  

  

```bash
  

git  clone  https://github.com/nealmick/bb

cd  bb

## install requirements


python3  -m  venv  env

  
source  env/bin/activate
  

pip  install  -r  requirements.txt


## make database
  

python3  manage.py  makemigrations  predict  users


python3  manage.py  migrate


## Create your user


python3  manage.py  createsuperuser

  
## start server
  

python3  manage.py  runserver


## admin url


http://localhost:8000/admin


## webapp url


http://localhost:8000/
  

## review your model training logs with TensorBoard:


## start tensorboard server:


tensorboard  --logdir  logs/fit


## TensorBoard URL


http://localhost:6006/


```

  

  

# [Tensorboard Server](https://nbadata.cloud/tensorboard/)

  

<img  src="https://i.imgur.com/P8hmfxM.png"  width="800"  height="300"  />

  

<img  src="https://i.imgur.com/Ha6OHxn.png"  width="800"  height="300"  />

  

<img  src="https://i.imgur.com/Zu3YQrU.png"  width="800"  height="300"  />

  

  

# System Architecture:

  

<img  src="https://i.imgur.com/gd7ARVi.png"  width="800"  height="500"  />

  

  

# Feature Correlation:

  

<img  src="https://i.imgur.com/xJMmvZR.png"  width="800"  height="400"  />

  

<img  src="https://i.imgur.com/m1xfYkb.png"  width="800"  height="600"  />

  
  
  
  
  
  
  
  
  

# Data Feature Settings

  

Understanding the data features and how they can be configured is crucial for optimizing model performance and relevance. Here's a breakdown of each feature and its role:

  

# General Overview

Our datasets encompass over 20,000 game's, each with over 500 data points. By standard, our platform ingests the season averages of the top seven players from each team based on playing time. Additionally, to capture the momentum and form of the teams, we include a detailed breakdown of the previous game's statistics for the top five players from both the featured team and their opponents, as well as the final score of that game.

  

This nuanced approach ensures that not only are the long-term trends captured through seasonal averages, but also the immediate past performance, which might give insights into the current state of the teams and players.

  

 Field Goal Three (FG3M & FG3A)

Includes both the three-point attempts and the successful three-point shots, offering insights into a team's long-range shooting ability, both in volume and accuracy.

  

 Field Goal (FGM & FGA)

Consists of field goals made (FGM) and field goals attempted (FGA), providing insight into a team's overall shooting performance and offensive effectiveness from all areas of the court.

  

 Assists (AST)

Represents the total number of assists a player averages per game. Assists are a strong indicator of a team's offensive flow and the ability of players to create scoring opportunities for each other.

  

 Blocks (BLK)

Indicates the average number of shots a player blocks per game. This stat is a measure of a player's defensive impact and the team's ability to prevent scoring by the opposition.

  

 Rebounds (DREB & OREB)

Covers two separate statistics: defensive rebounds (DREB) and offensive rebounds (OREB). Together, they paint a picture of how well a team controls the ball after a missed shot, which is crucial for both defense and second-chance points.

  

 Free Throw (FTM & FTA)

Comprises free throws made (FTM) and free throws attempted (FTA), which can be critical in close games and also serve as a proxy for a team's ability to draw fouls.

  

 Personal Foul (PF)

The average number of fouls a player commits per game. While aggressive play can lead to turnovers and disrupted plays, it can also result in fouls that give away free points and lead to players getting into foul trouble.

  

 Points (PTS)

The average number of points a player scores per game. This is the most direct measure of offensive output and a key component in predicting game scores.

  

 Steals (STL)

The average number of times a player steals the ball from the opponent. Steals can lead to fast-break opportunities and are an indicator of a team's defensive aggressiveness.

  

 Turnovers (TO)

Represents how often a player loses possession of the ball to the opposing team. Keeping turnovers low is essential for maintaining offensive efficiency.

  

 Games Played

Represents the experience stage of the season.

  

 Point Spread

The expected margin of victory according to vegas.

  

  Players Per Team

Adjusting the number of players per team considered in the dataset allows for focusing on the core lineup or a broader set of players, which may change the model's focus from star players to overall team performance.

  

  Win/Loss Streaks

Consecutive wins or losses a team has had.

  

 Win/Loss Record

Overall performance of the team throughout the season.

  
  
  
  
  
  
  
  
  
  
  
  

# Model Training Settings

  

#### Epochs

The number of epochs represents the number of complete passes through the entire training dataset. The more epochs, the more the model has a chance to learn and adjust its weights, but too many can lead to overfitting.

  

#### Batch Size

Batch size determines the number of samples that will be propagated through the network at one time. A larger batch size provides a more accurate estimate of the gradient, but it also requires more memory and may take longer to process.

  

#### Layers and Neurons

Each layer in a neural network attempts to learn different features about the data. The 'Layer Count' refers to the number of neurons in a layer. More neurons can capture more complex relationships but can also lead to overfitting and increased computational load.

  

#### Activation Functions

Activation functions like ReLU (Rectified Linear Unit) introduce non-linear properties to the network, allowing it to learn more complex data patterns. More info here

  

#### Optimizer

The optimizer is an algorithm or method used to change the attributes of the neural network, such as weights and learning rate, to reduce the losses. Optimizers like Adam combine the advantages of two other extensions of stochastic gradient descent. More info here

  

#### Early Stopping

This technique prevents overfitting by terminating the training process if the model performance stops improving on a validation dataset.

  

#### Kernel Regularizer

Regularization techniques like L1 and L2 regularization are used to prevent overfitting by penalizing the weights of the neurons.

  

#### Restore Best Weights

If enabled, this feature will restore model weights from the epoch with the best value of the monitored metric at the end of training, ensuring you keep the most optimal version of the model.

  

Note: The settings provided here are tailored for NBA data and are designed to balance the bias-variance tradeoff, ensuring the model can generalize well from training data to unseen data.

  
  
  

## Evaluation

  

The model's performance is evaluated on a series of key metrics that collectively provide a comprehensive view of its predictive power and financial efficacy when applied to real-world betting scenarios. These metrics include the Win/Loss percentage, Spread Win/Loss percentage, and various Margin-based evaluations.

  

## Win/Loss Evaluation

This metric represents the percentage of games where the model correctly predicted the winning team. It is a direct indicator of the model's ability to determine the most likely victor in a matchup without considering the point spread.

  

## Spread Win/Loss Evaluation

The Spread Win/Loss statistic indicates the frequency with which the team favored by the Vegas spread wins the game outright. For example, if Vegas sets a spread of -10 for the home team, they predict the home team will win. If the home team wins by any margin, even if it's less than 10 points, this is counted as a 'Win' for Vegas in accurately selecting the winning team. This metric solely considers the success of Vegas odds in picking the winner, not the accuracy of the spread itself, or the spread compared to predictions. In a sense this metric is not convertible.

  

## Margin-Based Evaluation

The Margin-Based Evaluation is a nuanced metric that assesses the model's predictions relative to the actual point spread of the game. Margins are set at various levels (e.g., 1, 2, 3, 4 points) to evaluate the model's performance against different thresholds of prediction strength.

  

#### For each Margin level, the following statistics are captured:

  

- Eval: Represents the count of test games the model has never seen before, providing a concrete base for the evaluation metrics.

- Win: Denotes the count of games where the model's predictions were within the spread-adjusted Margin threshold and considered as wins.

- Total: Refers to the aggregate number of games that were tested for a specific Margin threshold.

- %: The percentage of games where the model's predictions fell within the Margin threshold, reflecting prediction accuracy.

+ (Positive Variance) + : The maximum positive difference during the evaluation period between the cumulative count of games won by the model and the cumulative count of games lost, indicative of the model's winning streak at any point in the test.

-  (Negative Variance) - : The maximum negative difference during the evaluation period between the cumulative count of games lost by the model and the cumulative count of games won, indicative of the model's losing streak at any point in the test.

- Profit: The hypothetical profit or loss if one were to bet according to the model's predictions, calculated by taking the total wins, multiplying by the standard betting odds payout, and subtracting the total number of bets.

These evaluations help in understanding not just whether the model can predict winners, but also how close the predictions are to the actual outcomes, which is crucial for assessing the model's utility in betting scenarios.

  

## Graphical Representations

The evaluation section also includes visual aids such as charts and graphs that illustrate the model's performance over time, across different metrics, and in comparison to the point spread. These visuals are designed to provide users with an at-a-glance understanding of the model's predictive behavior and trends.

  

Note: Users can expect the training and evaluation process to take a few minutes, during which the model will iterate through the data to refine its predictive capabilities.

  

For more technical details on the machine learning aspects such as activation functions and optimizers, take a look at the resources provided by TensorFlow.

  
  
  
  
  
  
  
  
  

#### Django apps:

  

1. bb - main django app

  

2. etc - code for index page

  

3. predict - logic for all predictons

  

4. users - handles all the users

  

  

#### other files:

  

1. checkpoints - stores trained weights

  

2. CSV - stores individual csv files for each prediction made

  

3. OBJ - stores pickle object data files for quick loading player stats

  

  

Libraries used include Tensorflow, Numpy, Django, and Pickle.

  

  
  

  

# [About Project](https://nbadata.cloud/predict/faq/)
](https://github.com/nealmick/bb#for-each-margin-level-the-following-statistics-are-captured)
