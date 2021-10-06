#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import os
from Bio.Seq import Seq
from Bio import SeqIO
import numpy as np
import tensorflow as tf
import math
import pickle
from tensorflow import keras


# In[ ]:


path_file_list=[]
for root, dirs, files in os.walk('Pathogenic E. Coli Sequences/'):
    for file in files:
        if file.endswith('.fasta'):
            path_file_list.append(('Pathogenic E. Coli Sequences/'+str(file)))


# In[ ]:


path_seq_list=[];
for filename in path_file_list:
    for seq_record in SeqIO.parse(filename,'fasta'):
        path_seq_list.append(seq_record.seq)


# In[ ]:


nonpath_ecoli_fasta_file='EcoliK12_MG1655.fasta'


# In[ ]:


nonpath_seq_list=[];
for seq_record in SeqIO.parse(nonpath_ecoli_fasta_file,'fasta'):
    nonpath_seq_list.append(seq_record.seq)


# In[ ]:


nonpath_vector_list=[];
for item in nonpath_seq_list:
    vector_rep=[]
    for letter in item:
        if letter=='A':
            number=0.25
        elif letter=='T':
            number=0.5
        elif letter=='C':
            number=0.75
        elif letter=='G':
            number=1
        vector_rep.append(number)
    nonpath_vector_list.append(vector_rep)


# In[ ]:


path_vector_list=[];
for item in path_seq_list:
    vector_rep=[]
    for letter in item:
        if letter=='A':
            number=0.25
        elif letter=='T':
            number=0.5
        elif letter=='C':
            number=0.75
        elif letter=='G':
            number=1
        vector_rep.append(number)
    path_vector_list.append(vector_rep)


# In[ ]:


cutoff=100000;
nonpath_list=[];

for item in nonpath_vector_list:
    i=0;
    while i+cutoff<=len(item):
        nonpath_list.append(item[i:i+cutoff]);
        i+=1;


# In[ ]:


path_list=[];

for item in path_vector_list:
    i=0;
    while i+cutoff<=len(item):
        path_list.append(item[i:i+cutoff]);
        i+=1;


# In[ ]:


path_array=np.asarray(path_list)


# In[ ]:


short_nonpath_list=random.sample(nonpath_list,len(path_list))


# In[ ]:


nonpath_array=np.asarray(short_nonpath_list)


# In[ ]:


path_labelled = np.hstack((path_array, np.atleast_2d(np.ones(len(path_array))).T))


# In[ ]:


non_path_labelled = np.hstack((nonpath_array, np.atleast_2d(np.zeros(len(nonpath_array))).T))


# In[ ]:


data=np.concatenate((non_path_labelled,path_labelled),axis=0)


# In[ ]:


y_raw=data[:,-1]
X_raw=np.delete(data,-1,axis=1)
y_raw.reshape(len(y_raw),1)


# In[ ]:


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test= train_test_split(X_raw, y_raw.reshape(len(y_raw),1), test_size=0.5, random_state=101)


# In[ ]:


np.savez('hundred_thousand_bp_trial1',X_train,y_train,X_test,y_test,'Xtrain','ytrain','Xtest','ytest')


# In[ ]:


data=np.load('hundred_thousand_bp_trial1.npz')
X_train=data['arr_0']
y_train=data['arr_1']
X_test=data['arr_2']
y_test=data['arr_3']


# In[ ]:


X_train=X_train.reshape(X_train.shape[0],X_train.shape[1],1)
X_test=X_test.reshape(X_test.shape[0],X_test.shape[1],1)
y_train=y_train.reshape(y_train.shape[0])
y_test=y_test.reshape(y_test.shape[0])


# In[ ]:


import tensorflow as tf
import math
import pickle
from tensorflow import keras
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Conv1D, MaxPooling1D, Flatten, Embedding, Dense
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.losses import BinaryCrossentropy


# In[ ]:


model = Sequential()

# kernel size here might be changed to 2
model.add(Conv1D(filters=20, kernel_size=20, padding='valid',activation='relu',input_shape=(np.shape(X_train)[1],1)))
model.add(MaxPooling1D(pool_size=2))

model.add(Conv1D(filters=20, kernel_size=18, padding='valid',activation='relu',input_shape=(np.shape(X_train)[1],1)))
model.add(MaxPooling1D(pool_size=2))

model.add(Conv1D(filters=20, kernel_size=16, padding='valid',activation='relu',input_shape=(np.shape(X_train)[1],1)))
model.add(MaxPooling1D(pool_size=2))

model.add(Conv1D(filters=20, kernel_size=10, padding='valid',activation='relu',input_shape=(np.shape(X_train)[1],1)))
model.add(MaxPooling1D(pool_size=2))

model.add(Flatten())

model.add(Dense(500,activation='relu'))
model.add(Dense(250,activation='relu'))
model.add(Dense(200,activation='relu'))
model.add(Dense(100,activation='relu'))

model.add(Dense(16,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

#opt=keras.optimizers.Adam(learning_rate=0.0001) # This learning rate is very low
opt=keras.optimizers.Adam(learning_rate=0.0001)

#model.compile(optimizer='adam',loss='mse')
#model.compile(optimizer='adam',loss='BinaryCrossentropy')

model.compile(optimizer=opt,loss='BinaryCrossentropy',metrics=['accuracy'])

model.summary()


# In[ ]:


history=model.fit(x=X_train,y=y_train,epochs=300,validation_data=(X_test,y_test),batch_size=100) 
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.plot('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train','val'],loc='upper left')
plt.show()


# In[ ]:


weights=model.get_weights()


# In[ ]:


model.save('hundredthousand_bp_model_1.h5')


# In[ ]:


loss_df=pd.DataFrame(model.history.history)
loss_df.to_csv('hundredthousand_bp_model_1.csv')
