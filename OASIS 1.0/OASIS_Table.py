import re
import operator
import os
import sys 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

import numpy as np
 
def main(): 
    app = QApplication(sys.argv) 
    w = Table() 
    #w.show() 
    sys.exit(app.exec_()) 
 
class Table(QMainWindow): 
    def __init__(self, feature_table): 
        QWidget.__init__(self) 

        self.object_selected = 0
        self.feature_table = feature_table

        export_data_action = QAction('&Export Table',self)
        export_data_action.setShortcut('Ctrl+E')
        export_data_action.triggered.connect(self.export_data)
        menubar = self.menuBar()
        OPTMenu = menubar.addMenu('&Operations')
        OPTMenu.addAction(export_data_action)

        # create table
        self.get_table_data(feature_table)
        self.table = self.createTable() 
        self.table.selectRow(self.object_selected)
        # layout
        # layout = QVBoxLayout()
        # layout.addWidget(self.table) 
        # self.setLayout(layout) 
        self.setCentralWidget(self.table)
        self.setWindowTitle("OASIS 1.0 Feature Table")


    def export_data(self):
        path = str(QFileDialog.getExistingDirectory(self,"Save feature table ..."))
        path = path + "\\"
        filename = path + "feature_table.txt"
        np.savetxt(filename, self.feature_table.tolist(), fmt = '%d \t %d \t %d \t %d \t %1.2f \t %d \t %1.2f \t %1.2f \t %1.2f \t %1.2f')
    def get_table_data(self, feature_table = None):
        stdouterr = os.popen4("dir c:\\")[1].read()
        lines = stdouterr.splitlines()
        lines = lines[5:]
        lines = lines[:-2]
        #self.tabledata = [re.split(r"\s+", line, 4)
        #             for line in lines]
        # self.tabledata = [['1','2','3','4','5','6','7','8','9','0'],
                          # ['2','4','5','7','7','23','12','24','10','0'],
                          # ['3','12','31','4','5','6','7','8','9','0'],
                          # ['4','21','32','2','5','6','7','8','9','0']]
        self.tabledata = feature_table.tolist()
        print type(self.tabledata)
    def createTable(self):
        # create the view
        # tv = QTableView()
        tv = QTableView()

        # set the table model
        header = ['ID', 'Centroid_X', 'Centroid_Y', 'Area', 'Aspect Ratio','# of Nucleus', 'Protein_AVG','Protein_std','Protein_MAX','Protein_MIN']
        tm = MyTableModel(self.tabledata, header, self) 
        tv.setModel(tm)

        # set the minimum size
        tv.setMinimumSize(860, 300)

        # hide grid
        tv.setShowGrid(False)

        # set the font
        font = QFont("Courier New", 8)
        tv.setFont(font)

        # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        tv.resizeColumnsToContents()

        # set row height
        nrows = len(self.tabledata)
        for row in xrange(nrows):
            tv.setRowHeight(row, 18)

        # enable sorting
        tv.setSortingEnabled(True)
        
        tv.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # mouse click setting
        tv.clicked.connect(self.cell_was_clicked)

        return tv

    def cell_was_clicked(self):
        row = self.table.selectionModel().currentIndex().row()
        column = 0
        model = self.table.model()
        index = model.index(row, column)
        cell_ID = int(model.data(index, Qt.DisplayRole).toString())
        self.emit(SIGNAL("OASIS_Table_Selection"), cell_ID)

    def object_selection_slot(self, cell_selection_ID = None):
        nrows = len(self.tabledata)
        for row in range(0,nrows):
            column = 0
            model = self.table.model()
            index = model.index(row, column)
            cell_ID = int(model.data(index, Qt.DisplayRole).toString())
            if cell_ID == cell_selection_ID:
                self.object_selected = cell_selection_ID
                self.table.selectRow(row)
                return

    def update_table(self, feature_table):
        print "To be Finished ... "                                                                                                                                                                                                 
 
class MyTableModel(QAbstractTableModel): 
    def __init__(self, datain, headerdata, parent=None, *args): 
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args) 
        self.arraydata = datain
        self.headerdata = headerdata
 
    def rowCount(self, parent): 
        return len(self.arraydata) 
 
    def columnCount(self, parent): 
        return len(self.arraydata[0]) 
 
    def data(self, index, role): 
        if not index.isValid(): 
            return QVariant() 
        elif role != Qt.DisplayRole: 
            return QVariant() 
        return QVariant(self.arraydata[index.row()][index.column()]) 

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))        
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))

if __name__ == "__main__": 
    main()