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


## Make a Dataset:
python3 data.py


## Train on the dataset:
## note: this will overwrite your trained weights in the checkpoints folder.
## so make a copy or change path if you dont want the web app model weights effected.
## variables to mess with would be epochs and batch size....
## If you change things like number of layers it wont integrate with web app.
## Also your training dataset can be opened with excel or somthing else here: csv/test123.csv 

python3 train_scores.py

## now review your model training logs with TensorBoard:
## start tensorboard server:
tensorboard --logdir logs/fit
## TensorBoard URL
http://localhost:6007/

```

# TensorBoard:
<img src="https://i.imgur.com/P8hmfxM.png" width="800" height="300" />
<img src="https://i.imgur.com/opg7vk4.png" width="800" height="300" />
<img src="https://i.imgur.com/Ha6OHxn.png" width="800" height="300" />
<img src="https://i.imgur.com/Zu3YQrU.png" width="800" height="300" />

# Under Development*



API used for future games played(GP), won(W), and loss(L):
https://github.com/swar/nba_api

Dataset used for past games played(GP), won(W), and loss(L):
https://github.com/kyleskom/NBA-Machine-Learning-Sports-Betting

API used for most data: https://www.balldontlie.io/ rate limit: 1 request per second

API used for spread: https://the-odds-api.com/ 

^rate limit: 500 request per month.  Okay we just hit this rate limit.  that was 500 games in like a few days guess more people using then i thought....
for now i quickly generated a new api key for the live server i will try to bypass ratelimit tonight.
if you want a local version to work go to the odds api site and get an api key, then paste here:
https://github.com/nealmick/bb/blob/074abbf42525a8c7c074a8b977cf56bd83f40a61/predict/views.py#L422




