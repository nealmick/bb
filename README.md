# Basket Ball!

Working on model to target scores!

The model predicts NBA game winners in the form of a sigmoid function. First, data is collected for games from the past two decades via an API. Over 20,000 unique games are gathered, organized neatly, and stored.  Each player has 17 total data points.  The top 3 players from each team are selected to be input for each game.  

The model is created using Google's Tensorflow library. The model is a series of 3 sequential layers. The first two layers are made up of 300 dense neurons with a ReLU activation function. The last layer is one dense neuron with a sigmoid activation representing the home or away team winning. The loss function is binary cross entropy, and the optimizer is Adamax.  Once training is complete the model weights are saved for use inside a Python Django web application.  

The web app is used to interact with and control the model.  New predictions can be made and are identified by the teams playing and the game date.  Once a specific game is identified the players season averages are gathered and can be edited in a table.  Every game is stored by the user who created it.  Accounts keep track of statistics such as the number of predictions made,  correct predictions, percent correct, prediction gain, and loss.  The main control view is paginated by the 4 last games predicted and sorted by date.  This view also contains today's games updated with live scores, and a summary of user prediction stats with graphs.  The web app includes account creation, authentication, and reset.  

The project is under development...


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
# Live: https://nbadata.cloud/




<img src="https://i.imgur.com/KIzXqh6.png" width="600" height="400" />
<img src="https://i.imgur.com/LY7u9xB.png" width="600" height="300" />


#### Install:
```bash
git clone https://github.com/nealmick/bb
cd bb

python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

python3 manage.py makemigrations predict users
python3 manage.py migrate
python3 manage.py createsuperuser


python3 manage.py runserver

http://localhost:8000/admin
http://localhost:8000/

```
*under development*
API used: https://www.balldontlie.io/



