import pickle
import tensorflow as tf
import pandas as pd
import numpy as np
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint

#------------------------------------------------------------------------#
#saves pickle object file
def save_obj(obj, name):
    with open('updatedObj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#loads pickle object file
def load_obj(name):
    with open('updatedObj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)
#------------------------------------------------------------------------#

# Loads tensorflow model and predicts game
# Takes model number path of csv file and username
# returns prediction 
def retrain_model(modelNum,path,username,home_score,visitor_score,strength_decimal):

    #read csv file and cread pandas df
    data = pd.read_csv(path)
    #load model settings
    try:
        modelSettings = load_obj(str(username)+'ModelSettings'+modelNum)
    except FileNotFoundError:
        return 'error'
    
    optimizer_class = getattr(tf.keras.optimizers, modelSettings['optimizer'].capitalize())
    default_lr = optimizer_class().learning_rate.numpy()

    lr = default_lr * strength_decimal * .1


    optimizer_class = getattr(tf.keras.optimizers, modelSettings['optimizer'].capitalize())
    custom_optimizer = optimizer_class(learning_rate=lr)


    print('------------ default learning rate: ', default_lr, '==== new lr: ', lr)

    model = tf.keras.Sequential([
        tf.keras.layers.Dense(modelSettings['layer1Count'], activation=modelSettings['layer1Activation']),
        tf.keras.layers.Dense(modelSettings['layer2Count'], activation=modelSettings['layer2Activation']),
        tf.keras.layers.Dense(2, activation='linear'),
        ])
    

    try:
        modelSettings = load_obj(str(username)+'ModelSettings'+modelNum)
        model.load_weights('./userModels/'+username+'/'+modelNum+'/checkpoints/my_checkpoint')
    except FileNotFoundError:
        return 'error'
    

    
    #drop a bunch of values
    d = ['gameid','home_id','visitor_id','home_history_gameid','visitor_history_gameid','home_history2_gameid','visitor_history2_gameid']
    try:
        if modelSettings['streaks'] != 'true':
            d=d+['home_streak','visitor_streak']
        if modelSettings['wl'] != 'true':
            d=d+['hw','hl','vw','vl']
        if modelSettings['gp'] != 'true':
            d=d+['hgp','vgp']
        if modelSettings['ps'] != 'true':
            d.append('spread')
        labels = ['ast','blk','dreb','fg3_pct','fg3a','fg3m','fga','fgm','fta','ftm','oreb','pf','pts','reb','stl', 'turnover', 'min']
        for currentPlayer in range(int(modelSettings['players']),7):
            derp = ['home_', 'visitor_']
            for foo in derp:#home vistor
                    for label in labels:
                        stat = foo+str(currentPlayer)+'_'+label#make lables
                        d.append(stat)

        features = ['min']
        if modelSettings['ast'] == 'true':
            features.append('ast')
        if modelSettings['blk'] == 'true':
            features.append('blk')
        if modelSettings['reb'] == 'true':
            #features.append('reb')
            features.append('dreb')
            features.append('oreb')
        if modelSettings['fg3'] == 'true':
            #features.append('fg3_pct')
            features.append('fg3m')
            features.append('fg3a')
        if modelSettings['fg'] == 'true':
            features.append('fga')
            features.append('fgm')
        if modelSettings['ft'] == 'true':
            features.append('fta')
            features.append('ftm')
        if modelSettings['pf'] == 'true':
            features.append('pf')
        if modelSettings['pts'] == 'true':
            features.append('pts')
        if modelSettings['stl'] == 'true':
            features.append('stl')
        if modelSettings['turnover'] == 'true':
            features.append('turnover')
        

        for currentPlayer in range(0,int(modelSettings['players'])):
            derp = ['home_', 'visitor_']
            for foo in derp:#home vistor
                    for label in labels:
                        if label not in features:
                            stat = foo+str(currentPlayer)+'_'+label#make labels
                            d.append(stat)
    except KeyError:
        d = ['gameid','home_id','visitor_id','home_streak','visitor_streak','hgp','hw','hl','vgp','vw','vl']
    data.drop(d, axis=1, inplace=True)

    #convert data to values
    data = data.values
    #convert values to floats
    data = data.astype(float)


    #x_train = tf.keras.utils.normalize(x_train, axis=1)
    #x_test = tf.keras.utils.normalize(x_test, axis=1)


    #define squential model

    #compile model
    model.compile(optimizer=custom_optimizer, loss='mean_squared_error', metrics=['accuracy'])
  # After dropping columns and normalizing if needed
    x_train = data
    home_score = float(home_score)
    visitor_score = float(visitor_score)

    # Create y_train with the home_score and visitor_score
    y_train = np.array([[home_score, visitor_score]])

    # Since we're not normalizing in this snippet, if you have normalization in your workflow, apply it to x_train here

    # Fit the model on this single game data
    model.fit(x_train, y_train, epochs=1, batch_size=1, shuffle=False)

    # Save the new weights
    model.save_weights('./userModels/'+username+'/'+str(modelNum)+'/checkpoints/my_checkpoint')

    return 'Model retrained on the new game data, the update model weights have also been saved.'



