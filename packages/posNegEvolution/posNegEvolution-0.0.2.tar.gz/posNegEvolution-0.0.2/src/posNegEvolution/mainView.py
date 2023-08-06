import PyQt5.QtWidgets as qtWidget
import PyQt5.QtGui as qtGui
from PyQt5.QtCore import Qt
import sys
import pandas as pd
import numpy as np
import statistics
from pathlib import Path 
import time
import matplotlib.pyplot as plt
from threading import Thread
from queue import Queue
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import copy

from posNegEvolution.pos_neg_evolution_init import posNegEvolutionMainLoop as pnEML 

disclaimer = '''Cellular/Microbial Positive and Negative Mutation Effect Evolution simulations basing on Gillespie algorithm. Copyright (C) 2022 by Jarosław Gil. 
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to redistribute it
    under certain conditions.'''

class mainFormat(qtWidget.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ID = 1
        self.idx_s = 0
        self._monitor = True
        self.idx_r = 0
        self.th_r = []
        self.r_ID = []
        self.th_s = []
        self.s_ID = []
        self.q = Queue()
        self.createMainView()
        self._monitor = True
        self.th_monitor = Thread(target=self.monitor, args=(self.q, self.status))
        self.th_monitor.start()
    
    def plot(self, ID, mutWave, select):
        self._fig.clear()
        ax = self._fig.add_subplot(111)     
        
        if select == 0:
            ax.scatter(mutWave[0,:], mutWave[1,:])
            ax.set_title("Population: %i, ID: %s, correlation: %.3f" % (len(mutWave[0,:]), ID, statistics.correlation(mutWave[0,:], mutWave[1,:])))
            ax.set_xlabel("Positive mutations")
            ax.set_ylabel("Negative mutations")
        elif select == 1:
            pos = []
            neg = []
            _sum = []
            for i in mutWave:
                if i[0] + i[1] not in _sum:
                    _sum.append(i[0]+i[1])
                    pos.append(i[0])
                    neg.append(i[1])
                else:
                    idx = _sum.index(i[0]+i[1])
                    pos[idx] = pos[idx] + i[0]
                    neg[idx] = neg[idx] + i[1]
                    
            ax.bar(_sum, pos)
            ax.bar(_sum, neg, bottom=pos)  
            ax.set_title("Population: %i, ID: %s" % (len(mutWave[:,0]), ID))
            ax.set_xlabel("Mutation number")
            ax.set_ylabel("Cells number")
            
        self._canvas.draw()
        self.status.setText(ID + ": PLOTTED")
    
    def monitor(self, q, status):
        while self._monitor:
            if not q.empty():
                data = q.get()
                if data[0] == '0':
                    status.setText(data[1] + ": " + data[2])
                elif data[0] == '-1':
                    status.setText(data[1] + ": correlation plot")
                    self.plot(data[1], data[2], 0)
                elif data[0] == '-2':
                    status.setText(data[1] + ": mutation wave")
                    self.plot(data[1], data[2], 1)
                else:
                    q.put(data)
    
    def about(self):
        global disclaimer
        self.showDialog(disclaimer, 'About')
    
    def closeEvent(self, event):        
        for i in self.s_ID:
            self.q.put(['1', str(i), "exit"])
        for i in self.r_ID:
            self.q.put(['1', str(i), "exit"])
        
        for i in self.th_r:
            i.join()
        for i in self.th_s:
            i.join()
            
        self._monitor = False
        plt.close(self._fig)
        self.th_monitor.join()
        event.accept()  
    
    def update(self):
        i = self.tabs.indexOf(self._tabUI)
        self.tabs.removeTab(i)
        self._tabUI = self.threadTabUI()
        self.tabs.addTab(self._tabUI, "Active threads")
    
    def stopSim(self):
        msg = self._msg.text()
        msg = msg.split(',')
        ID = msg[0]
        msg = msg[1]
        self.q.put(['1',ID,msg])
        index = 0
        if msg == "exit":
            try:
                index = self.s_ID.index(ID)
                self.s_ID.remove(ID)
                self.th_s[index].join()
                self.th_s.remove(self.th_s[index])
                self.idx_s = self.idx_s - 1
            except:
                index = self.r_ID.index(ID)
                self.r_ID.remove(ID)
                self.th_r[index].join()
                self.th_r.remove(self.th_r[index])
                self.idx_r = self.idx_r - 1
            
            self.status.setText("Stopped")
            if not self.th_r and not self.th_s:
                self.status.setStyleSheet("background-color: red")
    
    def createCanvasView(self):
        self.canvasTab = qtWidget.QWidget()
        _canvasTab = qtWidget.QVBoxLayout()
        
        self._fig = plt.figure()
        self._canvas = FigureCanvas(self._fig)
        self._toolbar = NavigationToolbar(self._canvas, self)
        
        _canvasTab.addWidget(self._toolbar)
        _canvasTab.addWidget(self._canvas)
        
        self.canvasTab.setLayout(_canvasTab)
        return self.canvasTab  
    
    def createMainView(self):
        layout = qtWidget.QVBoxLayout()
        # Create the tab widget with two tabs
        self.tabs = qtWidget.QTabWidget()
        self.tabs.addTab(self.generalTabUI(), "General")
        self.tabs.addTab(self.generatedTabUI(), "Generated")
        self.tabs.addTab(self.parametersTabUI(), "Parameters")
        self.tabs.addTab(self.createCanvasView(), "Plot")
        self._tabUI = self.threadTabUI()
        self.tabs.addTab(self._tabUI, "Active threads")
        layout.addWidget(self.tabs)
        layout.addStretch()
        
        self._binned = qtWidget.QCheckBox("Checked: binned version")
        layout.addWidget(self._binned)
        
        start = qtWidget.QPushButton(self)
        start.setText("Start simulation")
        start.clicked.connect(self.simStart)
        layout.addWidget(start)
        
        self.status = qtWidget.QLabel()
        self.status.setStyleSheet("background-color: red")
        self.status.setText("Stopped")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setFont(qtGui.QFont('Consolas', 15))  # this is what you need!
        layout.addWidget(self.status)
        
        send_msg = qtWidget.QPushButton(self)
        send_msg.setText("Send message")
        send_msg.clicked.connect(self.stopSim)
        layout.addWidget(send_msg)
        
        layout.addWidget(qtWidget.QLabel("message format: thread_ID,command (without space)"))
        layout.addWidget(qtWidget.QLabel("commands: exit - stop simulation, size - get population size, time - get simulation time"))
        layout.addWidget(qtWidget.QLabel("corr_plot - correlation plot, mut_wave - mutation wave plot, save - save to file"))
        
        self._msg = qtWidget.QLineEdit()
        self._msg.returnPressed.connect(self.stopSim)
        layout.addWidget(self._msg)
        
        self.setLayout(layout)
        
    def threadTabUI(self):
        self.threadTab = qtWidget.QWidget()
        _threadTab = qtWidget.QFormLayout()
        
        _refresh = qtWidget.QPushButton("Refresh")
        _refresh.clicked.connect(self.update)
        
        _threadTab.addRow("ID", _refresh)
        _threadTab.addRow("Started", qtWidget.QLabel())
        for i in self.s_ID:
            _threadTab.addRow(qtWidget.QLabel("ID: " + str(i)), qtWidget.QLabel())
        _threadTab.addRow(qtWidget.QLabel("Resumed"), qtWidget.QLabel())
        for i in self.r_ID:
            _threadTab.addRow(qtWidget.QLabel("ID: " + str(i)), qtWidget.QLabel())            

        self.threadTab.setLayout(_threadTab)
        return self.threadTab        
        
    def generalTabUI(self):
        """Create the General page UI."""
        generalTab = qtWidget.QWidget()
        _generalTab = qtWidget.QGridLayout()
        
        self._file_name = qtWidget.QLineEdit()
        _file_name_label = qtWidget.QLabel()
        _file_name_label.setText('File name')
        self._file_path = qtWidget.QLineEdit()
        _file_path_label = qtWidget.QLabel()
        _file_path_label.setText('File path')
        _file_path_button = qtWidget.QPushButton(self)
        _file_path_button.setText('Select path')
        _file_path_button.clicked.connect(self.selectPath)
        self._file_desc = qtWidget.QLineEdit()
        _file_desc_label = qtWidget.QLabel("TODO")
        _file_desc_label.setText('Description')
        _file_instr_fn = qtWidget.QLabel()
        _file_instr_fn.setText('File name - one cycle file name will appear with cycle number')
        _file_instr_fp = qtWidget.QLabel()
        _file_instr_fp.setText('File path - archive directory')
        _file_instr_fd = qtWidget.QLabel()
        _file_instr_fd.setText('Description - most important information to add to file')
        
        _generalTab.addWidget(_file_name_label, 0, 0)
        _generalTab.addWidget(self._file_name, 0, 1, 1, 2)
        _generalTab.addWidget(_file_path_label, 1, 0)
        _generalTab.addWidget(self._file_path, 1, 1)
        _generalTab.addWidget(_file_path_button, 1, 2)
        _generalTab.addWidget(_file_desc_label, 2, 0, 1, 3)
        _generalTab.addWidget(self._file_desc, 3, 0, 2, 3)
        _generalTab.addWidget(_file_instr_fn, 5, 0, 1, 3)
        _generalTab.addWidget(_file_instr_fp, 6, 0, 1, 3)
        _generalTab.addWidget(_file_instr_fd, 7, 0, 1, 3)
        
        generalTab.setLayout(_generalTab)
        return generalTab
    
    def generatedTabUI(self):
        generatedTab = qtWidget.QWidget()
        _generatedTab = qtWidget.QGridLayout()
        
        _file_instr = qtWidget.QLabel()
        _file_instr.setText('Select figures to generate (and save optionally in file directory)')
        self._mw = qtWidget.QCheckBox("Mutation Wave")
        self._fw = qtWidget.QCheckBox("Fitness Wave")
        self._sx = qtWidget.QCheckBox("Save files")
        
        _generatedTab.addWidget(_file_instr)
        _generatedTab.addWidget(self._mw)
        _generatedTab.addWidget(self._fw)
        _generatedTab.addWidget(self._sx)
        
        generatedTab.setLayout(_generatedTab)
        return generatedTab
    
    def parametersTabUI(self):
        parametersTab = qtWidget.QWidget()
        _parametersTab = qtWidget.QGridLayout()
        
        self._population = qtWidget.QLineEdit(str(10**6))
        self._population.setValidator(qtGui.QIntValidator(0, 10**7))
        
        self._capacity = qtWidget.QLineEdit(str(10**6))
        self._capacity.setValidator(qtGui.QIntValidator(0, 10**7))
        
        self._steps = qtWidget.QLineEdit(str(100))
        self._steps.setValidator(qtGui.QIntValidator(0, 10**5))
        
        self._tau = qtWidget.QLineEdit(str(0.005))     
        self._tau.setValidator(qtGui.QDoubleValidator(0.000, 1.000, 3))
        
        self._skip = qtWidget.QLineEdit(str(10))
        self._skip.setValidator(qtGui.QDoubleValidator(0.1, 100.0, 1))
        
        self._mut_effect = qtWidget.QLineEdit(".1, -.001")
        self._mut_effect.setInputMask("[#.#####, #.#####]")
        self._mut_prob = qtWidget.QLineEdit("0.0001, 0.05")        
        self._mut_prob.setInputMask("[#.#####, #.#####]")
        
        self._lambda = qtWidget.QLineEdit(str(10))
        self._lambda.setValidator(qtGui.QIntValidator(0, 10**2))
        
        self._threads = qtWidget.QLineEdit(str(16))
        self._threads.setValidator(qtGui.QIntValidator(1, 2**10))
        
        _load_params = qtWidget.QPushButton(self)
        _load_params.setText('Load parameters')
        _load_params.clicked.connect(self.loadParams)
        
        _resume_button = qtWidget.QPushButton(self)
        _resume_button.setText('Resume simulation - Load File')
        _resume_button.clicked.connect(self.resume)
        
        _save_params = qtWidget.QPushButton(self)
        _save_params.setText('Save Parameters')
        _save_params.clicked.connect(self.saveParams)
        
        _calculate_crit = qtWidget.QPushButton(self)
        _calculate_crit.setText('Calculate critical population')
        _calculate_crit.clicked.connect(self.critPop)
        
        _file_instr_1 = qtWidget.QLabel()
        _file_instr_1.setText('Simulation time = steps * cycle time')
        _file_instr_2 = qtWidget.QLabel()
        _file_instr_2.setText('Mutation effect and probability are consistent lists')
        
        row = 0
        _parametersTab.addWidget(qtWidget.QLabel("Initial population"), row, 0)
        _parametersTab.addWidget(self._population, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 0, max: 10^7"), row, 2)
        row = row + 1
        _parametersTab.addWidget(qtWidget.QLabel("Enviroment capacity"), row, 0)
        _parametersTab.addWidget(self._capacity, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 0, max: 10^7"), row, 2)
        row = row + 1
        _parametersTab.addWidget(qtWidget.QLabel("Simulation steps"), row, 0)
        _parametersTab.addWidget(self._steps, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 0, max: 10^5"), row, 2)
        row = row + 1
        _parametersTab.addWidget(qtWidget.QLabel("Tau step"), row, 0)
        _parametersTab.addWidget(self._tau, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 0, max: 1, step: 0.001"), row, 2)
        row = row + 1
        _parametersTab.addWidget(qtWidget.QLabel("Cycle time"), row, 0)
        _parametersTab.addWidget(self._skip, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 0.1, max: 100.0, step: 0.1"), row, 2)
        row = row + 1
        _parametersTab.addWidget(qtWidget.QLabel("Mutation effect (list)"), row, 0)
        _parametersTab.addWidget(self._mut_effect, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 0.00001, max: 0.99999"), row, 2)
        row = row + 1
        _parametersTab.addWidget(qtWidget.QLabel("Mutation probability (list)"), row, 0)
        _parametersTab.addWidget(self._mut_prob, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 0.00001, max: 0.99999"), row, 2)  
        row = row + 1
        _parametersTab.addWidget(qtWidget.QLabel("Mutation intesity"), row, 0)
        _parametersTab.addWidget(self._lambda, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 1, max: 100"), row, 2) 
        row = row + 1
        _parametersTab.addWidget(qtWidget.QLabel("Threads used in simulation"), row, 0)
        _parametersTab.addWidget(self._threads, row, 1)
        _parametersTab.addWidget(qtWidget.QLabel("min: 1, max: 1024"), row, 2) 
        row = row + 1
        _parametersTab.addWidget(_load_params, row, 0, 1, 3)
        row = row + 1
        _parametersTab.addWidget(_resume_button, row, 0, 1, 3)
        row = row + 1
        _parametersTab.addWidget(_save_params, row, 0, 1, 3)
        row = row + 1
        _parametersTab.addWidget(_calculate_crit, row, 0, 1, 3)
        
        parametersTab.setLayout(_parametersTab)
        return parametersTab
    
    def critPop(self):        
        try:
            mut_prob = self._mut_prob.text().split(',')
            mut_prob = [float(x.strip('[]')) for x in mut_prob]
            mut_effect = self._mut_effect.text().split(',')
            mut_effect = [float(x.strip('[]')) for x in mut_effect]
        except:
            self.showDialog("Type correct parameters","Alert")
            return        
        
        self.status.setText("Critical Population: " + str(round((mut_prob[1]/mut_prob[0])*(mut_effect[1]/mut_effect[0]**2),0)))
    
    def selectPath(self):
        dir_path = qtWidget.QFileDialog.getExistingDirectory(self,"Choose Directory","Z:\\")
        self._file_path.setText(dir_path)

    def saveParams(self):
        try:
            pop = int(self._population.text())
            cap = int(self._capacity.text())
            steps = int(self._steps.text())
            tau = float(self._tau.text())
            skip = float(self._skip.text())
            mut_prob = self._mut_prob.text().split(',')
            mut_prob = [float(x) for x in mut_prob]
            mut_effect = self._mut_effect.text().split(',')
            mut_effect = [float(x) for x in mut_effect]
            iLambda = int(self._lambda.text())
            threads = int(self._threads.text())
        except:
            self.showDialog("Type correct parameters","Alert")
            return
        
        try:
            if self._file_name.text() == "":
                raise Exception()
            if self._file_path.text() == "":
                raise Exception()
        except:
            self.showDialog("Enter save localization and name", "Alert")
            return
            
        dfp = pd.DataFrame({
                'pop': pop,
                'cap': cap,
                'steps': steps,
                'tau': tau,
                'skip': skip,
                'mut_prob': [mut_prob],
                'mut_effect': [mut_effect],
                'threads': threads,
                'lambda': iLambda
            }, index=[0])
        
        filepath = Path(self._file_path.text() + '\\params'  + ".csv")  
        filepath.parent.mkdir(parents=True, exist_ok=True)  
        dfp.to_csv(filepath)  

    def simStart(self):
        try:
            pop = int(self._population.text())
            cap = int(self._capacity.text())
            steps = int(self._steps.text())
            tau = float(self._tau.text())
            skip = float(self._skip.text())
            mut_prob = self._mut_prob.text().split(',')
            mut_prob = [float(x) for x in mut_prob]
            mut_effect = self._mut_effect.text().split(',')
            mut_effect = [float(x) for x in mut_effect]
            iLambda = int(self._lambda.text())
            threads = int(self._threads.text())
        except:
            self.showDialog("Type correct parameters","Alert")
            return
        
        try:
            if self._file_name == "" and self._sx.isChecked():
                raise Exception()
            if self._file_path == "" and self._sx.isChecked():
                raise Exception()
        except:
            self.showDialog("Enter save localization and name", "Alert")
            return
        
        plots = 1*self._mw.isChecked() + 2*self._fw.isChecked() + 16*self._sx.isChecked()
        
        if self._binned.isChecked():
            self._status.setText("binned version not available")
        else:        
            iMuts = np.zeros(pop, dtype=np.int64).tolist()
            iProp = np.ones(pop).tolist()
            
            self.status.setText("Started")
            self.status.setStyleSheet("background-color: green")
            time.sleep(1)
    
            self.th_s.append(Thread(target=pnEML, args=(np.array([
                                                        copy.deepcopy(iProp), 
                                                        copy.deepcopy(iMuts), 
                                                        copy.deepcopy(iMuts)]).T.tolist(), 
                                                        copy.deepcopy([pop, cap, steps, tau, skip, mut_prob, mut_effect, iLambda, threads]), 
                                                        self._file_name.text(), 
                                                        self._file_desc.text(), 
                                                        self._file_path.text(), plots, 0, self.q, self.ID, 0)))    

            self.s_ID.append(str(self.ID))
            self.ID = self.ID + 1
            self.th_s[self.idx_s].start()
            self.idx_s = self.idx_s + 1
       
    def resume(self):
        self.showPromptParams()
        fname = qtWidget.QFileDialog.getOpenFileName(None, 'Open file', "Z://","CSV files (*.csv);; Text files (*.txt)")[0] 
        if fname == "":
            self.showDialog("No file selected!", "Alert")
            return
        self.loadPaths(fname)
        
        try:
            pop = int(self._population.text())
            cap = int(self._population.text())
            steps = int(self._population.text())
            tau = float(self._population.text())
            skip = float(self._population.text())
            mut_prob = self._mut_prob.text().split(',')
            mut_prob = [float(x.strip('[]')) for x in mut_prob]
            mut_effect = self._mut_effect.text().split(',')
            mut_effect = [float(x.strip('[]')) for x in mut_effect]
            iLambda = int(self._lambda.text())
            threads = int(self._threads.text())
        except:
            self.showDialog("Type correct parameters","Alert")
            return        
           
        df = pd.read_csv(fname)
        
        plots = 1*self._mw.isChecked() + \
                2*self._fw.isChecked() + \
                16*self._sx.isChecked()
        
        iProp = df['Fitness'].tolist()
        ipMutations = df['Positive mutations'].tolist()
        inMutations = df['Negative mutations'].tolist()
        
        del df
                
        self.status.setText("Started")
        self.status.setStyleSheet("background-color: green")
        time.sleep(1)
        
        self.th_r.append(Thread(target=pnEML, args=(([copy.deepcopy(iProp), 
                                                    copy.deepcopy(ipMutations), 
                                                    copy.deepcopy(inMutations)]).T.tolist(), 
                                                   copy.deepcopy([pop, cap, steps, tau, skip, mut_prob, mut_effect, iLambda, threads]), 
                                                   self._file_name.text(), 
                                                   self._file_desc.text(), 
                                                   self._file_path.text(), plots, self._last_cycle+1, self.q, self.ID, 0)))
        self.r_ID.append(str(self.ID))
        self.ID = self.ID + 1
        self.th_r[self.idx_r].start()
        self.idx_r = self.idx_r + 1     
        
    def showDialog(self, text, title):
        msgBox = qtWidget.QMessageBox()
        msgBox.setIcon(qtWidget.QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(qtWidget.QMessageBox.Ok)
         
        returnValue = msgBox.exec()
        if returnValue == qtWidget.QMessageBox.Ok:
           print('OK clicked')
           
    def loadParams(self):
        fname = qtWidget.QFileDialog.getOpenFileName(self, 'Open file', "Z://","CSV files (*.csv)")        
        df = pd.read_csv(fname[0])
        
        pop = df['pop'][0]
        cap = df['cap'][0]
        steps = df['steps'][0]
        tau = df['tau'][0]
        skip = df['skip'][0]
        iLambda = df['lambda'][0]
        xx = df['mut_prob'][0]
        xx = xx.split(',')
        xx = [float(x.strip('[]')) for x in xx]
        mut_prob = ""
        for i in xx:
            mut_prob = mut_prob + str(i) + ','
        mut_prob = mut_prob.rstrip(',')
        xx = df['mut_effect'][0]       
        xx = xx.split(',')
        xx = [float(x.strip('[]')) for x in xx]
        mut_effect = ""
        for i in xx:
            mut_effect = mut_effect + str(i) + ','
        mut_effect = mut_effect.rstrip(',')
        threads = df['threads'][0]
        
        self.params = [pop, cap, steps, tau, skip, mut_prob, mut_effect]
        self._population.setText(str(pop))
        self._capacity.setText(str(cap))
        self._steps.setText(str(steps))
        self._tau.setText(str(tau))
        self._skip.setText(str(skip))
        self._mut_prob.setText(str(mut_prob))
        self._mut_effect.setText(str(mut_effect))        
        self._lambda.setText(str(iLambda))
        self._threads.setText(str(threads))
      
    def showPromptParams(self):
        msgBox = qtWidget.QMessageBox()
        msgBox.setIcon(qtWidget.QMessageBox.Information)
        msgBox.setText("Have you change simulation parameters as continiuing simulation?")
        msgBox.setWindowTitle("Parameters")
        msgBox.setStandardButtons(qtWidget.QMessageBox.Yes | qtWidget.QMessageBox.No)       
        returnValue = msgBox.exec()
        if returnValue == qtWidget.QMessageBox.No:
           self.loadParams()    
      
    def loadPaths(self, fname):        
        # self.showDialog("Select file same as resume simulation", "Info")
        xname = fname.split('/')
        
        ##TODO interpret only last number!!!
        
        path = ""
        name = ""
        self._last_cycle = 0
        for i in xname:
            if xname.index(i) == len(xname)-1:
                t = i.split('_')
                t = t[len(t)-1]
                self._last_cycle = int(''.join(x for x in t if x.isdigit()))
                if i.endswith('.csv'):
                    name = i.rstrip('_' + str(self._last_cycle) + '.csv')
                elif i.endswith('.txt'):
                    name = i.rstrip('_' + str(self._last_cycle) + '.txt')
            else:
                path = path + i + '\\'
        
        if name.endswith("_binned"):
            name = name.rstrip("_binned")
        else:
            name = name.rstrip("_single")
        self._file_name.setText(name)
        self._file_path.setText(path)  
        self._file_desc.setText(str(self._last_cycle) + " - last cycle, starting with +1")                   

def run():
        app = qtWidget.QApplication(sys.argv)
        win = mainFormat()
        win.show()
        ret = app.exec_()
        sys.exit(ret)

if __name__ == "__main__":
    run()