import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import datetime

path = "csv1/test123.csv"
current_time = str(time.time())

data = pd.read_csv(path)

homeScore = data['home_score'].values
visitorScore = data['visitor_score'].values
data.drop(['home_score', 'visitor_score', 'gameid'], axis=1, inplace=True)


data = data.values
data = data.astype(float)

x_train, x_test, y_train, y_test = train_test_split(data, np.column_stack((homeScore, visitorScore)), test_size=0.1)

#x_train = tf.keras.utils.normalize(x_train, axis=1)
#x_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.Sequential([

    #tf.keras.layers.Dense(2048, activation='relu'),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    
    tf.keras.layers.Dense(2, activation='linear'),



])

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)



model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=65, validation_split=0.1, batch_size=32,callbacks=[tensorboard_callback])


def print_predictions(model, x_test, y_test):
    y_pred = model.predict(x_test)
    c = 0
    total = 0
    for i in range(len(y_pred)):
        print("Predicted home score: {:.2f} | Actual home score: {:.2f}".format(y_pred[i][0], y_test[i][0]))
        print("Predicted visitor score: {:.2f} | Actual visitor score: {:.2f}".format(y_pred[i][1], y_test[i][1]))

        if y_pred[i][0] > y_pred[i][1] and y_test[i][0] > y_test[i][1]:
            print("--------------correct-------------")
            
            c+=1
        elif y_pred[i][0] < y_pred[i][1] and y_test[i][0] < y_test[i][1]:
            print("--------------correct-------------")

            c+=1
        else:
            print("--------------wrong-------------")

        total +=1
    print("correct %:  ", (c/total)*100)

print_predictions(model, x_test, y_test)
