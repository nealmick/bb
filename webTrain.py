import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import datetime




def webappTrain(modelNum,epochs,size,layer1Count,layer1Activation,layer2Count,layer2Activation,optimizer,username,es,rmw,kr):
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
    if kr =='true':


        model = tf.keras.Sequential([
            tf.keras.layers.Dense(layer1Count, activation=layer1Activation, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            tf.keras.layers.Dense(layer2Count, activation=layer2Activation, kernel_regularizer=tf.keras.regularizers.l2(0.001)),
            
            tf.keras.layers.Dense(2, activation='linear'),

        ])
    else:
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(layer1Count, activation=layer1Activation),
            tf.keras.layers.Dense(layer2Count, activation=layer2Activation),
            
            tf.keras.layers.Dense(2, activation='linear'),

        ])
    if rmw =='true':
        EarlyStopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            restore_best_weights=True,
            patience=4, verbose=0, mode='auto')
    else:       
        EarlyStopping = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            restore_best_weights=False,
            patience=4, verbose=0, mode='auto')

    log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    TensorBoard = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    #checkpoint = ModelCheckpoint(filepath='./checkpoints/my_checkpoint',save_best_only=True)
    #creating and training model then saving
    model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])
    if es =='true':
        model.fit(x_train, y_train, epochs=epochs, validation_split=0.1, batch_size=size ,callbacks=[TensorBoard,EarlyStopping],shuffle=False)
    else:
        model.fit(x_train, y_train, epochs=epochs, validation_split=0.1, batch_size=size ,callbacks=[TensorBoard],shuffle=False)

    model.save_weights('./userModels/'+username.username+'/'+str(modelNum)+'/checkpoints/my_checkpoint')



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

        evMargin6Count = 0#count expected 
        evMargin6 = 0# expected margin


        evMargin4Count = 0#count expected 
        evMargin4 = 0# expected margin

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

            margin = abs(pmp)-abs(spread[i])

            if float(pmp) < 0 and spread[i] < 0:
                print('both negative')
                #margin = pmscore+spread[i]



            if abs(margin) > 6:
                evMargin6Count+=1
                if mcorrect:
                    evMargin6+=1

            if abs(margin) > 4:
                evMargin4Count+=1
                if mcorrect:
                    evMargin4+=1

            if abs(margin) > 3:
                evMargin3Count+=1
                if mcorrect:
                    evMargin3+=1
                
            if abs(margin) > 2:

                evMargin2Count+=1
                if mcorrect:

                    evMargin2+=1

            if abs(margin) > 1:
                
                evMargin1Count+=1
                if mcorrect:

                    evMargin1+=1
            print(abs(margin))

            #prediction - spread > 0 and winner 1
            #prediction - spread < 0 and winner 0
            




            print('spread:',spreadCorrect,spread[i], 'prediction: ',correct,round(p[i][0]),round(p[i][1]),'=',round(p[i][0]-p[i][1]),' actual:' ,homeTestScore[i],visitorTestScore[i],'=',pmscore)

            print('#-------------------------------------------#')
            if correct:
                c+=1
        #betting 100$ pergame at 110/100 
        print('percent correct winners: ', c/n*100,'%')
        print('spread percent correct winners: ', s/n*100,'%')
        print('expected value all games: ', ev/n*100,'%')
        print('expected value over 1 point margins: ',evMargin1,'/',evMargin1Count,'=', evMargin1/evMargin1Count*100,'%')
        print('spent:', round(evMargin1Count*100),'profits ',round((evMargin1 * 190.91)-(evMargin1Count*100)),' total :',round((evMargin1 * 190.91)))
        print('expected value over 2 point margins: ',evMargin2,'/',evMargin2Count,'=', evMargin2/evMargin2Count*100,'%')
        print('spent:', round(evMargin2Count*100),'profits ',round((evMargin2 * 190.91)-(evMargin2Count*100)),' total :',round((evMargin2 * 190.91)))
        print('expected value over 3 point margins: ',evMargin3,'/',evMargin3Count,'=', evMargin3/evMargin3Count*100,'%')
        print('spent:', round(evMargin3Count*100),'profits ',round((evMargin3 * 190.91)-(evMargin3Count*100)),' total :',round((evMargin3 * 190.91)))
        print('expected value over 4 point margins: ',evMargin4,'/',evMargin4Count,'=', evMargin4/evMargin4Count*100,'%')
        print('spent:', round(evMargin4Count*100),' profits :',round((evMargin4 * 190.91)-(evMargin4Count*100)),' total :',round((evMargin4 * 190.91)))

        r = []








        
        r.append('percent correct winners: '+str(round(c/n*100))+'%')
        r.append('spread percent correct winners: '+ str(round(s/n*100))+'%')
        r.append('expected value all games: '+str(round(ev/n*100))+'%')
       
        r.append('expected value over 1 point margins: '+str(evMargin1)+'/'+str(evMargin1Count)+'='+ str(round(evMargin1/evMargin1Count*100))+'%')
        r.append('spent: '+str(round(evMargin1Count*100))+' profits: '+str(round((evMargin1 * 190.91)-(evMargin1Count*100)))+' total: '+str(round((evMargin1 * 190.91))))
        r.append('expected value over 2 point margins: '+str(evMargin2)+'/'+str(evMargin2Count)+'='+ str(round(evMargin2/evMargin2Count*100))+'%')
        r.append('spent: '+str(round(evMargin2Count*100))+' profits: '+str(round((evMargin2 * 190.91)-(evMargin2Count*100)))+' total: '+str(round((evMargin2 * 190.91))))

        r.append('expected value over 3 point margins: '+str(evMargin3)+'/'+str(evMargin3Count)+'='+ str(round(evMargin3/evMargin3Count*100))+'%')
        r.append('spent: '+str(round(evMargin3Count*100))+' profits: '+str(round((evMargin3 * 190.91)-(evMargin3Count*100)))+' total: '+str(round((evMargin3 * 190.91))))

        r.append('expected value over 4 point margins: '+str(evMargin4)+'/'+str(evMargin4Count)+'='+ str(round(evMargin4/evMargin4Count*100))+'%')
        r.append('spent: '+str(round(evMargin4Count*100))+' profits: '+str(round((evMargin4 * 190.91)-(evMargin4Count*100)))+' total: '+str(round((evMargin4 * 190.91))))

        #r.append('expected value over 6 point margins: '+str(evMargin6)+'/'+str(evMargin6Count)+'='+ str(round(evMargin6/evMargin6Count*100))+'%')
        #r.append('spent: '+str(round(evMargin6Count*100))+' profits: '+str(round((evMargin6 * 190.91)-(evMargin6Count*100)))+' total: '+str(round((evMargin6 * 190.91))))
        eval = {}

        eval['correct'] = c
        eval['wrong'] = n-c
        eval['spreadCorrect'] = s
        eval['spreadWrong'] = n-s
        eval['evMargin1'] = evMargin1
        eval['evMargin1wrong'] = evMargin1Count-evMargin1
        eval['evMargin2'] = evMargin2
        eval['evMargin2wrong'] = evMargin2Count-evMargin2
        eval['evMargin3'] = evMargin3
        eval['evMargin3wrong'] = evMargin3Count-evMargin3
        




        return [r,eval]
    r = print_prediction(model, data)
    return r
