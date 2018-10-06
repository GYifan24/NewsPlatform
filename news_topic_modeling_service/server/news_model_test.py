import pandas as pd
import shutil
import news_classes
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import pickle
import os
from os.path import join
from os.path import normpath

FEATURE_OUTPUT_FILE = normpath(join(os.path.dirname(__file__), '../model/feature.sav'))
MODEL_FILE = normpath(join(os.path.dirname(__file__), '../model/model.sav'))


model = pickle.load(open(MODEL_FILE, 'rb'))

def classify(text):
    loaded_tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
        encoding='latin-1', ngram_range=(1, 2), stop_words='english', vocabulary=pickle.load(open(FEATURE_OUTPUT_FILE, "rb")))

    features = loaded_tfidf.fit_transform(text).toarray()


    y_pred = model.predict(features)
    topic = news_classes.class_map[str(y_pred[0])]
    return topic

if __name__ == "__main__":
    test_txt = 'President Donald Trump told Israeli Prime Minister Benjamin Netanyahu Wednesday that the US is going to push for a peace deal with the Palestinians and asked Israel "to hold back" on settlement construction.'
    print (classify([test_txt]))
