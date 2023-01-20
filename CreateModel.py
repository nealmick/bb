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
trainPath = 'ffall.csv'


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
      batch_size= 100, # Artificially small to make examples easier to show.
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
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(8, activation='relu'),

    #tf.keras.layers.Dense(300, activation='relu'),
    #tf.keras.layers.Dense(150, activation='relu'),
    #tf.keras.layers.Dense(125, activation='relu'),
    tf.keras.layers.Dense(1,activation='sigmoid'),
])

model.compile(
    loss='binary_crossentropy',
    optimizer='adamax',
    metrics=['accuracy'])


train_data = train_dataset.shuffle(500)

print(s.count(','))
model.fit(train_data, epochs=100)
model.save_weights('./checkpoints/my_checkpoint')
preprocessing_layer, test_dataset = prep('ffasdf.csv', fdsa, s,epochs =1)
test_loss, test_accuracy = model.evaluate(test_dataset)
print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))


predictions = model.predict(test_dataset)
c=0
w=0
fdsa = ''

for prediction in predictions[:10]:
    fdsa= fdsa+ str(prediction)+','
print(fdsa)
'''

for i in range(100):
    testPath= 'csv2/ffasdf'+str(i)+'.csv'
    #print(testPath)
    preprocessing_layer, test_dataset = prep(testPath, fdsa, s,epochs =1)
    test_data = test_dataset#.shuffle(500)
    #test_data = test_dataset

    #tf.saved_model.save(model, "/asdf/")
    #loaded = tf.saved_model.load("/tmp/cnn/1/")
    predictions = model.predict(test_data)
    x = list(test_data)[0][1][:100]
    for prediction, winner in zip(predictions[:100], x):
        gameid = int(list(test_data)[0][0]['gameid'])
        foo='coinflip'
        if prediction[0] >= .55 and winner ==1:
            c+=1
            foo = 'c1'
        if prediction[0] < .45 and winner ==0:
            c+=1
            foo = 'c0'
        if prediction[0] >= .55 and winner ==0:
            w+=1
            foo='w0'
        if prediction[0] < .45 and winner ==1:
            w+=1
            foo='w1'
        print(foo,"Prediction: {:.2}".format(prediction[0]),':',int(winner),':',round((c/(c+w))*100),'%',gameid,':',i)


#--------------------

cc = 0
c=0
w=0
for batch, label in test_dataset:
    winner=int(label)
    for key, value in batch.items():
        if key == 'gameid':
            gameid = int(value)
        #print("{:20s}: {}".format(key,value.numpy()))
    if predictions[cc] >= .5 and winner ==1:
        c+=1
        foo = 'c1'
        asdf=1
    if predictions[cc] < .5 and winner ==0:
        c+=1
        foo = 'c0'
        asdf = 0
    if predictions[cc] >= .5 and winner ==0:
        w+=1
        asdf = 0
        foo='w0'
    if predictions[cc] < .5 and winner ==1:
        w+=1
        foo='w1'
        asdf=1
    print(foo,':',predictions[cc],round((c/(c+w))*100),'%',gameid)
    cc+=1



'''
'''

c=1
w=1


link = 'https://www.balldontlie.io/api/v1/stats?game_ids[]='
data = list(test_dataset)
for i in range(len(predictions)):
    winner = int(data[i][1])
    asdf=None
    gameid = int(data[i][0]['gameid'])
    foo = 'c'
    #if predictions[i] > .6 or predictions[i] <.4:
    if predictions[i] >= .5 and winner ==1:
        c+=1
        foo = 'c1'
        asdf=1
    if predictions[i] < .5 and winner ==0:
        c+=1
        foo = 'c0'
        asdf = 0
    if predictions[i] >= .5 and winner ==0:
        w+=1
        asdf = 0
        foo='w0'
    if predictions[i] < .5 and winner ==1:
        w+=1
        foo='w1'
        asdf=1
    if asdf != winner:
        print('----------------')

    url = link + str(gameid)
    r = req(url)
    h = r['data'][0]['game']['home_team_score']
    v = r['data'][0]['game']['visitor_team_score']

    if h>v:
        asdf='1'
    if h<v:
        asdf='0'

    print(foo,predictions[i],':',round((c/(c+w))*100),'%',gameid)#,'h:',h,'v:',v)

test_loss, test_accuracy = model.evaluate(test_dataset)
print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))

'''


'''

predictions = model.predict(test_data)
data = list(test_data)

c = 1
w = 1
for game in range(0,len(data)):
    gameid = int(data[game][0]['gameid'])
    winner = int(data[game][1])
    prediction = round(float(predictions[game]),3)
    rPrediction = round(prediction); rPrediction = int(rPrediction)
    cw = ''
    if rPrediction == winner:
        c+=1
        cw = ' -c'
    if rPrediction != winner:
        w+=1
        cw = ' -w'
    p = '%: '+str(round(((c/(c+w))*100)))
    str0 = 'data#:'+str(game)
    str1 = ', gID:'+str(gameid)
    str2 = ', prd:'+str(prediction)
    str3 = ', rPrd:'+str(rPrediction)
    str4 = ', win:'+str(winner)
    str5 = ', c:'+str(c)
    str6 = ', w:'+str(w)
    print(str0,p,str1,str2,str3,str4,str5,str6,cw)

test_loss, test_accuracy = model.evaluate(test_data)
print('\n\nTest Loss {}, Test Accuracy {}'.format(test_loss, test_accuracy))



print(predictions)
print(len(predictions))

a = list(test_data)
#print(a)
print(len(a),'------------')
print(len(a[0][1]))
print(a[0][0])

#dee data is here m8: a[0][0]
#dee winner is here m8: a[0][1]
#



for i in range(0,len(a)):
    gameid = int(a[i][0]['gameid'][0])
    print('GameID: ',gameid)

'''
#print(int(a[1][1]))
'''











print(len(a[0][0]['gameid']),'-----------------')
for x in range(len(a[0][0]['gameid'])):
    print(x)
    gameid = int(a[0][0]['gameid'][x])
    print(gameid)
'''

#predictions = model.predict(test_data)
#print(len(predictions))
#print(predictions[1])

'''
for i in range(10):
    predictions = model.predict(test_data)
    print(len(predictions),'--------------')
    a = list(test_data)
    winners = list(a[0][1])
    for x in range(len(a[0][0]['gameid'])):
        winner = int(a[0][1][x])
        gid = int(a[0][0]['gameid'][x])
        url = link + str(gid)
        h=0
        v=0
        print('gameid: ', gid)
        print('print winner: ',winner)
        print(predictions[x])
        #predictions[x] = predictions[x]*.2
        #print(predictions[x])
        if predictions[x] >= .5 and  winner== 1:
            print('correct')
            if h < v:
                print('***********************************')

            c+=1
        if predictions[x] < .5 and winner == 0:
            if h > v:
                print('***********************************')
            print('correct')
            c+=1
        if predictions[x] < .5 and winner == 1:
            print('incorrect')
            if h < v:
                print('***********************************')
            w+=1
        if predictions[x] > .5 and winner == 0:
            print('incorrect')
            if h > v:
                print('***********************************')
            w+=1

        print('c: ',c)
        print('w: ',w)
        num = c + w
        print("correct percent: ",c/num*100)
        print('-----------------------------')

        r = req(url)
        h = r['data'][0]['game']['home_team_score']
        v = r['data'][0]['game']['visitor_team_score']
        print(h)
        print(v)


'''

#print('\n\nTest Accuracy {}'.format(test_accuracy))
#r = model.predict(test_data)
#print(dict(zip(model.metrics_names, r)))
#model.fit(test_data)

#predictions = model.predict(test_data)
#print(len(predictions))
