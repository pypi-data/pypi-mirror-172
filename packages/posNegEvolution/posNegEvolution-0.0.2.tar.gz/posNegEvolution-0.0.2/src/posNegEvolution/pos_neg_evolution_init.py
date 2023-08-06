from IPython.core.debugger import Pdb
import matplotlib.pyplot as plt
import numpy as np
import time
import copy
import os
import pandas as pd
from pathlib import Path  
from threading import Thread
from queue import Queue

from posNegEvolution.pos_neg_evolution_loop import posNegEvolutionLoop as PNEL
  
end = False
  
def waveMut_ar(iMuts, iClones, cln):
    muts = iMuts
    clones = iClones
    m_u = []
    c_u = []
    
    mim = int(min(muts))
    mxm = int(max(muts))
    m_u = [x for x in range(mim, mxm+1)]
    if cln:
        for i in clones:
            if i not in c_u:
                c_u.append(i)
    else:
        c_u = [0]
    TAB = np.zeros((mxm-mim+1,len(c_u)+1))
    c_u.sort()
    t = [(muts[i], clones[i]) for i in range(len(muts))]
    for m,c in t:
        if cln:
            ci = c_u.index(c)
        else:
            ci = 0
        xx = TAB[m-mim][ci+1] 
        TAB[m-mim][ci+1] = xx + 1
        TAB[m-mim][0] = m
    
    return muts, clones, m_u, c_u, TAB

def saveToFile(df, file_localization, file_name, iter_outer, ending='.csv'):    
    filepath = Path(file_localization + '\\' + file_name + '_' + str(iter_outer) + ending)      
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    df.to_csv(filepath)  

def mutationWavePlot(iMuts, iClones=None, cln=0, name="", local="", f_num=0, ret=0):
    print("inavaliable, TODO")

def fitnessWavePlot(iProp, iClones=None, cln=0, name="", local="", f_num=0):
    print("inavaliable, TODO")

def commands(q, ID, iPop, file_localization, file_name, iter_outer, skip, iter_inner, cycle, tau):
    global end
    queue_data = q.get()
    # print(queue_data)
    if(queue_data[0] == '1' and queue_data[1] == str(ID)):
        if(queue_data[2] == "exit"):
            print("exit")
            end = True
        elif(queue_data[2] == "size"):
            q.put(['0', str(ID), str(len(iPop))])
        elif(queue_data[2] == "time"):
            q.put(['0', str(ID), str((iter_outer-1)*skip + (iter_inner%cycle)*tau)])
        elif(queue_data[2] == "save"):
            tsf = Thread(target=saveToFile, args=(pd.DataFrame({
                                                        'Fitness': [row[0] for row in iPop],
                                                        'Positive mutations': [row[1] for row in iPop],
                                                        'Negative mutations': [row[2] for row in iPop],
                                                    }),  
                                                  file_localization, file_name, iter_outer, ".csv"))
            tsf.start()
        elif(queue_data[2] == "corr_plot"):        
            mutWave = []
            for cell in iPop:
                mutWave.append([cell[1], cell[2]])
            q.put(["-1", str(ID), np.array(mutWave).T])
        elif(queue_data[2] == "mut_wave"):
            mutWave = []
            for cell in iPop:
                mutWave.append([cell[1], cell[2]])
            q.put(["-2", str(ID), np.array(mutWave)])
    else:
        q.put(queue_data)
 
    
def plotter(iPop, file_name, file_localization, iter_outer, plots, select):
    if select == 0:
        if plots & 1:
            tsf = Thread(target=mutationWavePlot, args=([row[0] for row in iPop], 
                                                        [row[2] for row in iPop], 
                                                        1, file_name, file_localization, iter_outer, 0))
            tsf.start()

        if plots & 2:
            tsf = Thread(target=fitnessWavePlot, args=([row[1] for row in iPop], 
                                                       [row[2] for row in iPop],
                                                        0, file_name, file_localization, iter_outer))
            tsf.start()
        
        if plots & 16: 
            tsf = Thread(target=saveToFile, args=(pd.DataFrame({
                                                        'Fitness': [row[0] for row in iPop],
                                                        'Positive mutations': [row[1] for row in iPop],
                                                        'Negative mutations': [row[2] for row in iPop],
                                                    }),  
                                                  file_localization, file_name, iter_outer))
            tsf.start()
    
#iMuts, iProp, iClones, iMutations, iEffect
def posNegEvolutionMainLoop(iPop, params, file_name="", file_description="", file_localization="", plots=0, t_iter=0, q=None, ID=0, select=0):
    global end
    """
    Main simulation loop
        iPop: population matrix where row is in form of:
            Fitness: fitness parameter
            Positive mutation number
            Negative mutation number
        params: simulation parameters with structure 
        [initial population size, population capacity, simulation steps number, tau step [s], one cycle time [s], 
         mutation probability (list) adequate index for mutation effect, mutation effect (list), mutations intesity, number of threads]
        file_name: save file name, data will be saved to file_name.csv, figures: file_name_typeofplot.jpg
        file_localization: path to file, figures will be saved in path: file_localization/Figures/Cycle_number
        plots: binary interpreted value defines which plots will be generated: 
            1 - mutation wave
            2 - fitness wave
            16 - ack to save data
        t_iter - value of starting iteration (for resume t_iter != 0)
        q - queue to comunicate with simulation in thread
        ID - simulation ID
        select - 0 normal, 1 binned
    """
    cap = params[1]
    steps = params[2]
    tau = params[3]
    skip = params[4]
    mut_effect = params[6]
    mut_prob = params[5]
    lmbd = params[7]
    threads = params[8]

    iter_inner = 0 + 1*(t_iter>0)
    begin = 0 + 1*(t_iter==0)
    iter_outer = t_iter
    resume = 0 + 1*(t_iter>0)
    cycle = round(skip/tau)
    
    t = time.time()

    while 1:   
        if q != None:
            if not q.empty():
                commands(q, ID, iPop, file_localization, file_name, iter_outer, skip, iter_inner, cycle, tau)

        if end:
            break

        if iter_inner % cycle == 0 or begin:
            begin = 0
            t = time.time() - t  
            print(str(ID) + ':' + str(t))
            
            plotter(iPop, file_name, file_localization, iter_outer, plots, select)

            iter_outer = iter_outer + 1            
            t = time.time()
        
        if iter_outer % steps == 0:
            print("pointer")
        
        if select == 0:            
            iPop = PNEL(iPop, cap, tau, mut_prob, mut_effect, resume, q, lmbd, threads)

        resume = 0
        iter_inner = iter_inner + 1
             