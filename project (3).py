# -*- coding: utf-8 -*-
"""project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QouWOBgmDqoVNOnXclJ-BVZ_a6i9rRUo
"""

from google.colab import drive
drive.mount('/content/drive')

import os
os.getcwd()

os.chdir('/content/drive/My Drive/forsk deeplearning')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data=pd.read_csv('mbti_1.csv')

data["list_messages"]=data["posts"].apply(lambda x: x.strip().split("|||"))

data.head()



import re
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
list_stopwords=list(stopwords.words('english'))+[word.lower() for word in list(data.type.unique())]
nltk.download ('wordnet')
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

def remove_url(message_list):
  res=""
  for message in message_list:
    if "http" in message:
      l=re.findall(r"\b(?:https?://)?(?:(?i:[1-9a-z]+\.))[^\s,]+\b",message)
      for link in l:
        message=message.replace(link,"")
      res=res+" "+message.strip()
    else:
      res=res+message.strip()
   
 
  res=re.sub('[^a-zA-Z\s]'," ",res)
  res=res.lower()
  res=res.split()
  res = [word for word in res if not word in list_stopwords]
  wl = PorterStemmer()
  res = [wl.stem(word) for word in res]
  res=" ".join(res)  
  return(res)

data["paragraph"]=data.list_messages.apply(remove_url)



map1 = {"I": 0, "E": 1}
map2 = {"N": 0, "S": 1}
map3 = {"T": 0, "F": 1}
map4 = {"J": 0, "P": 1}
data['I-E'] = data['type'].astype(str).str[0]
data['I-E'] = data['I-E'].map(map1)
data['N-S'] = data['type'].astype(str).str[1]
data['N-S'] = data['N-S'].map(map2)
data['T-F'] = data['type'].astype(str).str[2]
data['T-F'] = data['T-F'].map(map3)
data['J-P'] = data['type'].astype(str).str[3]
data['J-P'] = data['J-P'].map(map4)

import string
def text_process(mess):
    nopunc = [char for char in mess if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    return [word for word in nopunc.split()]

data['cbd']=data.paragraph

from sklearn.feature_extraction.text import CountVectorizer

bow_transformer = CountVectorizer(analyzer="word",max_features=1500).fit(data['cbd'])

print(len(bow_transformer.vocabulary_))

messages_bow = bow_transformer.transform(data["paragraph"])

type(messages_bow)

print('Shape of Sparse Matrix: ', messages_bow.shape)
print('Amount of Non-Zero occurences: ', messages_bow.nnz)

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer().fit(messages_bow)

messages_tfidf = tfidf_transformer.transform(messages_bow).toarray()

print(len(messages_tfidf[0]))

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['la'] = le.fit_transform(data['type'])

data.head()

"".join(data.list_messages[0])

labels_ie =data.iloc[:,3].values
labels_ns =data.iloc[:,4].values
labels_tf =data.iloc[:,5].values
labels_jp =data.iloc[:,6].values
labels=data.type.values



from sklearn.model_selection import train_test_split
features_train_ie, features_test_ie, labels_train_ie, labels_test_ie = train_test_split(messages_tfidf, labels_ie, test_size = 0.33, random_state = 7)

from sklearn.model_selection import train_test_split
features_train_ns, features_test_ns, labels_train_ns, labels_test_ns = train_test_split(messages_tfidf, labels_ns, test_size = 0.33, random_state = 7)

from sklearn.model_selection import train_test_split
features_train_tf, features_test_tf, labels_train_tf, labels_test_tf = train_test_split(messages_tfidf, labels_tf, test_size = 0.33, random_state = 7)

from sklearn.model_selection import train_test_split
features_train_jp, features_test_jp, labels_train_jp, labels_test_jp = train_test_split(messages_tfidf, labels_jp, test_size = 0.33, random_state = 7)

from sklearn.model_selection import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(messages_tfidf, labels, test_size = 0.33, random_state = 7)

print(features_train.shape)
print(labels_train.shape)

from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=2)
features_train, labels_train = sm.fit_sample(features_train, labels_train.ravel())

import xgboost
classifier_ie = xgboost.XGBClassifier()
classifier_ns = xgboost.XGBClassifier()
classifier_tf = xgboost.XGBClassifier()
classifier_jp = xgboost.XGBClassifier()
classifier = xgboost.XGBClassifier()

classifier_ie.fit(features_train_ie, labels_train_ie)

classifier_ns.fit(features_train_ns, labels_train_ns)

classifier_tf.fit(features_train_tf, labels_train_tf)

classifier_jp.fit(features_train_jp, labels_train_jp)



labels_pred = classifier_jp.predict(features_test_jp)

from sklearn.metrics import accuracy_score
accuracy=accuracy_score(labels_test_jp,labels_pred)

accuracy

from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression

parameters = {
    'C': np.linspace(1, 10, 10)
             }
lr = LogisticRegression()

clf = GridSearchCV(lr, parameters, cv=5, verbose=5, n_jobs=3)
clf.fit(features_train, labels_train.ravel())



import pickle


project_pickle="newpickle_all.sav"

list_objects=[bow_transformer,classifier_ie,classifier_ns,classifier_tf,classifier_jp]

pickle.dump(list_objects,open(project_pickle,"wb"))

import pickle
loded_model = pickle.load(open("newpickle.sav",'rb'))



