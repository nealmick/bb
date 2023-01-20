from __future__ import absolute_import, division, print_function, unicode_literals
import functools
import requests, time, json
import numpy as np
import pandas as pd
import tensorflow as tf
import seaborn as sns
from tensorflow.keras import *

LABEL_COLUMN = 'winner'
LABELS = [0, 1]
labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']


link = 'https://www.balldontlie.io/api/v1/stats?seasons[]=2019&game_ids[]='

def sss(labels):
    s = ''
    derp = ['home_', 'visitor_']
    for foo in derp:
        for i in range(1,4):
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
      batch_size= 25, # Artificially small to make examples easier to show.
      shuffle=False,
      label_name=LABEL_COLUMN,
      na_value="?",
      num_epochs=epochs,
      ignore_errors=True,
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
    normalizer = functools.partial(normalize_numeric_data, mean=MEAN, std=STD)
    numeric_column = tf.feature_column.numeric_column('numeric', shape=[len(NUMERIC_FEATURES)])
    numeric_columns = [numeric_column]
    numeric_layer = tf.keras.layers.DenseFeatures(numeric_columns)
    preprocessing_layer = tf.keras.layers.DenseFeatures(numeric_columns)
    return preprocessing_layer, packed_dataset


preprocessing_layer, test_dataset = prep('ffall.csv', fdsa, s,epochs =1)

model = tf.keras.Sequential([
    preprocessing_layer,
    tf.keras.layers.Dense(300, activation='relu'),
    tf.keras.layers.Dense(300, activation='relu'),
    #tf.keras.layers.Dense(1000, activation='relu'),
    #tf.keras.layers.Dense(500, activation='relu'),
    tf.keras.layers.Dense(1,activation='sigmoid'),
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adamax',
    metrics=['accuracy'])


model.load_weights('./checkpoints/my_checkpoint')
model.fit(test_dataset, epochs=0)

test_loss, test_accuracy = model.evaluate(test_dataset)
print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))

preprocessing_layer, test_dataset = prep('ffasdf.csv', fdsa, s,epochs =1)
test_loss, test_accuracy = model.evaluate(test_dataset)
print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))


c=1
w=1
for i in range(100):
    testPath= 'csv4/ffasdf'+str(i)+'.csv'
    #print(testPath)
    preprocessing_layer, test_dataset = prep(testPath, fdsa, s,epochs =1)
    test_data = test_dataset#.shuffle(500)
    #test_data = test_dataset

    #tf.saved_model.save(model, "/asdf/")
    #loaded = tf.saved_model.load("/tmp/cnn/1/")
    predictions = model.predict(test_data,steps=1)
    x = list(test_data)[0][1][:100]
    for prediction, winner in zip(predictions[:100], x):
        gameid = int(list(test_data)[0][0]['gameid'])
        foo='coinflip'
        if prediction[0] >= .5 and winner ==1:
            c+=1
            foo = 'c1'
        if prediction[0] < .5 and winner ==0:
            c+=1
            foo = 'c0'
        if prediction[0] >= .5 and winner ==0:
            w+=1
            foo='w0'
        if prediction[0] < .5 and winner ==1:
            w+=1
            foo='w1'
        print(foo,"Prediction: {:.2}".format(prediction[0]),':',int(winner),':',round((c/(c+w))*100),'%',gameid,':',i)








#############
