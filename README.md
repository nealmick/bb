# Basket Ball!


Developed with Python utilizing the TensorFlow library, the model is trained on over 19,000 games from the past 2 decades. The purpose of the project is to analyze and predict game outcomes, giving valuable insights to sports organizations and teams. The model is integrated with a Django web app, which provides prediction statistics, graphs, and today's games, displayed in a responsive and intuitive user interface.




The model outputs two linear values represent the home and visitor scores. The loss function is MSE, and the optimizer is Adamax.  Once training is complete the model weights are saved for use inside a Python Django web application.  The web app is used to interact with and control the model.  New predictions can be made and are identified by the teams playing and the game date.  Once a specific game is identified the players season averages are gathered and can be edited in a table.  Every game is stored by the user who created it.  Accounts keep track of statistics such as the number of predictions made,  correct predictions, percent correct, prediction gain, and loss.  The main control view is paginated by the 4 last games predicted and sorted by date.  This view also contains today's games updated with live scores, and a summary of user prediction stats with graphs.  The web app includes account creation, authentication, and reset.  

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
<img src="https://i.imgur.com/t4AEIvh.png" width="600" height="350" />

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



