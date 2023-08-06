import sys
import copy
from pathlib import Path
import numpy as np
import pandas as pd

from posNegEvolution.mainView import run
from posNegEvolution.pos_neg_evolution_init import posNegEvolutionMainLoop as CEML 

disclaimer = '''Cellular/Microbial Positive and Negative Mutation Effect Evolution simulations basing on Gillespie algorithm. Copyright (C) 2022 by Jarosław Gil. 
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.'''

def saveParams(dfp, output):           
    filepath = Path(output + '\\params'  + ".csv")  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    dfp.to_csv(filepath)  

def _help():
    print("Usage: if parameter is not set, default value will be used")
    print("To run grafical version of software simply type clonalEvolution without parameters")
    print("opt \t | description \t \t \t | default value")
    print("-----------------------------------------------------")
    print("-p \t | initial population size \t | 1000")
    print("-c \t | population capacity \t \t | 1000")
    print("-s \t | simulation steps (not used) \t | 100")
    print("-t \t | tau step \t \t \t | 0.005")
    print("-ct \t | cycle time \t \t \t | 1")
    print("-mp \t | mutation probabilities \t | 0.1,0.1")
    print("-me \t | mutation effects \t \t | 0.001,0.001")
    print("-l \t | mutation intensity (lambda) \t | 10")
    print("-th \t | used threads \t \t | 1")
    print("-----------------------------------------------------")
    print("mutation effects and probabilities values (positive,negative) should be separeted only by ,")
    print("more than two calues of mutation effects and probabilities are ignored")
    print("default value is set when wrong or no parameter value is provided")
    print()
    print("Additional parameters:")
    print("opt \t \t | description")
    print("-----------------------------------------------------")
    print("-out \t \t | save files localization (obligatory)")
    print("-fname \t \t | output file name (obligatory)")
    print("-par \t \t | load simulation parameters - path and file name")
    print("-save \t \t | ack to save simulation data (default: False)")
    print("-save_p \t | save params to file")
    print("-crit \t \t | print critical population value")
    print("-binned \t | type for binned version (inactive, TODO)")
    print("-----------------------------------------------------")
    print()
    print("To resume simulation provide:")
    print("-resume -par parameters_file -file file_to_resume (-save {optional}) {inactive, TODO}")
    print("In path use \\ symbol not / !")
    print()
    print(disclaimer)

def checkParams(p):
    try:
        pop = int(np.where(p == '-p')[0][0])
        pop = pop + 1
        pop = int(p[pop])
    except:
        pop = 1000
        
    try:
        cap = int(np.where(p == '-c')[0][0])
        cap = cap + 1
        cap = int(p[cap])
    except:
        cap = 1000
    
    try:
        steps = int(np.where(p == '-s')[0][0])
        steps = steps + 1
        steps = int(p[steps])
    except:
        steps = 100
    
    try:
        tau = int(np.where(p == '-t')[0][0])
        tau = tau + 1
        tau = float(p[tau])
    except:
        tau = 0.005
        
    try:
        skip = int(np.where(p == '-ct')[0][0])
        skip = skip + 1
        skip = int(p[skip])
    except:
        skip = 1
        
    try:
        mut_prob = int(np.where(p == '-mp')[0][0])
        mut_prob = mut_prob + 1
        mut_prob = p[mut_prob].split(',')
        mut_prob = [float(x) for x in mut_prob]
    except:
        mut_prob = [0.1, 0.1]
    
    try:
        mut_effect = int(np.where(p == '-me')[0][0])
        mut_effect = mut_effect + 1
        mut_effect = p[mut_effect].split(',')
        mut_effect = [float(x) for x in mut_effect]
        mut_effect[1] = -mut_effect[1]
    except:
        mut_effect = [0.001, -0.001]
       
    try:
        _lambda = int(np.where(p == '-l')[0][0])
        _lambda = skip + 1
        _lambda = int(p[_lambda])
    except:
        _lambda = 10
        
    try:
        threads = int(np.where(p == '-th')[0][0])
        threads = threads + 1
        threads = int(p[threads])
    except:
        threads = 1
        
    dfp = pd.DataFrame({
                'pop': pop,
                'cap': cap,
                'steps': steps,
                'tau': tau,
                'skip': skip,
                'mut_prob': [mut_prob],
                'mut_effect': [mut_effect],
                'lambda': _lambda,
                'threads': threads
            }, index=[0])
    print(dfp)
    return dfp

def loadParams(_in):
    dfp = pd.read_csv(_in)
    dfp = pd.DataFrame({
        'pop': int(dfp['pop'][0]),
        'cap': int(dfp['cap'][0]),
        'steps': int(dfp['steps'][0]),
        'tau': float(dfp['tau'][0]),
        'skip': float(dfp['skip'][0]),
        'mut_prob': [[float(x.strip('[]')) for x in (dfp['mut_prob'][0].split(','))]],
        'mut_effect': [[float(x.strip('[]')) for x in (dfp['mut_effect'][0].split(','))]],
        'lambda': int(dfp['lambda'][0]),
        'threads': int(dfp['threads'][0])
        }, index = [0])
    return dfp

def main():
    if len(sys.argv) == 1:
        run()
    else:
        p = np.array(sys.argv)
        if len(p[p=='-h']) > 0:
            _help()
        elif len(p[p=='-resume']) > 0:
            _in = ""
            try:
                _in = int(np.where(p == '-par')[0][0])
                _in = _in + 1
                _in = p[_in]
            except:
                print('Enter parameters file')
                return
            dfp = loadParams(_in)
            
            
        else:
            dfp = []
            if len(p[p=='-par']) > 0:
                _in = ""
                try:
                    _in = int(np.where(p == '-par')[0][0])
                    _in = _in + 1
                    _in = p[_in]
                except:
                    print('Enter parameters file')
                    return
                dfp = loadParams(_in)
            else:
                dfp = checkParams(p)
                
            output = ""
            name = ""
            plots = 0
            try:
                output = int(np.where(p == '-out')[0][0])
                output = output + 1
                output = p[output]
                
                name = int(np.where(p == '-fname')[0][0])
                name = name + 1
                name = p[name]
            except:
                print('Enter save path and name')
                return
            
            if len(p[p=="-save_p"]) > 0:
                saveParams(dfp, output)
            if len(p[p=="-crit"]) > 0:
                a = dfp['mut_prob'][0]
                b = dfp['mut_effect'][0]
                print(round((a[1]/a[0])*(b[1]/b[0]**2),0))
            if len(p[p=="-save"]) > 0:
                plots = 16
    
            if len(p[p=="-binned"]) > 0:
                print("binned version is incomplete")
            else:                                
                iMuts = np.zeros(dfp['pop'][0], dtype=np.int64).tolist()
                iProp = np.ones(dfp['pop'][0]).tolist()
                
                CEML(np.array([
                        copy.deepcopy(iProp), 
                        copy.deepcopy(iMuts), 
                        copy.deepcopy(iMuts)]).T.tolist(), 
                        copy.deepcopy([dfp['pop'][0], dfp['cap'][0], dfp['steps'][0], dfp['tau'][0], dfp['skip'][0], dfp['mut_prob'][0], dfp['mut_effect'][0], dfp['lambda'][0], dfp['threads'][0]]), 
                        name, "", output, plots=plots)           
                                         
            
if __name__ == "__main__":
    main()