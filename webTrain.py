import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import datetime


import logging
import sys
import contextlib
from io import StringIO
import os




import tensorflow as tf


class ImmediateFileHandler(logging.FileHandler):
    def __init__(self, log_filename, mode='a', encoding=None, delay=False):
        super().__init__(log_filename, mode, encoding, delay)
        self.terminator = ''

    def emit(self, record):
        super().emit(record)
        self.flush()  # Force flushing after every emit

def setup_logging(username, modelNum):
    # Define the directory and log filename
    log_directory = f'./userModels/{username}/{modelNum}'
    log_filename = os.path.join(log_directory, 'training_log.txt')

    # Create the directory if it doesn't exist
    os.makedirs(log_directory, exist_ok=True)

    logger = logging.getLogger(f'tensorflow_logger_{username}_{modelNum}')
    logger.setLevel(logging.INFO)

    # Clear any old handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Setup the file handler with the ImmediateFileHandler
    file_handler = ImmediateFileHandler(log_filename, mode='w')
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

class DirectWriteLoggerCallback(tf.keras.callbacks.Callback):
    def __init__(self, logger):
        super(DirectWriteLoggerCallback, self).__init__()
        self.logger = logger

@contextlib.contextmanager
def log_stdout(logger):
    class LoggerWriter:
        def __init__(self, level):
            self.level = level

        def write(self, message):
            if message != '\n':
                self.level(message)

        def flush(self):
            pass

    old_stdout = sys.stdout
    sys.stdout = LoggerWriter(logger.info)
    try:
        yield
    finally:
        sys.stdout = old_stdout




def webappTrain( modelNum,epochs,size,layer1Count,layer1Activation,layer2Count,layer2Activation,optimizer,username,es,rmw,kr,streaks,wl,gp,ps,players,ast,blk,reb,fg3,fg,ft,pf,pts,stl,turnover,re_eval = False):
    logger = setup_logging(username, modelNum)
    with log_stdout(logger):
        labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        print('players-------------',players)
        #path to train and test datasets
        path = "csv/train.csv"
        test_path = "csv/test.csv"
        
        current_time = str(time.time())
        #read train data
        data = pd.read_csv(path)
        #extract target data
        homeScore = data['home_score'].values
        visitorScore = data['visitor_score'].values
        home_id = data['home_id'].values
        visitor_id = data['visitor_id'].values
        
        #drop values
        #,'home_streak','visitor_streak'
        #data.drop(['home_score', 'visitor_score', 'gameid','home_id','visitor_id','hgp','hw','hl','vgp','vw','vl'], axis=1, inplace=True)
        d = ['home_score', 'visitor_score', 'gameid','home_id','visitor_id','home_history_gameid','visitor_history_gameid','home_history2_gameid','visitor_history2_gameid']
        
        if streaks != 'true':
            d=d+['home_streak','visitor_streak']
        if wl != 'true':
            d=d+['hw','hl','vw','vl']
        if gp != 'true':
            d=d+['hgp','vgp']
        if ps != 'true':
            d.append('spread')
        for currentPlayer in range(int(players),7):
            derp = ['home_', 'visitor_']
            for foo in derp:#home vistor
                    for label in labels:
                        stat = foo+str(currentPlayer)+'_'+label#make lables
                        d.append(stat)

        features = ['min']
        if ast == 'true':
            features.append('ast')
        if blk == 'true':
            features.append('blk')
        if reb == 'true':
            #features.append('reb')
            features.append('dreb')
            features.append('oreb')
        if fg3 == 'true':
            #features.append('fg3_pct')
            features.append('fg3m')
            features.append('fg3a')
        if fg == 'true':
            features.append('fga')
            features.append('fgm')
        if ft == 'true':
            features.append('fta')
            features.append('ftm')
        if pf == 'true':
            features.append('pf')
        if pts == 'true':
            features.append('pts')
        if stl == 'true':
            features.append('stl')
        if turnover == 'true':
            features.append('turnover')
        

        for currentPlayer in range(0,int(players)):
            derp = ['home_', 'visitor_']
            for foo in derp:#home vistor
                    for label in labels:
                        if label not in features:
                            stat = foo+str(currentPlayer)+'_'+label#make labels
                            d.append(stat)
        print(d)
        data.drop(d, axis=1, inplace=True)
        data.fillna(0, inplace=True)

        #convert data to values
        data = data.values


        #convert to float
        data = data.astype(float)

        #split train test not really used
        x_train, x_test, y_train, y_test = train_test_split(data, np.column_stack((homeScore, visitorScore)), test_size=0.0001)


        #define model
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
        #early stopping
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

        #tensorboard log dir
        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        #tensorboard callback
        TensorBoard = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

        #compile model
        model.compile(optimizer=optimizer, loss='mean_squared_error', metrics=['accuracy'])
        logger = setup_logging(username, modelNum)
        direct_write_logger_callback = DirectWriteLoggerCallback(logger)


        #train model
        
        if es =='true':
            model.fit(x_train, y_train, epochs=epochs, validation_split=0.1, batch_size=size ,callbacks=[TensorBoard,EarlyStopping,direct_write_logger_callback],shuffle=False)
        else:
            model.fit(x_train, y_train, epochs=epochs, validation_split=0.1, batch_size=size ,callbacks=[TensorBoard,direct_write_logger_callback],shuffle=False)
        #save weights
        model.save_weights('./userModels/'+username.username+'/'+str(modelNum)+'/checkpoints/my_checkpoint')



        #read test games
        data = pd.read_csv(test_path)
        data.fillna(0, inplace=True)
    

        homeTestScore = data['home_score'].values
        visitorTestScore = data['visitor_score'].values
        spread = data['spread'].values
        #data.drop(['home_score', 'visitor_score', 'gameid','home_id','visitor_id','hgp','hw','hl','vgp','vw','vl'], axis=1, inplace=True)
        data.drop(d, axis=1, inplace=True)

        #prepare test data
        data = data.values
        data = data.astype(float)
        #evaluate model
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
            evMargin4Min = -1
            evMargin4Max = 0
            evMargin4Current = 0


            evMargin3Count = 0#count expected 
            evMargin3 = 0# expected margin
            evMargin3Min = -1
            evMargin3Max = 0

            evMargin3Current = 0    


            evMargin2Count = 0#count expected 
            evMargin2 = 0# expected margin
            evMargin2Min = -1
            evMargin2Max = 0
            evMargin2Current = 0


            evMargin1Count = 0#count e~xpected 
            evMargin1 = 0# expected margin
            evMargin1Min = -1
            evMargin1Max = 0
            evMargin1Current = 0
            gameSeries1 = []
            gameSeries2 = []
            gameSeries3 = []
            SeriesStepCounter = 0
            for i in range(len(p)):
                SeriesStepCounter+=1
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
                    #print('correct agaist spread',pred,swin)
                elif pred == 1 and swin == 1:
                    ev +=1
                    #print('correct agaist spread',pred,swin)
                else:
                    mcorrect = False
                    #print('wrong agaist spread',pred,swin)

                margin = abs(pmp)-abs(spread[i])

                if float(pmp) < 0 and spread[i] < 0:
                    #print('both negative')
                    #margin = pmscore+spread[i]
                    pass



                if abs(margin) > 6:
                    evMargin6Count+=1
                    if mcorrect:
                        evMargin6+=1

                if abs(margin) > 4:
                    evMargin4Count+=1
                    if mcorrect:
                        evMargin4+=1
                        evMargin4Current += 1
                    else:
                        evMargin4Current -= 1

                    if evMargin4Current < evMargin4Min:
                        evMargin4Min = evMargin4Current
                    if evMargin4Current > evMargin4Max:
                        evMargin4Max = evMargin4Current

                if abs(margin) > 3:
                    evMargin3Count+=1
                    if mcorrect:
                        evMargin3+=1
                        evMargin3Current += 1
                    else:
                        evMargin3Current -= 1

                    if evMargin3Current < evMargin3Min:
                        evMargin3Min = evMargin3Current

                    if evMargin3Current > evMargin3Max:
                        evMargin3Max = evMargin3Current


                if abs(margin) > 2:
                    evMargin2Count+=1
                    if mcorrect:
                        evMargin2+=1
                        evMargin2Current += 1
                    else:
                        evMargin2Current -= 1

                    if evMargin2Current < evMargin2Min:
                        evMargin2Min = evMargin2Current

                    if evMargin2Current > evMargin2Max:
                        evMargin2Max = evMargin2Current

                if abs(margin) > 1:
                    evMargin1Count+=1
                    if mcorrect:
                        evMargin1+=1
                        evMargin1Current += 1
                    else:
                        evMargin1Current -= 1

                    if evMargin1Current < evMargin1Min:
                        evMargin1Min = evMargin1Current
                    
                    if evMargin1Current > evMargin1Max:
                        evMargin1Max = evMargin1Current

                #print(abs(margin))

                #prediction - spread > 0 and winner 1
                #prediction - spread < 0 and winner 0
                


                if SeriesStepCounter >= len(p)/100 :
                    gameSeries1.append(evMargin1Current)
                    gameSeries2.append(evMargin2Current)
                    gameSeries3.append(evMargin3Current)
                    SeriesStepCounter = 0

                #print('spread:',spreadCorrect,spread[i], 'prediction: ',correct,round(p[i][0]),round(p[i][1]),'=',round(p[i][0]-p[i][1]),' actual:' ,homeTestScore[i],visitorTestScore[i],'=',pmscore)

                #print('#-------------------------------------------#'+' variance: '+str(evMargin1Min*100))
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








            res = {}
            res['wl'] = round(c/n*100)
            res['swl'] = round(s/n*100)
            res['count'] = round(n)
            res['evMargin1'] = str(evMargin1)
            res['evMargin1Count'] = str(evMargin1Count)
            res['evMargin1Pct'] = str(round(evMargin1/evMargin1Count*100))
            res['evMargin1Min'] = evMargin1Min
            res['evMargin1Max'] = evMargin1Max
            res['evMargin1Total'] = round((evMargin1Count * 100))
            res['evMargin1Profit'] = round((evMargin1 * 190.91)-(evMargin1Count*100))
            
            res['evMargin2'] = str(evMargin2)
            res['evMargin2Count'] = str(evMargin2Count)
            res['evMargin2Pct'] = str(round(evMargin2/evMargin2Count*100))
            res['evMargin2Min'] = evMargin2Min
            res['evMargin2Max'] = evMargin2Max
            res['evMargin2Total'] = round((evMargin2Count * 100))
            res['evMargin2Profit'] = round((evMargin2 * 190.91)-(evMargin2Count*100))
            

            res['evMargin3'] = str(evMargin3)
            res['evMargin3Count'] = str(evMargin3Count)
            res['evMargin3Pct'] = str(round(evMargin3/evMargin3Count*100))
            res['evMargin3Min'] = evMargin3Min
            res['evMargin3Max'] = evMargin3Max

            res['evMargin3Total'] = round((evMargin3Count * 100))
            res['evMargin3Profit'] = round((evMargin3 * 190.91)-(evMargin3Count*100))
            

            res['evMargin4'] = str(evMargin4)
            res['evMargin4Count'] = str(evMargin4Count)
            res['evMargin4Pct'] = str(round(evMargin4/evMargin4Count*100))
            res['evMargin4Min'] = evMargin4Min
            res['evMargin4Max'] = evMargin4Max

            res['evMargin4Total'] = round((evMargin4Count * 100))
            res['evMargin4Profit'] = round((evMargin4 * 190.91)-(evMargin4Count*100))
            
            res['gameSeries1'] = gameSeries1
            res['gameSeries2'] = gameSeries2
            res['gameSeries3'] = gameSeries3




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
            




            return [eval,res]
        r = print_prediction(model, data)
        return r
