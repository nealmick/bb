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

    tf.keras.layers.Dense(128, activation='LeakyReLU'),
    tf.keras.layers.Dense(64, activation='LeakyReLU'),
    
    tf.keras.layers.Dense(2, activation='linear'),



])

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

#model.load_weights('./checkpoints/my_checkpoint')
#creating and training model then saving
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=25, validation_split=0.2, batch_size=32 ,callbacks=[tensorboard_callback],shuffle=True)
model.save_weights('./checkpoints/my_checkpoint')



##testinged model
data = pd.read_csv(test_path)
homeTestScore = data['home_score'].values
visitorTestScore = data['visitor_score'].values
spread = data['spread'].values

data.drop(['gameid'], axis=1, inplace=True)
data.drop(['home_score'], axis=1, inplace=True)
data.drop(['visitor_score'], axis=1, inplace=True)

data = data.values
data = data.astype(float)

def print_prediction(model,data):
    p = model.predict(data)
    c = 0#count correct winners
    n = 0#count all
    s = 0#count spread correct winner
    ev = 0#count expected value



    evMargin3Count = 0#count expected 
    evMargin3 = 0# expected margin
    evMargin2Count = 0#count expected 
    evMargin2 = 0# expected margin
    evMargin1Count = 0#count e~xpected 
    evMargin1 = 0# expected margin


    for i in range(len(p)):
        correct = False#if prediction is correct winner
        spreadCorrect = False#if spread is correct winner
        pmscore = round(homeTestScore[i]-visitorTestScore[i]) #plus minus score
        pmp = p[i][0]-p[i][1]
        n+=1
        spread[i]=spread[i]*-1

        if spread[i]>0 and homeTestScore[i]>visitorTestScore[i]:
            spreadCorrect = True
            s +=1
        if spread[i]<0 and homeTestScore[i]<visitorTestScore[i]:
            s +=1
            spreadCorrect = True

        if p[i][0] > p[i][1] and homeTestScore[i] > visitorTestScore[i]:
            correct = True
        elif p[i][0] < p[i][1] and homeTestScore[i] < visitorTestScore[i]:
            correct = True
        spreadError = abs(spread[i]-pmscore)
        predictionError = abs(pmp-pmscore)
       #print(spreadError,predictionError)


        pred = '' #prediction with spread 0 or 1
        if spread[i]>pmp and pmp <0:
            pred = 0
        elif spread[i]>pmp and pmp >0:
            pred = 0
        elif spread[i]<pmp and pmp <0:
            pred = 1
        elif spread[i]<pmp and pmp >0:
            pred = 1
        swin = ''#winner with spread 0 or 1 
        if spread[i]>pmscore and pmscore <0:
            swin = 0
        elif spread[i]>pmscore and pmscore >0:
            swin = 0
        elif spread[i]<pmscore and pmscore <0:
            swin = 1
        elif spread[i]<pmscore and pmscore >0:
            swin = 1
        mcorrect = True
        if pred == 0 and swin == 0:
            ev +=1
            print('correct agaist spread',pred,swin)
        elif pred == 1 and swin == 1:
            ev +=1
            print('correct agaist spread',pred,swin)
        else:
            mcorrect = False

            print('wrong agaist spread',pred,swin)


        if abs(pmp)-abs(spread[i]) > 3 or abs(pmp)-abs(spread[i]) < -3:
            evMargin3Count+=1
            if mcorrect:
                evMargin3+=1
        if abs(pmp)-abs(spread[i]) > 2 or abs(pmp)-abs(spread[i]) < -2:
            evMargin2Count+=1
            if mcorrect:
                evMargin2+=1

        if abs(pmp)-abs(spread[i]) > 1 or abs(pmp)-abs(spread[i]) < -1:
            evMargin1Count+=1
            if mcorrect:
                evMargin1+=1


        #prediction - spread > 0 and winner 1
        #prediction - spread < 0 and winner 0
        




        print('spread:',spreadCorrect,spread[i], 'prediction: ',correct,round(p[i][0]),round(p[i][1]),'=',round(p[i][0]-p[i][1]),' actual:' ,homeTestScore[i],visitorTestScore[i],'=',pmscore)

        print('#-------------------------------------------#')
        if correct:
            c+=1
    print('percent correct winners: ', c/n*100,'%')
    print('spread percent correct winners: ', s/n*100,'%')
    print('expected value all games: ', ev/n*100,'%')
    print('expected value over 1 point margins: ',evMargin1,'/',evMargin1Count,'=', evMargin1/evMargin1Count*100,'%')
    print('expected value over 2 point margins: ',evMargin2,'/',evMargin2Count,'=', evMargin2/evMargin2Count*100,'%')
    print('expected value over 3 point margins: ',evMargin3,'/',evMargin3Count,'=', evMargin3/evMargin3Count*100,'%')
print_prediction(model, data)

