import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")


from keras.preprocessing import sequence
from keras.models import Sequential,Model
from keras.layers import Flatten, Dense,Embedding,SimpleRNN,LSTM,Activation,Dropout,Input
from keras.wrappers.scikit_learn import KerasClassifier

import matplotlib.pyplot as plt
import pickle 



def rnnSimple(max_len,max_words,dim_embedding, activation='sigmoid'):
    '''
    Max length of the sequence -> sequence of integers
    Max words                  -> integer (max value of the values of sequence)
    dim_embedding              -> integer (if equal to max_len, then ebbending is "switched off")
    returns a RNN model        
    '''
      

    model = Sequential()
    model.add(Embedding(max_words, dim_embedding, input_length=max_len)) 
    model.add(SimpleRNN(dim_embedding))
    model.add(Dense(1, activation=activation))
    return model


def LstmR(max_len, max_words, dim_embedding, neurons, neuronsHL, dropOut_rate):
    '''
    Max length of the sequence ->   integer
    Max words                  ->   integer 
    Dim_embedding              ->   integer
    Neurons                    ->   integer (forming the neural networks)
    NeuronsHL                  ->   integer (forming the hidden layer of the neural networks)
    DropOut_rate               ->   float (percentage of neurons to switch off)
    
                
    returns a LstmR model
    
    '''
    model = Sequential()
    model.add(Embedding(max_words,dim_embedding,input_length=max_len, name='features'))
    model.add(LSTM(neurons))
    model.add(Dense(neuronsHL, activation='relu',name='FC1'))
    model.add(Dropout(dropOut_rate))
    model.add(Dense(1, activation='sigmoid',name='out_layer'))
    return model

def create_Sequence(X, events, path):
    
    ''' 
    X              -> list of triples containing three elements (coordinates:(x,y) and list of events)
    events         -> list of all events in the game 
    path           -> path where the files exstracted of games and target are located

    It returns 4 elements: 
    statsLenSeq    -> list containing all the length of each sequence for each game
    allSequences   -> list of all sequences for all games
    Yseq           -> target variable (0: 'Lose', 1: 'Win')
    control        -> bool (when true, indicated that X and Y have the same length)
    '''

    statsLenSeq = []
    allSequences = []
    for sequence in X:
        xs = []
        ys = []
        allSeqPlayer = []
        for movements in sequence:
            x = int(movements[0]/150)
            y = int(movements[1]/150)
            v = 100 * x + y
            seqf = [v]
            for k in movements[2]:
                seqf.append(events[k])

            for s in seqf:
                allSeqPlayer.append(s)
        allSequences.append(allSeqPlayer)
        statsLenSeq.append(len(allSeqPlayer))
    Ys = pickle.load(open(path+"Y_seq.pkl","rb"))
    Yseq = [int(b) for b in Ys]
    control = len(Ys)==len(allSequences)
    pickle.dump(allSequences,open("WseqX.pickle","wb"))
    pickle.dump(Yseq,open("WseqY.pickle","wb"))
   
        
        
    return statsLenSeq, allSequences, Yseq, control

def getDifferantialPace(X):
    ''' 
    X              -> list of triples containing three elements (coordinates:(x,y) and list of events)
   
    It returns 2 elements: 
    allDx    -> list containing all differential movements of each player from frame to its subsequential frame
    allDy    -> list (same as allDy)
    
    
    '''
     
    xs = []
    ys = []
    for sequence in X:
        for movements in sequence:
            xs.append(movements[0])
            ys.append(movements[1])
    xsArray=np.array(xs)
    ysArray=np.array(ys)
    diffx = np.diff(xsArray)
    diffy = np.diff(ysArray)
    allDx = []
    allDy = []
    for d in diffx:
        allDx.append(abs(d))
        allDy.append(abs(d))
    return allDx, allDy

def plotValidationAcc(history, accuracy= 'acc', val_accuracy= 'val_acc', figsize=(12,8), fontsize = 14):
    '''
    history of results among the epochs
    accuracy is a string uqual to 'acc' or 'accuracy' depending on what history dataframe has
    generated as a column

    returns the plot of validation accuracys

    '''
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.plot(range(1,len(history.history[accuracy])+1), history.history[accuracy], 'b', label='Training Accuracy ')
    ax.plot(range(1,len(history.history[accuracy])+1), history.history[val_accuracy], 'b', label='Validation Accuracy ' ,       color='red')
    ax.set_title('Validation and Training Accuracy RNN',fontsize=fontsize)
    ax.set_xlabel('Epochs',fontsize=fontsize)
    ax.set_ylabel('Accuracy',fontsize=fontsize)
    ax.legend()
    
    
def plotValidationLoss(history, accuracy = 'acc', figsize=(12,8), fontsize = 14): 
    '''
    history of results among the epochs
    accuracy is a string uqual to 'acc' or 'accuracy' depending on what history dataframe has
    generated as a column

    returns the plot of validation loss
    '''
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.plot(range(1,len(history.history[accuracy])+1), history.history['loss'], 'b', label='Training Loss')
    ax.plot(range(1,len(history.history[accuracy])+1), history.history['val_loss'], 'b', label='Validation Loss' ,     color='red')
    ax.set_title('Validation and Training Loss',fontsize=fontsize)
    ax.set_xlabel('Epochs',fontsize=fontsize)
    ax.set_ylabel('Loss',fontsize=fontsize)
    ax.legend()
    
    
def DiffplotValidationAcc(history, historyP, accuracy = 'acc', val_accuracy= 'val_acc',figsize=(12,8), fontsize = 14):
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.plot(range(1,len(history.history[accuracy])+1), history.history[accuracy], 'b', label='Training Accuracy ')
    ax.plot(range(1,len(history.history[accuracy])+1), history.history[val_accuracy], 'b', label='Validation Accuracy ' , color='red')
    ax.plot(range(1,len(historyP.history[accuracy])+1), historyP.history[accuracy], 'b', label='Training Accuracy powerful model (LSTM)', color='orange')
    ax.plot(range(1,len(historyP.history[accuracy])+1), historyP.history[val_accuracy], 'b', label='Validation Accuracy powerful model (LSTM)' , color='green')
    ax.set_title('Validation and Training Accuracy RNN/LSTM',fontsize=fontsize)
    ax.set_xlabel('Epochs',fontsize=fontsize)
    ax.set_ylabel('Accuracy',fontsize=fontsize)
    ax.legend()
    
   
    
    
def DiffplotValidationLoss(history,historyP ,figsize=(12,8), fontsize = 14):
    fig = plt.figure(figsize=figsize)
    ax = plt.gca()
    ax.plot(range(1,len(history.history['loss'])+1), history.history['loss'], 'b', label='Training Loss ')
    ax.plot(range(1,len(history.history['loss'])+1), history.history['val_loss'], 'b', label='Validation Loss ' , color='red')
    ax.plot(range(1,len(historyP.history['loss'])+1), historyP.history['loss'], 'b', label='Training Loss powerful model (LSTM)', color='orange')
    ax.plot(range(1,len(historyP.history['loss'])+1), historyP.history['val_loss'], 'b', label='Validation Loss  powerful model (LSTM) ' , color='green')
    ax.set_title('Validation and Training Loss RNN/LSTM',fontsize=fontsize)
    ax.set_xlabel('Epochs',fontsize=fontsize)
    ax.set_ylabel('Loss',fontsize=fontsize)
    ax.legend()