# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 16:40:31 2017

@author: jhudson
"""

import tensorflow as tf
import numpy.random as rnd
import cryptoFunctions as cf
import numpy as np
import pandas as pd

glbNameHold = 1

def fitLSTM(X_data,y_data):
    global glbNameHold
    n_neurons = 100
    n_layers = 1
    learning_rate = 0.0001
    n_steps = 100
#    n_inputs = 3
    n_inputs = np.shape(X_data)[2]
    n_outputs = 1
    
    X = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
    y = tf.placeholder(tf.float32, [None, n_steps, n_outputs])
    cell = tf.contrib.rnn.BasicLSTMCell(num_units=n_neurons)
    rnn_outputs, states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
    
    stacked_rnn_outputs = tf.reshape(rnn_outputs, [-1, n_neurons])
    stacked_outputs = tf.contrib.layers.fully_connected(stacked_rnn_outputs, n_outputs, activation_fn=None)
    outputs = tf.reshape(stacked_outputs, [-1, n_steps, n_outputs])
    
    loss = tf.reduce_mean(tf.square(outputs-y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    training_op = optimizer.minimize(loss)
    
    init = tf.global_variables_initializer()
    saver = tf.train.Saver()
    
    n_iterations = 115000
    batch_size = 1
    
    file_path = "/tmp/my_model" + str(glbNameHold) + ".ckpt"
    
    with tf.Session() as sess:
        init.run()
        for iteration in range(n_iterations):
            shuffled_idx = rnd.permutation(len(X_data))
#            X_batch, y_batch = [X_data[:,:,shuffled_idx[0:batch_size]], y_data[:,:,shuffled_idx[0:batch_size]]]
            X_batch, y_batch = [X_data[shuffled_idx[0:batch_size],:,:], y_data[shuffled_idx[0:batch_size],:,:]]
            X_batch = X_batch.reshape((-1,n_steps,n_inputs))
            y_batch = y_batch.reshape((-1,n_steps,n_outputs))
            X_batch = np.float32(X_batch)
            y_batch = np.float32(y_batch)
            sess.run(training_op, feed_dict={X: X_batch, y: y_batch})
            if iteration % 100 == 0:
                mse = loss.eval(feed_dict={X: X_batch, y: y_batch})
                print(iteration, "\tMSE:", mse)
        save_path = saver.save(sess, "/tmp/my_model.ckpt")
        save_path = saver.save(sess, file_path)
        
    glbNameHold = glbNameHold + 1
    out = [file_path, n_steps, n_inputs]
    return(out)
        
def predLSTM(X_data, info, steps = 1):        
    with tf.Session() as sess:
#        saver.restore(sess, "/tmp/my_model.ckpt")
        saver.restore(sess, info[0])
#        sequence = [0.]*n_steps
        sequence = X_data[0,:,:]
#        for iteration in range(20):
        for iteration in range(steps):
#            X_batch = np.array(sequence[-n_steps:]).reshape(-1, n_steps, n_inputs)
            X_batch = sequence.reshape(-1,n_steps,n_inputs)
            X_batch = sequence.reshape(-1,info[1],info[2])
            y_pred = sess.run(outputs, feed_dict={X: X_batch})
#            sequence.append(y_pred[0, -1, 0])
            tmp = np.insert(np.asarray(y_pred[0, -1, 0]),1,X_data[iteration+1,-1,1:])
            sequence = np.append(sequence[1:],tmp.reshape(1,3),axis=0)
            
            
            
#def cutData(data):
#    Xtmp = btcusdOHLC.Open
#    ytmp = btcusdOHLC.Close
#    
#    X1 = btcusdOHLC.Open
#    X2 = ethusdOHLC.Open
#    X3 = ltcusdOHLC.Open
#    ytmp = btcusdOHLC.Close
#    ytmp = ytmp.values.reshape(len(ytmp),1)
#    
#    Xtmp = pd.concat([X1,X2,X3],axis=1)
#    
#    stds = np.std(Xtmp)
#    means = np.mean(Xtmp)
#    
#    Xtmp = pd.DataFrame((Xtmp.values - means.values.reshape(1,3))*(1/stds.values))
#    ytmp = (ytmp - np.mean(ytmp))*(1/np.std(ytmp))
#    
#    X_data = np.zeros(shape=(400,n_steps,n_inputs))
#    y_data = np.zeros(shape=(400,n_steps,n_outputs))
#    
#    top = 
#    
#    for i in range(0,400):
#        X_data[i,:,:] = Xtmp.values[i:(i+100),:]
#        y_data[i,:,:] = ytmp[i:(i+100)]
#    
#    del Xtmp, ytmp, i, X1, X2, X3
#    X_data = Xtmp.loc[range(n_steps),:]
#    y_data = ytmp.loc[range(n_steps)]
#    
#    Xtmp = Xtmp.drop(0)
#    Xtmp.index = range(0,len(Xtmp))
#    ytmp = ytmp.drop(0)
#    ytmp.index = range(0,len(ytmp))
#    
#    for i in range(0,len(Xtmp)):
#        X_data = pd.concat([X_data, pd.DataFrame(Xtmp.loc[0:n_steps,:], index = X_data.index)],axis = 1)
#        Xtmp = Xtmp.drop(0)
#        Xtmp.index = range(0,len(Xtmp))
#        y_data = pd.concat([y_data, pd.Series(ytmp[0:n_steps], index = y_data.index)],axis = 1)
#        ytmp = ytmp.drop(0)
#        ytmp.index = range(0,len(ytmp))
#        
#    X_data = X_data.fillna(0)
#    y_data = y_data.fillna(0)
#    X_datac = X_data.values.reshape((-1,n_steps,3), order='C')
#    y_datac = y_data.values.reshape((-1,n_steps,1), order='C')
#    X_dataf = X_data.values.reshape((-1,n_steps,3), order='F')
#    y_dataf = y_data.values.reshape((-1,n_steps,1), order='F')
#    X_dataa = X_data.values.reshape((-1,n_steps,3), order='A')
#    y_dataa = y_data.values.reshape((-1,n_steps,1), order='A')
    
def prepData(Xin,yin,time_steps):
    if(len(np.shape(Xin)) != 2):
        raise ValueError('oops')
    cols = np.shape(Xin)[1]
    np.shape(Xin)
    rows = np.shape(Xin)[0]
    means = np.mean(Xin)
    stds = np.mean(Xin)
    Xtmp = pd.DataFrame((Xin.values - means.values.reshape(1,cols))*(1/stds.values))
    ytmp = (yin - np.mean(yin))*(1/np.std(yin))
    
    top = rows - (time_steps - 1)
    
    X_data = np.zeros(shape=(top,time_steps,cols))
    y_data = np.zeros(shape=(top,time_steps,1))
    
    for i in range(top):
        X_data[i,:,:] = Xtmp.values[i:(i+time_steps),:]
        y_data[i,:,:] = ytmp[i:(i+100)]
        
    return X_data, y_data
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        