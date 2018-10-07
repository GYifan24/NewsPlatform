import pandas as pd
import shutil
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import pickle
import os
from os.path import join
from os.path import normpath

MODEL_OUTPUT_FILE = normpath(join(os.path.dirname(__file__), '../model/model.sav'))
TFIDF_OUTPUT_FILE = normpath(join(os.path.dirname(__file__), '../model/tfidf.sav'))
DATA_SET_FILE = normpath(join(os.path.dirname(__file__), '../data/data.csv'))


def run() :
    df = pd.read_csv(DATA_SET_FILE, header=None)
    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2',
        encoding='latin-1', ngram_range=(1, 2), stop_words='english')

    # df[0]: label df[1]: title df[2]: description
    features = tfidf.fit_transform(df[1]).toarray()
    labels = df[0]

    X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, df.index, test_size=0.33, random_state=0)

    # train and predict
    model = LogisticRegression(random_state=0)
    model.fit(X_train, y_train)
    y_pred_proba = model.predict_proba(X_test)
    y_pred = model.predict(X_test)

    # CV = 5
    # accuracy = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)

    # print("LogisticRegression Training model accuracy: " + accuracy)

    # save models
    pickle.dump(model, open(MODEL_OUTPUT_FILE, 'wb'))
    pickle.dump(tfidf, open(TFIDF_OUTPUT_FILE, 'wb'))

if __name__ == "__main__":
    run()
