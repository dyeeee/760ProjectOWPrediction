import time
import numpy
import pandas
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd
from keras import optimizers
from tensorflow.keras.optimizers import SGD, RMSprop, Adam

seed = 7
numpy.random.seed(seed)

df = pd.read_table("./P3_Data/OWL_Data_team_match_stat_all_2020_withRank_v3.csv", sep=",")
test_df = pd.read_table("./P3_Data/OWL_Data_TESTSET_V3.csv", sep=",")

# split data & response
# data = df.iloc[:, 4:]
# response = df["t1_win"]
#
# test_Data = test_df.iloc[:, 5:]
# test_response = test_df["3"]
index = [11, 6, 13, 12, 5, 27, 10, 18, 16, 30, 20, 15, 29, 36, 14, 41]

data = df.iloc[:, index]
response = df["t1_win"]

# test_df = test_df.iloc[:, 1:]
test_Data = test_df.iloc[:, index]
test_response = test_df["t1_win"]

X_train, y_train = data, response
X_test, y_test = test_Data, test_response

# define the keras model
model = Sequential()
model.add(Dense(100, input_dim=len(index), activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
opt = RMSprop(lr=0.00001, rho=0.8, epsilon=None, decay=0.0)
opt2 = Adam(lr=0.00001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])

# model.fit(X_train, y_train, epochs=150, batch_size=10, verbose=1)
# _, accuracy = model.evaluate(X_train, y_train, verbose=0)
# print('Train Accuracy: %.2f' % (accuracy * 100))
#
# print("test set")
# _, scores = model.evaluate(X_test, y_test, batch_size=150, verbose=0)
# print('Test Accuracy: %.2f' % (scores * 100))

history = model.fit(X_train, y_train,
                    epochs=50,
                    validation_data=(X_test, y_test))

import matplotlib.pyplot as plt

history_dict = history.history
history_dict.keys()
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs = range(1, len(loss_values) + 1)

plt.clf()
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.clf()
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']

plt.plot(epochs, acc_values, 'bo', label='Training acc')
plt.plot(epochs, val_acc_values, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Acc')
plt.legend()

plt.show()

print("test set")
_, scores = model.evaluate(X_test, y_test, batch_size=150, verbose=0)
print('Test Accuracy: %.2f' % (scores * 100))