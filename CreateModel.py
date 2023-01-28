from __future__ import absolute_import, division, print_function, unicode_literals
import functools
import requests, time, json
import numpy as np
import pandas as pd
import tensorflow as tf
import seaborn as sns
from tensorflow.keras import *
import datetime

LABEL_COLUMN = 'winner'
LABELS = [0, 1]
trainPath = 'test123.csv'

labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']#added min



link = 'https://www.balldontlie.io/api/v1/stats?seasons[]=2019&game_ids[]='


def sss(labels):
    s = ''
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(0,5):
            for label in labels:
                s+=foo+str(i)+'_'+label+','
    return s

foo = 'winner,gameid,'
s = sss(labels)
fdsa = foo + s

def create_columns(s):
    csv_columns = []
    a = ''
    for char in s:
        if char != ',':
            a += char
        else:
            csv_columns.append(a)
            a = ''
    return csv_columns

def defaults(fdsa):
    d = []
    for i in range(0,len(create_columns(fdsa))):
        d.append(0.0)
    return d


def get_dataset(file_path,epochs, **kwargs):
  dataset = tf.data.experimental.make_csv_dataset(
      file_path,
      batch_size= 32, # Artificially small to make examples easier to show.
      shuffle=False,
      label_name=LABEL_COLUMN,
      na_value="?",
      num_epochs=epochs,
      ignore_errors=False,
      **kwargs)
  return dataset


def show_batch(dataset):
    for batch, label in dataset:
        for key, value in batch.items():
            print("{:20s}: {}".format(key,value.numpy()))

#simple pack dont use in future...
def pack(features, label):
    return tf.stack(list(features.values()), axis=-1), label


class PackNumericFeatures(object):
  def __init__(self, names):
    self.names = names
  def __call__(self, features, labels):
    numeric_features = [features.pop(name) for name in self.names]
    numeric_features = [tf.cast(feat, tf.float32) for feat in numeric_features]
    numeric_features = tf.stack(numeric_features, axis=-1)
    features['numeric'] = numeric_features

    return features, labels
def normalize_numeric_data(data, mean, std):
    # Center the data
    return (data-mean)/std

def req(url):

    #print('request: ', url)
    r = requests.get(url)
    time.sleep(1)
    #print(r)
    return r.json()

def prep(file_path, fdsa, s,epochs):
    dataset = get_dataset(file_path, select_columns=create_columns(fdsa), column_defaults = defaults(fdsa),epochs=epochs)
    NUMERIC_FEATURES = create_columns(s)
    packed_dataset = dataset.map(PackNumericFeatures(NUMERIC_FEATURES))
    desc = pd.read_csv(file_path)[NUMERIC_FEATURES].describe()
    #print(desc)
    MEAN = np.array(desc.T['mean'])
    STD = np.array(desc.T['std'])
    #normalizer = functools.partial(normalize_numeric_data, mean=MEAN, std=STD)
    numeric_column = tf.feature_column.numeric_column('numeric', shape=[len(NUMERIC_FEATURES)])
    numeric_columns = [numeric_column]
    numeric_layer = tf.keras.layers.DenseFeatures(numeric_columns)
    preprocessing_layer = tf.keras.layers.DenseFeatures(numeric_columns)
    return preprocessing_layer, packed_dataset

preprocessing_layer, train_dataset = prep(trainPath, fdsa, s,epochs=1)

model = tf.keras.Sequential([
    preprocessing_layer,
    #tf.keras.layers.Dense(300, activation='selu'),

    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),



    #tf.keras.layers.Dense(300, activation='relu'),
    #tf.keras.layers.Dense(150, activation='relu'),
    #tf.keras.layers.Dense(125, activation='relu'),
    tf.keras.layers.Dense(1,activation='sigmoid'),
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adam',
    metrics=['accuracy'])



log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)


train_data = train_dataset.shuffle(500)
preprocessing_layer, test_dataset = prep('test.csv', fdsa, s,epochs =1)

print(s.count(','))
model.fit(train_data, epochs=75,validation_data=test_dataset, callbacks=[tensorboard_callback])
model.save_weights('./checkpoints/my_checkpoint')



test_loss, test_accuracy = model.evaluate(test_dataset,callbacks=[tensorboard_callback])
print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))


predictions = model.predict(test_dataset)
c=0
w=0
fdsa = ''

for prediction in predictions[:50]:
    fdsa= fdsa+ str(prediction)+','
print(fdsa)


