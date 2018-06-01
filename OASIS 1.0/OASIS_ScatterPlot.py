import sys,os
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 
def main(): 
    app = QApplication(sys.argv) 
    w = Scatter() 
    #w.show() 
    sys.exit(app.exec_()) 
 
class Scatter(QMainWindow): 
    def __init__(self, feature_table): 
        QWidget.__init__(self) 

        self.x_flag = 5
        self.y_flag = 4

        self.object_selected = 0 

        # get_data
        self.get_scatter_data()
        self.feature_table = feature_table
        
         
        # Menu
        menu = self.menuBar()
        x_bar = menu.addMenu("&X Axis")
        y_bar = menu.addMenu("&Y Axis")
        
        self.x_bar_action = []
        self.y_bar_action = []
        
        self.x_bar_action.append(QAction('&Centroid x',self))
        self.x_bar_action.append(QAction('&Centroid y',self))
        self.x_bar_action.append(QAction('&Area',self))
        self.x_bar_action.append(QAction('&Aspect Ratio',self))
        self.x_bar_action.append(QAction('&# of Nucleus',self))
        self.x_bar_action.append(QAction('&Protein_AVG',self))
        self.x_bar_action.append(QAction('&Protein_std',self))
        self.x_bar_action.append(QAction('&Protein_MAX',self))
        self.x_bar_action.append(QAction('&Protein_MIN',self))

        self.x_bar_action[0].triggered.connect(self.x_bar_0)
        self.x_bar_action[1].triggered.connect(self.x_bar_1)
        self.x_bar_action[2].triggered.connect(self.x_bar_2)
        self.x_bar_action[3].triggered.connect(self.x_bar_3)
        self.x_bar_action[4].triggered.connect(self.x_bar_4)
        self.x_bar_action[5].triggered.connect(self.x_bar_5)
        self.x_bar_action[6].triggered.connect(self.x_bar_6)
        self.x_bar_action[7].triggered.connect(self.x_bar_7)
        self.x_bar_action[8].triggered.connect(self.x_bar_8)
        
        self.y_bar_action.append(QAction('&Centroid x',self))
        self.y_bar_action.append(QAction('&Centroid y',self))
        self.y_bar_action.append(QAction('&Area',self))
        self.y_bar_action.append(QAction('&Aspect Ratio',self))
        self.y_bar_action.append(QAction('&# of Nucleus',self))
        self.y_bar_action.append(QAction('&Protein_AVG',self))
        self.y_bar_action.append(QAction('&Protein_std',self))
        self.y_bar_action.append(QAction('&Protein_MAX',self))
        self.y_bar_action.append(QAction('&Protein_MIN',self))
        
        self.y_bar_action[0].triggered.connect(self.y_bar_0)
        self.y_bar_action[1].triggered.connect(self.y_bar_1)
        self.y_bar_action[2].triggered.connect(self.y_bar_2)
        self.y_bar_action[3].triggered.connect(self.y_bar_3)
        self.y_bar_action[4].triggered.connect(self.y_bar_4)
        self.y_bar_action[5].triggered.connect(self.y_bar_5)
        self.y_bar_action[6].triggered.connect(self.y_bar_6)
        self.y_bar_action[7].triggered.connect(self.y_bar_7)
        self.y_bar_action[8].triggered.connect(self.y_bar_8)

        for i in range(0,9):
            self.x_bar_action[i].setCheckable(True)
            self.y_bar_action[i].setCheckable(True)
            x_bar.addAction(self.x_bar_action[i])
            y_bar.addAction(self.y_bar_action[i])
        
        #Scatter Plot
        self.main_frame = QWidget()
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.create_scatter_plot(feature_table)     
        
        # layout
        self.setFixedSize(640,500)
        self.setCentralWidget(self.main_frame) 
        self.setWindowTitle("OASIS 1.0 Scatter Plot")

    def get_scatter_data(self):
        stdouterr = os.popen4("dir c:\\")[1].read()
        lines = stdouterr.splitlines()
        lines = lines[5:]
        lines = lines[:-2]
        #self.tabledata = [re.split(r"\s+", line, 4)
        #             for line in lines]
        self.tabledata = [['1','2','3','4','5','6','7','8','9','0'],
                          ['2','1','2','4','5','6','7','8','9','0'],
                          ['3','1.5','2.5','4','5','6','7','8','9','0'],
                          ['4','2.5','1','4','5','6','7','8','9','0']]
    def create_scatter_plot(self,feature_table):
        # x_axis = [1,2,4,3,2.5,2.1]
        # y_axis = [2,1,3,4,1.2,1.5]
        x_axis = feature_table[:,4]
        y_axis = feature_table[:,5]
        plt.plot(x_axis,y_axis,'ro')
        # x0 = [2]
        # y0 = [1]
        # plt.plot(x0,y0,'go')
        plt.xlabel('X_AXIS')
        plt.ylabel('Y_AXIS')
        plt.grid(True)

    def x_bar_0(self):
        self.x_flag = 0
        self.x_bar_action[0].setChecked(True)
        self.x_bar_action[1].setChecked(False)
        self.x_bar_action[2].setChecked(False)
        self.x_bar_action[3].setChecked(False)
        self.x_bar_action[4].setChecked(False)
        self.x_bar_action[5].setChecked(False)
        self.x_bar_action[6].setChecked(False)
        self.x_bar_action[7].setChecked(False)
        self.x_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def x_bar_1(self):
        self.x_flag = 1
        self.x_bar_action[0].setChecked(False)
        self.x_bar_action[1].setChecked(True)
        self.x_bar_action[2].setChecked(False)
        self.x_bar_action[3].setChecked(False)
        self.x_bar_action[4].setChecked(False)
        self.x_bar_action[5].setChecked(False)
        self.x_bar_action[6].setChecked(False)
        self.x_bar_action[7].setChecked(False)
        self.x_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def x_bar_2(self):
        self.x_flag = 2
        self.x_bar_action[0].setChecked(False)
        self.x_bar_action[1].setChecked(False)
        self.x_bar_action[2].setChecked(True)
        self.x_bar_action[3].setChecked(False)
        self.x_bar_action[4].setChecked(False)
        self.x_bar_action[5].setChecked(False)
        self.x_bar_action[6].setChecked(False)
        self.x_bar_action[7].setChecked(False)
        self.x_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def x_bar_3(self):
        self.x_flag = 3
        self.x_bar_action[0].setChecked(False)
        self.x_bar_action[1].setChecked(False)
        self.x_bar_action[2].setChecked(False)
        self.x_bar_action[3].setChecked(True)
        self.x_bar_action[4].setChecked(False)
        self.x_bar_action[5].setChecked(False)
        self.x_bar_action[6].setChecked(False)
        self.x_bar_action[7].setChecked(False)
        self.x_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def x_bar_4(self):
        self.x_flag = 4
        self.x_bar_action[0].setChecked(False)
        self.x_bar_action[1].setChecked(False)
        self.x_bar_action[2].setChecked(False)
        self.x_bar_action[3].setChecked(False)
        self.x_bar_action[4].setChecked(True)
        self.x_bar_action[5].setChecked(False)
        self.x_bar_action[6].setChecked(False)
        self.x_bar_action[7].setChecked(False)
        self.x_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def x_bar_5(self):
        self.x_flag = 5
        self.x_bar_action[0].setChecked(False)
        self.x_bar_action[1].setChecked(False)
        self.x_bar_action[2].setChecked(False)
        self.x_bar_action[3].setChecked(False)
        self.x_bar_action[4].setChecked(False)
        self.x_bar_action[5].setChecked(True)
        self.x_bar_action[6].setChecked(False)
        self.x_bar_action[7].setChecked(False)
        self.x_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def x_bar_6(self):
        self.x_flag = 6
        self.x_bar_action[0].setChecked(False)
        self.x_bar_action[1].setChecked(False)
        self.x_bar_action[2].setChecked(False)
        self.x_bar_action[3].setChecked(False)
        self.x_bar_action[4].setChecked(False)
        self.x_bar_action[5].setChecked(False)
        self.x_bar_action[6].setChecked(True)
        self.x_bar_action[7].setChecked(False)
        self.x_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def x_bar_7(self):
        self.x_flag = 7
        self.x_bar_action[0].setChecked(False)
        self.x_bar_action[1].setChecked(False)
        self.x_bar_action[2].setChecked(False)
        self.x_bar_action[3].setChecked(False)
        self.x_bar_action[4].setChecked(False)
        self.x_bar_action[5].setChecked(False)
        self.x_bar_action[6].setChecked(False)
        self.x_bar_action[7].setChecked(True)
        self.x_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def x_bar_8(self):
        self.x_flag = 8
        self.x_bar_action[0].setChecked(False)
        self.x_bar_action[1].setChecked(False)
        self.x_bar_action[2].setChecked(False)
        self.x_bar_action[3].setChecked(False)
        self.x_bar_action[4].setChecked(False)
        self.x_bar_action[5].setChecked(False)
        self.x_bar_action[6].setChecked(False)
        self.x_bar_action[7].setChecked(False)
        self.x_bar_action[8].setChecked(True)
        self.update_scatter_plot()


    def y_bar_0(self):
        self.y_flag = 0
        self.y_bar_action[0].setChecked(True)
        self.y_bar_action[1].setChecked(False)
        self.y_bar_action[2].setChecked(False)
        self.y_bar_action[3].setChecked(False)
        self.y_bar_action[4].setChecked(False)
        self.y_bar_action[5].setChecked(False)
        self.y_bar_action[6].setChecked(False)
        self.y_bar_action[7].setChecked(False)
        self.y_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def y_bar_1(self):
        self.y_flag = 1
        self.y_bar_action[0].setChecked(False)
        self.y_bar_action[1].setChecked(True)
        self.y_bar_action[2].setChecked(False)
        self.y_bar_action[3].setChecked(False)
        self.y_bar_action[4].setChecked(False)
        self.y_bar_action[5].setChecked(False)
        self.y_bar_action[6].setChecked(False)
        self.y_bar_action[7].setChecked(False)
        self.y_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def y_bar_2(self):
        self.y_flag = 2
        self.y_bar_action[0].setChecked(False)
        self.y_bar_action[1].setChecked(False)
        self.y_bar_action[2].setChecked(True)
        self.y_bar_action[3].setChecked(False)
        self.y_bar_action[4].setChecked(False)
        self.y_bar_action[5].setChecked(False)
        self.y_bar_action[6].setChecked(False)
        self.y_bar_action[7].setChecked(False)
        self.y_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def y_bar_3(self):
        self.y_flag = 3
        self.y_bar_action[0].setChecked(False)
        self.y_bar_action[1].setChecked(False)
        self.y_bar_action[2].setChecked(False)
        self.y_bar_action[3].setChecked(True)
        self.y_bar_action[4].setChecked(False)
        self.y_bar_action[5].setChecked(False)
        self.y_bar_action[6].setChecked(False)
        self.y_bar_action[7].setChecked(False)
        self.y_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def y_bar_4(self):
        self.y_flag = 4
        self.y_bar_action[0].setChecked(False)
        self.y_bar_action[1].setChecked(False)
        self.y_bar_action[2].setChecked(False)
        self.y_bar_action[3].setChecked(False)
        self.y_bar_action[4].setChecked(True)
        self.y_bar_action[5].setChecked(False)
        self.y_bar_action[6].setChecked(False)
        self.y_bar_action[7].setChecked(False)
        self.y_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def y_bar_5(self):
        self.y_flag = 5
        self.y_bar_action[0].setChecked(False)
        self.y_bar_action[1].setChecked(False)
        self.y_bar_action[2].setChecked(False)
        self.y_bar_action[3].setChecked(False)
        self.y_bar_action[4].setChecked(False)
        self.y_bar_action[5].setChecked(True)
        self.y_bar_action[6].setChecked(False)
        self.y_bar_action[7].setChecked(False)
        self.y_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def y_bar_6(self):
        self.y_flag = 6
        self.y_bar_action[0].setChecked(False)
        self.y_bar_action[1].setChecked(False)
        self.y_bar_action[2].setChecked(False)
        self.y_bar_action[3].setChecked(False)
        self.y_bar_action[4].setChecked(False)
        self.y_bar_action[5].setChecked(False)
        self.y_bar_action[6].setChecked(True)
        self.y_bar_action[7].setChecked(False)
        self.y_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def y_bar_7(self):
        self.y_flag = 7
        self.y_bar_action[0].setChecked(False)
        self.y_bar_action[1].setChecked(False)
        self.y_bar_action[2].setChecked(False)
        self.y_bar_action[3].setChecked(False)
        self.y_bar_action[4].setChecked(False)
        self.y_bar_action[5].setChecked(False)
        self.y_bar_action[6].setChecked(False)
        self.y_bar_action[7].setChecked(True)
        self.y_bar_action[8].setChecked(False)
        self.update_scatter_plot()

    def y_bar_8(self):
        self.y_flag = 8
        self.y_bar_action[0].setChecked(False)
        self.y_bar_action[1].setChecked(False)
        self.y_bar_action[2].setChecked(False)
        self.y_bar_action[3].setChecked(False)
        self.y_bar_action[4].setChecked(False)
        self.y_bar_action[5].setChecked(False)
        self.y_bar_action[6].setChecked(False)
        self.y_bar_action[7].setChecked(False)
        self.y_bar_action[8].setChecked(True)
        self.update_scatter_plot()

    def update_scatter_plot(self, cell_selection_ID = None):
        #Scatter Plot
        self.main_frame.deleteLater()
        self.main_frame = QWidget()
        plt.close()
        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        axis_names = ['Centroid X', 'Centroid Y', 'Area', 'Aspect Ratio','# of Nucleus', 'Protein AVG', 'Protein Std', 'Protein Max', 'Protein Min']
        x_axis = self.feature_table[:,self.x_flag+1]
        y_axis = self.feature_table[:,self.y_flag+1]
        plt.plot(x_axis,y_axis,'ro')
        plt.xlabel('X_AXIS: '+axis_names[self.x_flag] + "  Unit: AU")
        plt.ylabel('Y_AXIS: '+axis_names[self.y_flag] + "  Unit: AU")

        if cell_selection_ID != None:
            self.object_selected = cell_selection_ID
            x_selected = self.feature_table[self.object_selected-1][self.x_flag+1]
            y_selected = self.feature_table[self.object_selected-1][self.y_flag+1]
            plt.plot(x_selected, y_selected, 'go')
        plt.grid(True)        
        # layout
        self.setCentralWidget(self.main_frame) 


 


if __name__ == "__main__": 
    main()