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



