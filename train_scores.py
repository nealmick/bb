import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import datetime

path = "csv/train.csv"
test_path = "csv/test.csv"
current_time = str(time.time())

data = pd.read_csv(path)

homeScore = data['home_score'].values
visitorScore = data['visitor_score'].values
data.drop(['home_score', 'visitor_score', 'gameid'], axis=1, inplace=True)


data = data.values
data = data.astype(float)

x_train, x_test, y_train, y_test = train_test_split(data, np.column_stack((homeScore, visitorScore)), test_size=0.0001)

#x_train = tf.keras.utils.normalize(x_train, axis=1)
#x_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.Sequential([

    tf.keras.layers.Dense(512, activation='LeakyReLU'),
    tf.keras.layers.Dense(256, activation='LeakyReLU'),
    
    tf.keras.layers.Dense(2, activation='linear'),



])

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)


#creating and training model then saving
model.compile(optimizer='adamax', loss='mean_squared_error', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=30, validation_split=0.1, batch_size=16 ,callbacks=[tensorboard_callback],shuffle=True)
model.save_weights('./checkpoints/my_checkpoint')


'''
##testinged model
data = pd.read_csv(test_path)
homeTestScore = data['home_score'].values
visitorTestScore = data['visitor_score'].values
data.drop(['gameid'], axis=1, inplace=True)
data.drop(['home_score'], axis=1, inplace=True)
data.drop(['visitor_score'], axis=1, inplace=True)

data = data.values
data = data.astype(float)

def print_prediction(model,data):
    p = model.predict(data)
    c = 0
    n = 0
    for i in range(len(p)):
        correct = False
        n+=1
        if p[i][0] > p[i][1] and homeTestScore[i] > visitorTestScore[i]:
            correct = True
        elif p[i][0] < p[i][1] and homeTestScore[i] < visitorTestScore[i]:
            correct = True
        if correct:
            c+=1
            print('correct - predicted:',round(p[i][0]),round(p[i][1]),'=',round(p[i][0]-p[i][1]),' actual:' ,homeTestScore[i],visitorTestScore[i],'=',round(homeTestScore[i]-visitorTestScore[i]))
        if not correct:
            print('wrong - predicted:',round(p[i][0]),round(p[i][1]),'=',round(p[i][0]-p[i][1]),' actual:' ,homeTestScore[i],visitorTestScore[i],'=',round(homeTestScore[i]-visitorTestScore[i]))

    print('percent correct winners: ', c/n*100,'%')
print_prediction(model, data)
'''
