from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from sklearn.metrics import accuracy_score
from preprocessing import preprocessing
import scipy.sparse as sp
import pandas as pd
import time


positive = pd.read_csv('positive.csv', sep=';', encoding='utf-8')
negative = pd.read_csv('negative.csv', sep=';', encoding='utf-8')


positive.columns = ['del1', 'del2', 'del3', 'Comment', 'Score', 'del4', 'del5', 'del6', 'del7', 'del8', 'del9', 'del10']
negative.columns = ['del1', 'del2', 'del3', 'Comment', 'Score', 'del4', 'del5', 'del6', 'del7', 'del8', 'del9', 'del10']


positive.drop(['del1', 'del2', 'del3', 'del4', 'del5', 'del6', 'del7', 'del8', 'del9', 'del10'], axis=1, inplace=True)
negative.drop(['del1', 'del2', 'del3', 'del4', 'del5', 'del6', 'del7', 'del8', 'del9', 'del10'], axis=1, inplace=True)


positive['Preprocessed_text'] = positive.apply(lambda row: preprocessing(row['Comment']), axis=1)
negative['Preprocessed_text'] = negative.apply(lambda row: preprocessing(row['Comment']), axis=1)


n_rows = len(positive)
number_20_percent = int(n_rows * 20 / 100)

test = pd.concat([positive[:10000], negative[:10000]])
train = pd.concat([positive[10200:40200], negative[10200:40200]])


train_prep = [" ".join(tokens) for tokens in train['Preprocessed_text']]
test_prep = [" ".join(tokens) for tokens in test['Preprocessed_text']]


vectorizer = TfidfVectorizer()
train_vectors = vectorizer.fit_transform(train_prep)

joblib.dump(vectorizer, 'tfidf_vectorizer.joblib')

test_vectors = vectorizer.transform(test_prep)

train_vectors = sp.csr_matrix(train_vectors)
test_vectors = sp.csr_matrix(test_vectors)

model = svm.SVC(kernel='rbf', C=10, gamma='scale')

model.fit(train_vectors, train['Score'])

pred = model.predict(test_vectors)

accuracy = accuracy_score(test['Score'], pred)
print("Accuracy:", accuracy)

joblib.dump(model, 'svm_model_3000.pkl')