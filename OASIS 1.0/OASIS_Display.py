import sys
import SimpleITK as sitk
import numpy as np
from PyQt4.QtGui import *
from PyQt4.QtCore import *

#import G2_QImageConverter as QC



class OASIS_Display(QFrame):
	def __init__(self,path,t_span):
		super(OASIS_Display,self).__init__()

		#self.path = "C:\\LAB\\Osteoclast\\Data\\Set1\\"
		self.path = path
		self.t = 1
		self.t_span = t_span
		
		self.CH0 = []
		self.CH1 = []
		self.CH2 = []
		self.CH3 = []
		self.CH1_label = []
		self.CH1_CCP_label = []
		self.CH1_pixmap = QPixmap(1024,1024)
		self.CH2_label = []
		
		
		self.CH0_dict = {}
		self.CH1_dict = {}
		self.CH2_dict = {}
		self.CH3_dict = {}
		self.CH1_label_dict = {}
		self.CH2_label_dict = {}

		
		self.CH0_dict_v = {}
		self.CH1_dict_v = {}
		self.CH2_dict_v = {}
		self.CH3_dict_v = {}
		self.CH1_label_dict_v = {}
		self.CH2_label_dict_v = {}
	
		self.cell_feature_table = []
		self.cell_feature_table_dict={}
		#self.monoWell = []
		
		self.Display_Flags = {'CH0': True, 'CH1': True, 'CH2': True, 'CH3': False, 'CH1_label': True, 'CH2_label': True, 'crosspair': True}
		self.object_selected = 0
		
		self.Width = 1024
		self.Height = 1024
		
		self.imageLabel = QLabel()
		self.imageLabel.mousePressEvent = self.object_selection_func
		self.scrollArea = QScrollArea()
		self.slider = QSlider(Qt.Horizontal)
		self.spinBox = QSpinBox()
		self.playButton = QPushButton()
		self.pauseButton = QPushButton()
		self.stopButton = QPushButton()
		self.starButton = QPushButton()
		self.progress = QProgressBar()

		self.loadImages()
		self.setupUI()
		
	def setupUI(self):
	
	##################################### Image Panel #########################################################
		self.imageLabel.setBackgroundRole(QPalette.Base)
		self.imageLabel.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
		self.imageLabel.setMouseTracking(True)
		self.imageLabel.setScaledContents(True)
		
		
		pic = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		pic.fill(qRgb(0,0,0))
		painter = QPainter(pic)
		painter.setCompositionMode(QPainter.CompositionMode_Plus)
		
		channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		channelImage.fill(qRgb(255,255,255))
		channelImage.setAlphaChannel(self.CH0)
		painter.drawImage(0,0,channelImage)
		
		channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		channelImage.fill(qRgb(255,0,0))
		channelImage.setAlphaChannel(self.CH1)
		painter.drawImage(0,0,channelImage)
		
		channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		channelImage.fill(qRgb(0,255,0))
		channelImage.setAlphaChannel(self.CH2)
		painter.drawImage(0,0,channelImage)
		
		# pen = QPen(Qt.cyan)
		# painter.setPen(pen)
		# for i in range(1,1023):
			# for j in range(1,1023):
				# v = self.CH1_label[i][j]
				# if v >0:
					# v1 = self.CH1_label[i][j+1]
					# v2 = self.CH1_label[i+1][j]
					# v3 = self.CH1_label[i][j-1]
					# v4 = self.CH1_label[i-1][j]
					# if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
						# painter.drawPoint(j,i)
						
						
		# pen.setColor(Qt.magenta)
		# painter.setPen(pen)
		# for i in range(1,1023):
			# for j in range(1,1023):
				# v = self.CH2_label[i][j]
				# if v >0:
					# v1 = self.CH2_label[i][j+1]
					# v2 = self.CH2_label[i+1][j]
					# v3 = self.CH2_label[i][j-1]
					# v4 = self.CH2_label[i-1][j]
					# if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
						# painter.drawPoint(j,i)
		# del pen
		del painter
		
		self.imageLabel.setPixmap(QPixmap.fromImage(pic))
		
	
		self.scrollArea.setMouseTracking(True)
		self.scrollArea.setBackgroundRole(QPalette.Dark)
		self.scrollArea.setWidget(self.imageLabel)
		self.scrollArea.horizontalScrollBar().setRange(0,0)
		self.scrollArea.verticalScrollBar().setRange(0,0)
		self.scrollArea.horizontalScrollBar().setValue(0)
		self.scrollArea.verticalScrollBar().setValue(0)
		#self.scrollArea.setFixedSize(1026,1026)
		self.scrollArea.setFixedSize(800,800)
		
		#self.slider.setDisabled(True)
		self.slider.setRange(1,self.t_span)
		self.slider.setValue(1)
		self.slider.valueChanged.connect(self.sliderChange)
		
		#self.spinBox.setDisabled(True)
		self.spinBox.setRange(1,self.t_span)
		self.spinBox.setValue(1)
		self.spinBox.valueChanged.connect(self.spinChange)
		

		
	################################### Layout ###########################################################
		hLabel = QLabel("t")
		hLabel.setDisabled(True)
		
		GridLayout = QGridLayout()
		HBoxLayout_top = QHBoxLayout()
		HBoxLayout_bottom = QHBoxLayout()
		
		
		HBoxLayout_bottom.addWidget(self.spinBox)
		HBoxLayout_bottom.addWidget(hLabel)
		HBoxLayout_bottom.addWidget(self.slider)


		GridLayout.addWidget(self.scrollArea,1,0)
		GridLayout.addLayout(HBoxLayout_bottom,2,0)
		
		# window = QWidget()
		# window.setLayout(GridLayout)
		# self.setCentralWidget(window)
		
		# self.setWindowTitle('OASIS 0.1')
		self.setLayout(GridLayout)
		self.show()
		
####################################### Loading the Image data ####################################
	def getImagePath(self, CH):
		if CH == 0:
			path = self.path +"Image\\Original\\Image" + str(self.t) + ". Ch1 BF.tif"
		if CH == 1:
			path = self.path +"Image\\Original\\Image" + str(self.t) + ". Ch2 488.tif"
		if CH == 2:
			path = self.path +"Image\\Original\\Image" + str(self.t) + ". Ch3 Dapi.tif"
		if CH == 3:
			path = self.path +"Image\\Original\\Image" + str(self.t) + ". Ch4 644.tif"
		
		return path
	
	def getLabelImagePath(self, CH):
		path = self.path + "B" + str(self.BID).zfill(3) +"/label_img/imgR"+str(self.row)+"C"+str(self.col)+"CH"+str(CH)+"label/imgR"+str(self.row)+"C"+str(self.col)+"CH"+str(CH)+"label_t"+str(self.t)+".tif"
		return path
		

		
	def loadImages(self):
		
		# temporary modification for time change, update later
		self.object_selected = 0
		self.CH1_label = []
		self.CH1_CCP_label = []
		self.CH1_pixmap = QPixmap(1024,1024)
		self.CH2_label = []
		
		
		if str(self.t) in self.CH0_dict.keys():
			self.CH0 = self.CH0_dict[str(self.t)]
		else:
			try:
				self.CH0_dict[str(self.t)] = QImage(self.getImagePath(0))
				#print self.getImagePath(0)
			except:
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH0_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH0 = self.CH0_dict[str(self.t)]
		
		if str(self.t) in self.CH1_dict.keys():
			self.CH1 = self.CH1_dict[str(self.t)]
		else:
			try:
				self.CH1_dict[str(self.t)] = QImage(self.getImagePath(1))
				
			except:
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH1_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH1 = self.CH1_dict[str(self.t)]
		
		if str(self.t) in self.CH2_dict.keys():
			self.CH2 = self.CH2_dict[str(self.t)]
		else:
			try:
				self.CH2_dict[str(self.t)] = QImage(self.getImagePath(2))
				
			except:
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH2_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH2 = self.CH2_dict[str(self.t)]
		
		
		if str(self.t) in self.CH3_dict.keys():
			self.CH3 = self.CH3_dict[str(self.t)]
		else:
			try:
				self.CH3_dict[str(self.t)] = QImage(self.getImagePath(3))
				
			except:
				temp = np.zeros([self.Width, self.Height], dtype = np.uint8)
				self.CH3_dict[str(self.t)] = QC.numpy2qimage(temp)
			self.CH3 = self.CH3_dict[str(self.t)]

		if str(self.t) in self.CH1_label_dict.keys():
			self.CH1_label = self.CH1_label_dict[str(self.t)]
		else:
			try:
				CH1_label = sitk.ReadImage(self.getLabelImagePath(1))
				self.CH1_label_dict[str(self.t)] = sitk.GetArrayFromImage(CH1_label)
				
			except:
				self.CH1_label_dict[str(self.t)] = np.zeros([self.Width, self.Height], dtype = np.uint16)
			self.CH1_label = self.CH1_label_dict[str(self.t)]
		
		if str(self.t) in self.CH2_label_dict.keys():
			self.CH2_label = self.CH2_label_dict[str(self.t)]
		else:
			try:
				CH2_label = sitk.ReadImage(self.getLabelImagePath(2))
				self.CH2_label_dict[str(self.t)] = sitk.GetArrayFromImage(CH2_label)
				
			except:
				self.CH2_label_dict[str(self.t)] = np.zeros([self.Width, self.Height], dtype = np.uint16)
			self.CH2_label = self.CH2_label_dict[str(self.t)]

	############################################# GUI Action Setup ############################################ 
	def refreshImages(self):
		pic = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
		pic.fill(qRgb(0,0,0))
		painter = QPainter(pic)
		painter.setCompositionMode(QPainter.CompositionMode_Plus)
		
		if self.Display_Flags['CH0'] == True:
			channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			channelImage.fill(qRgb(255,255,255))
			channelImage.setAlphaChannel(self.CH0)
			painter.drawImage(0,0,channelImage)
		
		if self.Display_Flags['CH1'] == True:
			channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			channelImage.fill(qRgb(18,255,0))
			channelImage.setAlphaChannel(self.CH1)
			painter.drawImage(0,0,channelImage)
		
		if self.Display_Flags['CH2'] == True:
			channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			channelImage.fill(qRgb(0,107,255))
			channelImage.setAlphaChannel(self.CH2)
			painter.drawImage(0,0,channelImage)
			
		if self.Display_Flags['CH3'] == True:
			channelImage = QImage(self.Width, self.Height, QImage.Format_ARGB32_Premultiplied)
			channelImage.fill(qRgb(255,137,0))
			channelImage.setAlphaChannel(self.CH3)
			painter.drawImage(0,0,channelImage)
		
		pen = QPen(Qt.magenta)
		painter.setPen(pen)
		if self.Display_Flags['CH1_label'] == True:
			try:
				# for i in range(1,1023):
					# for j in range(1,1023):
						# v = self.CH1_label[i][j]
						# if v >0:
							# v1 = self.CH1_label[i][j+1]
							# v2 = self.CH1_label[i+1][j]
							# v3 = self.CH1_label[i][j-1]
							# v4 = self.CH1_label[i-1][j]
							# if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
								# painter.drawPoint(j,i)
				painter.drawPixmap(0,0,self.CH1_pixmap)
			except:
				print "No cell segmentation yet!"

		pen.setColor(Qt.yellow)
		painter.setPen(pen)
		if self.Display_Flags['CH2_label'] == True:
			try:
				for blob in self.CH2_label:
					y,x,r = blob
					center = QPoint(x,y)
					painter.drawEllipse(center,r,r)
			except:
				print "No Nucleus Detected!"
				
		####### paint the selected object outline with crosspair
		if self.object_selected != 0:
			# pen.setColor(Qt.cyan)
			# painter.setPen(pen)
			# try:
				# for i in range(1,1023):
					# for j in range(1,1023):
						# v = self.CH1_label[i][j]
						# if v == self.object_selected:
							# v1 = self.CH1_label[i][j+1]
							# v2 = self.CH1_label[i+1][j]
							# v3 = self.CH1_label[i][j-1]
							# v4 = self.CH1_label[i-1][j]
							# if (v!=v1 or v!=v2 or v!=v3 or v!=v4):
								# painter.drawPoint(j,i)
			# except:
				# print "No Cell Selected! "
			pen.setColor(Qt.white)
			painter.setPen(pen)
			y = self.cell_feature_table[self.object_selected-1][1]
			x = self.cell_feature_table[self.object_selected-1][2]
			painter.drawLine(x,0,x,1023)
			painter.drawLine(0,y,1023,y)
			
		del pen
		del painter
		
		self.imageLabel.setPixmap(QPixmap.fromImage(pic))
		
		
	def refreshLabelImage(self):
		print "To be finished ..."

	# From here, most of the functions are event handler or slots
	def spinChange(self):
		self.slider.setValue(self.spinBox.value())

	
	def sliderChange(self):
		self.spinBox.setValue(self.slider.value())
		self.t = self.slider.value()
		self.object_selected = 0
		self.loadImages()
		self.refreshImages()
		
	def keyPressEvent(self, e):
		if (e.key()>=Qt.Key_0 and e.key()<=Qt.Key_9):
			num = e.key() - 0x30
			
			if num == 0:
				self.Display_Flags['CH0'] = not self.Display_Flags['CH0']
			if num == 1:
				self.Display_Flags['CH1'] = not self.Display_Flags['CH1']
			if num == 2:
				self.Display_Flags['CH2'] = not self.Display_Flags['CH2']
			if num == 3:
				self.Display_Flags['CH3'] = not self.Display_Flags['CH3']
			if num == 4:
				self.Display_Flags['CH1_label'] = not self.Display_Flags['CH1_label']
			if num == 5:
				self.Display_Flags['CH2_label'] = not self.Display_Flags['CH2_label']
		self.refreshImages()
		
	# def mousePressEvent (self, QMouseEvent):
		# print QMouseEvent.pos()
	
	def object_selection_func(self, event):
		x = event.pos().x()
		y = event.pos().y()
		print "x = " + str(x) + "y = " + str(y)
		cell_ID = self.CH1_CCP_label[y][x]
		if cell_ID != 0:
			self.emit(SIGNAL("OASIS_Display_Selection"), cell_ID)
			self.object_selected = cell_ID
			self.refreshImages()

	def object_selection_slot(self, cell_ID):
		if cell_ID != 0:
			self.object_selected = cell_ID
			self.refreshImages()
			
	def show_centroid_Dapi(self):
		print "To be finished ..."
	
	def show_crosspair_Dapi(self):
		print "To be finished ..."
		
	def highlight_nucleus(self):
		print "To be finished ..."
		
	def show_centroid_Cell(self):
		print "To be finished ..."
		
	def show_crosspair_Cell(self):
		print "To be finished ..."
		
	def highlight_Cell(self):
		print "To be finished ..."
	
	
	######################################### Image Segmentation and Feature Calculation########################
	def nuclei_segmentation(self):
		print "To be finished ..."
		
	def nuclei_feature_calc(self):
		print "To be finished"
		
	def cell_segmentation(self):
		print "To be finished ..."
		
	def cell_feature_calc(self):
		print "To be finished ..."
		
	def nuclei_allocator(self):
		print "To be finished ..."
		
	def osteoclast_summary(self):
		print "To be finished ..."
		
	
def main():
	app = QApplication(sys.argv)
	
	cube = OASIS_Display()
	
	sys.exit(app.exec_())
	
	
if __name__ == '__main__':
	main()