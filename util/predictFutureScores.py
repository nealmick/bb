#outdated no longer used
import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import datetime

path = "csv1/futureTest.csv"
current_time = str(time.time())

data = pd.read_csv(path)

data.drop(['gameid'], axis=1, inplace=True)


data = data.values
data = data.astype(float)


#x_train = tf.keras.utils.normalize(x_train, axis=1)
#x_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.Sequential([

    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    
    tf.keras.layers.Dense(2, activation='linear'),



])
model.load_weights('./checkpoints/my_checkpoint')



model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])



def print_prediction(model,data):
    p = model.predict(data)
    print(p[0])
print_prediction(model, data)
