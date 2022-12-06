import string
import numpy
from keras_preprocessing.sequence import pad_sequences
import pandas


ascii_letters = string.ascii_letters # 1~52
digits = string.digits # 53~62
punctuation = string.punctuation # 63~94
total_char = ascii_letters + digits + punctuation    


UNK = len(total_char) + 1
TOTAL_FEATURES = UNK + 1 
charmap = {
    c: idx+1
    for idx, c in enumerate(total_char)
}
max_len = 200

def encodeChar(c):
    return charmap.get(c, UNK)

def url_process(url):
    return pad_sequences([numpy.array([encodeChar(c) for c in url])], maxlen=max_len, padding='post')


def get_nomarlization_argument():
    dict = {}
    data = pandas.read_csv('/home/vantu/PTIT/Code/extension/core/dataset.csv')
    data.drop(['url', 'status', 'random_domain', 'nb_or', 'ratio_nullHyperlinks', 'ratio_intRedirection', 'ratio_intErrors', 'submit_email', 'sfh', 'google_index'], axis=1, inplace=True)
    for column in data.columns:
        mean = data[column].min()
        deviation = data[column].max() - data[column].min()
        dict[column] = [mean, deviation]
    return dict
    
nomarlization_dict = get_nomarlization_argument()

def nomarlization_data(features):
    #Prevent return null

    for i in features:
        if i == '':
            i = '0'
    data = get_nomarlization_argument()
    i = 0
    for key in data:
        features[i] = (features[i] - data[key][0]) / data[key][1]
        i += 1
    print(features)
    return features
    
# def nomarlization_data(features):
#     dict = get_nomarlization_argument
#     i = 0
#     for key in nomarlization_dict:
#         features[i] = (features[i] - dict[key][0]) / dict[key][1]
#         i += 1
#     print(features)
#     return features
    