################ For Segmentation #####################
from __future__ import division
from math import sqrt
from matplotlib import pyplot as plt
from skimage.feature import blob_log
from skimage.filters import threshold_otsu
from skimage import measure
from skimage import morphology 
from scipy.ndimage.morphology import binary_fill_holes

#######################################################
import sys
import copy
import SimpleITK as sitk
import numpy as np
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from OASIS_Display import *
from OASIS_Table import *
from OASIS_ScatterPlot import *
from OASIS_Adjust import *


class OASIS(QMainWindow):
	def __init__(self):
		super(OASIS,self).__init__()
		#self.OASIS_Display1 = OASIS_Display()
		
		################################### Menu Setup ############################################################
		self.statusBar()
		
		# File Menu
		exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)

		loadDatasetAction = QAction('&Loading...',self)
		loadDatasetAction.setShortcut('Ctrl+L')
		loadDatasetAction.triggered.connect(self.loadData)

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(loadDatasetAction)
		fileMenu.addAction(exitAction)
		
		# Window Menu
		winMenu = menubar.addMenu('&Windows')
		
		tableAction = QAction('&Feature Table',self)
		tableAction.triggered.connect(self.table_create)
		scatterAction = QAction('&Scatter Plot',self)
		scatterAction.triggered.connect(self.scatter_create)
		
		winMenu.addAction(tableAction)
		winMenu.addAction(scatterAction)

		
		# Image Menu
		imgMenu = menubar.addMenu('&Images')
		
		adjustAction = QAction('&Adjust...',self)
		adjustAction.setShortcut('Ctrl+C')
		adjustAction.triggered.connect(self.adjust_create)
		
		imgMenu.addAction(adjustAction)
		
		# Analytics Menu
		analyticsMenu = menubar.addMenu('&Analytics')
		
		segmentAction = QAction('&Segment',self)
		segmentAction.triggered.connect(self.cell_segmentation)
		mergeAction = QAction('&Merge',self)
		splitAction = QAction('&Split',self)
		eraseAction = QAction('&Erase',self)
		brushAction = QAction('&Brush',self)
		featAction = QAction('&Calculate Feature',self)
		featAction.triggered.connect(self.cell_feature_calc)
		
		analyticsMenu.addAction(segmentAction)
		editMenu = analyticsMenu.addMenu('&Edit...')
		editMenu.addAction(mergeAction)
		editMenu.addAction(splitAction)
		editMenu.addAction(eraseAction)
		editMenu.addAction(brushAction)
		analyticsMenu.addAction(featAction)
		
		
		# Help Menu
		helpMenu = menubar.addMenu('&Help')
		
		aboutAction = QAction('&About',self)
		aboutAction.triggered.connect(self.about_func)
		
		helpMenu.addAction(aboutAction)
		
		
		
		self.setWindowTitle('OASIS 1.0')
		self.show()
		
	def loadData(self):
		self.path = str(QFileDialog.getExistingDirectory(self,"Select Directory"))
		self.path = self.path + "\\"
		#self.OASIS_Display1.path = path
		t_span = int(sys.argv[1])
		self.OASIS_Display1 = OASIS_Display(self.path, t_span)
		self.setCentralWidget(self.OASIS_Display1)
		self.OASIS_Display1.loadImages()
		self.OASIS_Display1.refreshImages()

	
	def build_links(self):
		print "..."
	
	
	
	################ Menu Function ###############################
	def about_func(self):
		QMessageBox.information(self,"About","Version: OASIS 0.1 \n Author: Hengyang Lu \n Email: hlu9@uh.edu \n Copy Right Reserved.")
	
	def table_create(self):
		# self.feature_table = Table()
		# self.feature_table.show()
		print "Click Calculate Features again ..."
		
	def scatter_create(self):
		# self.scatter_plot = Scatter(self.feature_table_value)
		# self.scatter_plot.show()
		print "Click Calculate Features again ..."
	
	def adjust_create(self):
		self.adjust = Adjust()
		self.adjust.show()
	
	######################################## Control the Display of Label Image ################################
	def show_ID_Dapi(self):
			print "To be finished ..."
	
	def show_crosspair_Dapi(self):
		print "To be finished ..."
		
	def highlight_nucleus(self):
		print "To be finished ..."
		
	def show_ID_Cell(self):
		print "To be finished ..."
		
	def highlight_Cell(self):
		print "To be finished ..."
	
	def image_linear_hist(self,image, lower, upper):
		for pixel in np.nditer(image, op_flags=['readwrite']):
			if pixel <= lower:
				pixel[...] = 0
			if pixel >= upper:
				pixel[...] = 255
			if pixel > lower and pixel < upper:
				pixel[...]  = round((pixel - lower)/(upper - lower)*255)
		return image
		
	######################################### Image Segmentation and Feature Calculation########################
	def nuclei_segmentation(self):
		t = self.OASIS_Display1.t
		# if str(t) in self.OASIS_Display1.CH2_label_dict.keys():
			# self.OASIS_Display1.CH2_label = self.OASIS_Display1.CH2_label_dict[str(t)]
		# else:
		image1 =sitk.ReadImage(self.OASIS_Display1.getImagePath(2))
		image1 = sitk.GetArrayFromImage(image1)
		image2 = self.image_linear_hist(image1, 2, 20)
		blobs_log = blob_log(image2, min_sigma=6, max_sigma=8, num_sigma=11, threshold=0.04)
		# Compute radii in the 3rd column.
		blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
		self.OASIS_Display1.CH2_label = blobs_log
		self.OASIS_Display1.CH2_label_dict[str(t)] = blobs_log
		
	def cell_segmentation(self):
		self.nuclei_segmentation()
		
		################## Membrane Cell Segmentation #####
		t = self.OASIS_Display1.t
		image1 =sitk.ReadImage(self.OASIS_Display1.getImagePath(1))
		image1 = sitk.GetArrayFromImage(image1)
		image1 = self.image_linear_hist(image1, 0, 15)

		thresh = threshold_otsu(image1)
		image1_bw = image1 > thresh
			
			
		image2 =sitk.ReadImage(self.OASIS_Display1.getImagePath(2))
		image2 = sitk.GetArrayFromImage(image2)
		image2 = self.image_linear_hist(image2, 0, 20)

		thresh2 = threshold_otsu(image2)
		image2_bw = image2 > thresh

		# fill the holes of nucleus	
		image_bw = np.logical_or(image1_bw,image2_bw)

		# remove small objects
		image_bw = morphology.remove_small_objects(image_bw,150)

		# dilation
		for i in range(1,3):
			image_bw = morphology.binary_dilation(image_bw)

		# fill the holes
		image_bw = binary_fill_holes(image_bw)

		# binary opening to smooth the edge
		image_bw = morphology.binary_opening(image_bw)
		self.OASIS_Display1.CH1_label = image_bw
		#self.OASIS_Display1.CH1_label_dict[str(t)] = image_bw

		paint = QPainter()
		paint.begin(self.OASIS_Display1.CH1_pixmap)
		pen = QPen(Qt.magenta)
		paint.setPen(pen)
		try:
			for i in range(1,1023):
				for j in range(1,1023):
					v = self.OASIS_Display1.CH1_label[i][j]
					if v >0:
						v1 = self.OASIS_Display1.CH1_label[i][j+1]
						v2 = self.OASIS_Display1.CH1_label[i+1][j]
						v3 = self.OASIS_Display1.CH1_label[i][j-1]
						v4 = self.OASIS_Display1.CH1_label[i-1][j]
						if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
							paint.drawPoint(j,i)
		except:
			print "No cell segmentation Pixmap yet!"
		paint.end()

		######################################################
		self.OASIS_Display1.refreshImages()
		
		
	def cell_feature_calc(self):
		t = self.OASIS_Display1.t
		
		# Label different cells in CH1_label
		CH1_label = self.OASIS_Display1.CH1_label
		CH2_label = self.OASIS_Display1.CH2_label
		CH3 = self.OASIS_Display1.CH3
		
		CCP_label = measure.label(CH1_label, background=0)
		self.OASIS_Display1.CH1_CCP_label = CCP_label
		self.OASIS_Display1.CH1_label_dict[str(t)] = CCP_label
		
		CCP_Max = CCP_label.max()
		feature_table = np.zeros((CCP_Max,10))
		# Calculate features for each cell
		for cell_ID in range(1,CCP_Max+1):
			[rows,cols] = np.where(CCP_label == cell_ID)
			feature_table[cell_ID-1][0] = cell_ID
			feature_table[cell_ID-1][3] = len(rows)              # calculate cell area
			feature_table[cell_ID-1][1] = int(np.average(rows))  # calculate cell centroid
			feature_table[cell_ID-1][2] = int(np.average(cols))
			aspect_ratio = (max(cols)-min(cols))/(max(rows)-min(rows)+0.000001) #calculate aspect ratio
			feature_table[cell_ID-1][4] = float("{0:.2f}".format(aspect_ratio))
			# crop the patch, protein calculation
			image_CH3 =sitk.ReadImage(self.OASIS_Display1.getImagePath(3))
			image_CH3 = sitk.GetArrayFromImage(image_CH3)
			protein_list_temp = []
			for row,col in zip(rows, cols):
				protein_list_temp.append(image_CH3[row][col])
			protein_Max = np.max(protein_list_temp)
			protein_Min = np.min(protein_list_temp)
			protein_AVG = np.mean(protein_list_temp)
			protein_std = np.std(protein_list_temp)
			
			feature_table[cell_ID-1][6] = float("{0:.2f}".format(protein_AVG))
			feature_table[cell_ID-1][7] = float("{0:.2f}".format(protein_std))
			feature_table[cell_ID-1][8] = float("{0:.2f}".format(protein_Max))
			feature_table[cell_ID-1][9] = float("{0:.2f}".format(protein_Min))
		# nucleus calculation, start from the neucleus perspective
		neucleus_number = len(CH2_label[:,0])
		for i in range(0,neucleus_number):
			temp = CCP_label[CH2_label[i][0]][CH2_label[i][1]]
			if temp != 0:
				feature_table[temp-1][5] = feature_table[temp-1][5] + 1
		
			
		# Load features into feature table and scatter plot, save them to dictionary
		# feature_table_str = np.array(["%.2f" % w for w in feature_table.reshape(feature_table.size)])
		# feature_table_str = feature_table_str.reshape(feature_table.shape)
		# for cell_ID in range(1,CCP_Max+1):
			# feature_table_str[cell_ID-1][0] = feature_table_str[cell_ID-1][0][0:-1-2]
			# feature_table_str[cell_ID-1][1] = feature_table_str[cell_ID-1][1][0:-1-2]
			# feature_table_str[cell_ID-1][2] = feature_table_str[cell_ID-1][2][0:-1-2]
			# feature_table_str[cell_ID-1][3] = feature_table_str[cell_ID-1][3][0:-1-2]
			# feature_table_str[cell_ID-1][5] = feature_table_str[cell_ID-1][5][0:-1-2]
		self.feature_table_value = feature_table
		self.OASIS_Display1.cell_feature_table = feature_table
		
		self.feature_table = Table(feature_table)
		self.feature_table.show()
		
		self.scatter_plot = Scatter(self.feature_table_value)
		self.scatter_plot.show()
		
		self.connect(self.OASIS_Display1,SIGNAL("OASIS_Display_Selection"),self.feature_table.object_selection_slot)
		self.connect(self.OASIS_Display1,SIGNAL("OASIS_Display_Selection"),self.scatter_plot.update_scatter_plot)
		
		self.connect(self.feature_table, SIGNAL("OASIS_Table_Selection"),self.OASIS_Display1.object_selection_slot)
		self.connect(self.feature_table, SIGNAL("OASIS_Table_Selection"),self.scatter_plot.update_scatter_plot)
		
	def nuclei_allocator(self):
		print "To be finished ..."
		
	def osteoclast_summary(self):
		print "To be finished ..."
		
def main():
	app = QApplication(sys.argv)
	
	cube = OASIS()
	
	sys.exit(app.exec_())
	
	
if __name__ == '__main__':
	main()