import content_features as content
import external_features as external
import feature_extractor as feature
import url_features as url
import urllib
import utility
import keras
import xgboost
import utility

#1: legitimate, 0: phishing    
#XGBoost model
def machine_learning(url):
    xgboot_model = xgboost.XGBClassifier()
    xgboot_model.load_model('/home/vantu/PTIT/Code/extension/core/xgb.save_model')
    features = feature.extract_features(url)
    if features == None:
        return 0
    else:
        return xgboot_model.predict([utility.nomarlization_data(features)])[0]
#CNN-LSTM model
def cnn_lstm(url):
    threshold = 0.95
    cnn_lstm_model = keras.models.load_model("/home/vantu/PTIT/Code/extension/core/cnn-lstm.h5")
    result = cnn_lstm_model.predict(utility.url_process(url))
    delta = abs(result[0][0] - result[0][1])
    if delta > threshold:
        if result[0][0] > result[0][1]:
            return 0
        else:
            return 1

    return -1