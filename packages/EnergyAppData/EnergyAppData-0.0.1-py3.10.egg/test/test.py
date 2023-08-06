import pytest
import electricpower as pw
from keras import Sequential
from keras.layers import Flatten, Dense, Dropout, LSTM
X_train,X_test,Y_train,Y_test=pw.load_data()
def test_model(X_train,X_test,Y_train,Y_test):
    lstm_model = Sequential()
    lstm_model.add(LSTM(100, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
    lstm_model.add(LSTM(80, activation='relu',  return_sequences=True))
    lstm_model.add(LSTM(50, activation='relu', return_sequences=True))
    lstm_model.add(LSTM(20, activation='relu'))
    lstm_model.add(Dense(20, activation='relu'))
    lstm_model.add(Dense(1))
def test_model_error(S):
    with pytest.raises(AttributeError, message="Model has attribute name S"):
        test_model(S)
test_model(S)

