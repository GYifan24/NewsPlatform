import news_classes
import numpy as np
import os
from os.path import join
from os.path import normpath
import pandas as pd
import pickle
import sys
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

# import packages in trainer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

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

# Threading RPC Server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(classify, 'classify')
print(("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT)))
RPC_SERVER.serve_forever()
