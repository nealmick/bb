# Basket Ball!


Developed with Python utilizing the TensorFlow library, the model is trained on over 19,000 games from the past 2 decades. The purpose of the project is to analyze and predict game outcomes, giving valuable insights to sports organizations and teams. The model is integrated with a Django web app, which provides prediction statistics, graphs, and today's games, displayed in a responsive and intuitive user interface.




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
<img src="https://i.imgur.com/bisms9b.png" width="600" height="350" />
<img src="https://i.imgur.com/p8ymkZU.png" width="600" height="350" />
# Install:

```bash

git clone https://github.com/nealmick/bb
cd bb

## install requirements
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

## make database
python3 manage.py makemigrations predict users
python3 manage.py migrate
## Create your user
python3 manage.py createsuperuser

## start server
python3 manage.py runserver

## admin url
http://localhost:8000/admin

## webapp url
http://localhost:8000/

## review your model training logs with TensorBoard:
## start tensorboard server:
tensorboard --logdir logs/fit
## TensorBoard URL
http://localhost:6006/



```

# TensorBoard:
<img src="https://i.imgur.com/P8hmfxM.png" width="800" height="300" />
<img src="https://i.imgur.com/opg7vk4.png" width="800" height="300" />
<img src="https://i.imgur.com/Ha6OHxn.png" width="800" height="300" />
<img src="https://i.imgur.com/Zu3YQrU.png" width="800" height="300" />

# Under Development*



API used for future team data, injuries and odds. rate limit 2000 / day :

https://rapidapi.com/tank01/api/tank01-fantasy-stats/

API used for scores, games, and season averages, both future and historical. rate limit 1 / second :

https://www.balldontlie.io/

Dataset used for historical team win/loss ratio, and odds:

https://github.com/kyleskom/NBA-Machine-Learning-Sports-Betting


