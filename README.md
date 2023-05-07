# :basketball: Basket Ball!

A web app designed to consolidate and manage NBA data for machine learning analysis. Monitor player stats, injuries, and generate in-depth game reports while training TensorFlow predictive models. Access historical data from 19,000+ games spanning two decades, seamlessly integrated with a Django web app. Enjoy a responsive and intuitive user interface showcasing predictions, graphs, and game schedules.


# https://nbadata.cloud/




<img src="https://i.imgur.com/KIzXqh6.png" width="600" height="400" />
<img src="https://i.imgur.com/LY7u9xB.png" width="600" height="300" />
<img src="https://i.imgur.com/bisms9b.png" width="600" height="350" />
<img src="https://i.imgur.com/H4ClI69.png" width="600" height="300" />

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

# TensorBoard:  http://nbadata.cloud:6006/
Note: Tensorboard is not always live.
<img src="https://i.imgur.com/P8hmfxM.png" width="800" height="300" />
<img src="https://i.imgur.com/opg7vk4.png" width="800" height="300" />
<img src="https://i.imgur.com/Ha6OHxn.png" width="800" height="300" />
<img src="https://i.imgur.com/Zu3YQrU.png" width="800" height="300" />

# FAQ:  https://nbadata.cloud/predict/faq/

<img src="https://i.imgur.com/gd7ARVi.png" width="800" height="500" />


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


