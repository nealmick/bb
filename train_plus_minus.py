import time
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import datetime

path = "csv1/test123.csv"
current_time = str(time.time())

def difference(score):
    return score[0] - score[1]

data = pd.read_csv(path)
score = data[['home_score', 'visitor_score']].values
score_difference = np.apply_along_axis(difference, 1, score)
print(score_difference)





data.drop(['home_score','visitor_score', 'gameid'], axis=1, inplace=True)


data = data.values
data = data.astype(float)

x_train, x_test, y_train, y_test = train_test_split(data, score_difference, test_size=0.1)

#x_train = tf.keras.utils.normalize(x_train, axis=1)
#x_test = tf.keras.utils.normalize(x_test, axis=1)

model = tf.keras.Sequential([

    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    
    tf.keras.layers.Dense(1, activation='linear'),



])

log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)



model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=100, validation_split=0.1, batch_size=4,callbacks=[tensorboard_callback])


def print_results(model, x_test, y_test):
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
    print('Test Loss: {:.4f}'.format(test_loss))
    print('Test Accuracy: {:.4f}'.format(test_acc))

    predictions = model.predict(x_test)
    c = 0
    x = len(predictions)
    for i in range(x):
        if y_test[i] >= 0 and predictions[i][0] >=0:
            print('Correct - actual: {:.4f}, Predicted: {:.4f}'.format(y_test[i], predictions[i][0]))

            c+=1
        elif y_test[i] < 0 and predictions[i][0] <0:
            print('Correct - actual: {:.4f}, Predicted: {:.4f}'.format(y_test[i], predictions[i][0]))
            c+=1
        else:
            print('wrong - actual: {:.4f}, Predicted: {:.4f}'.format(y_test[i], predictions[i][0]))

    print('coorrect % ', c/x*100)
print_results(model, x_test, y_test)

#print_predictions(model, x_test, y_test)
