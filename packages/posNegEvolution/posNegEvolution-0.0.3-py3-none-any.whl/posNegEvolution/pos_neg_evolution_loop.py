import numpy as np
import math
from threading import Thread

def division(i, c, m_d, m_p, iPop, mut_effect, mut_prob, lmbd):   
    if m_d[i] or m_p[i] :
        prop = c[0]
        mut_p = c[1]
        mut_n = c[2]
        
        if m_d[i]:
            mut_num = 1#np.random.poisson(lmbd)
            prop = prop*((1+mut_effect[0])**mut_num)
            mut_p = mut_p + mut_num
        if m_p[i]:
            mut_num = 1#np.random.poisson(lmbd)
            prop = prop/((1-mut_effect[1])**mut_num)
            mut_n = mut_n + mut_num        
            
        try:
            iPop.append([prop, mut_p, mut_n])
        except:
            print("cell dead")
    else:
        try:
            iPop.append(c)
        except:
            print("cell dead")

def death(val, iPop):
    iPop.remove(val)

def th_div(pdv, pdv_idx, c, m_d, m_p, iPop, mut_effect, mut_prob, lmbd):
    t = pdv[c[0]:c[1]]
    for i in range(len(t)):
        division(pdv_idx[i], t[i], m_d, m_p, iPop, mut_effect, mut_prob, lmbd)
    
def th_dth(pdt, c, iPop):
    t = pdt[c[0]:c[1]]
    for i in reversed(t):
        death(i, iPop)
        
def prob_dvd(pdv, pdv_idx, idx_dvd, popSize, iPop, tau, THREADS):
    pdvx = np.random.exponential(1,popSize)
    pdvx = np.array([pdvx[i]/iPop[i][0] for i in range(popSize)])
    pdvx = np.where(pdvx < tau)[0] 
    pdv_idx.extend(pdvx)
    pdv.extend([iPop[pdvx[x]] for x in range(len(pdvx))])
    
    th = math.ceil(len(pdvx)/THREADS)
    idx_dvdx = [(int(x*th),int((x+1)*th)) for x in range(THREADS)]
    idx_dvdx[len(idx_dvdx)-1] = (idx_dvdx[len(idx_dvdx) - 1][0], len(pdvx))
    idx_dvd.extend(idx_dvdx)
    
def prob_dth(pdt, idx_dth, popSize, iPop, tau, mdt, THREADS):
    pdtx = np.random.exponential(1, popSize)
    pdtx = np.array([pdtx[i]/(mdt) for i in range(popSize)])
    pdtx = np.where(pdtx < tau)[0]    
    pdt.extend([iPop[pdtx[x]] for x in range(len(pdtx))])

    th = math.ceil(len(pdtx)/THREADS)
    idx_dthx = [(int(x*th),int((x+1)*th)) for x in range(THREADS)]
    idx_dthx[len(idx_dthx)-1] = (idx_dthx[len(idx_dthx) - 1][0], len(pdtx))  
    idx_dth.extend(idx_dthx)
    
#Fitness, Positive, NEgative
def posNegEvolutionLoop(iPop, cap, tau, mut_prob, mut_effect, resume, q, lmbd, THREADS):
    """    
    Description:
        One cycle to update population - tau loop iteration method
        Prameters:
            iPop: population matrix where row is in form of:
                Fitness
                Positive mutation number
                Negative mutation number
            cap: population capacity
            tau: tau step
            mut_prob: list in form of: [driver mutation probability, passenger mutation probability]
            mut_effect: list in form of: [driver mutation effect, passenger muatation effect]
            resume: acknowledge to resume simulation !!TODO!!
            q: common queue
            THREADS: threads number used in simulation !!TODO!!            
    """
    popSize = len(iPop)
    mdt = popSize/cap

    m_d = np.random.binomial(1, mut_prob[0], popSize)
    m_p = np.random.binomial(1, mut_prob[1], popSize)
    
    pdt = []
    pdv = []
    pdv_idx = []
    
    idx_dth = []
    idx_dvd = []
    
    dth = Thread(target=prob_dth, args=(pdt, idx_dth, popSize, iPop, tau, mdt, THREADS))
    dth.start()
    dvd = Thread(target=prob_dvd, args=(pdv, pdv_idx, idx_dvd, popSize, iPop, tau, THREADS))
    dvd.start()
    
    dth.join()
    dvd.join()
    
    # print(pdv)
    
    divides = []

    for i in range(len(idx_dvd)):
        divides.append(Thread(target=th_div, args=(pdv, pdv_idx, idx_dvd[i], m_d, m_p, iPop, mut_effect, mut_prob, lmbd)))
        divides[i].start()

    deaths = []
  
    for i in range(len(idx_dth)):
        deaths.append(Thread(target=th_dth, args=(pdt, idx_dth[i], iPop)))
        deaths[i].start()
        
    for i in divides:
        i.join()    
    for i in deaths:
        i.join()

    return iPop