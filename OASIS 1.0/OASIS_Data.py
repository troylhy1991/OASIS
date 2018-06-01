import sys,os
import cv2

#Part 0: Specify Path
src_path = "C:\\LAB\\Osteoclast\\Osteoclast_Data\\12122016\\" ## Change Source Path
dst_path = "C:\\LAB\\Osteoclast\\Osteoclast_Data\\Set2\\" ## Change destination Path

#Part 1: Make Directory
Image = dst_path + "Image\\"
Feature = dst_path + "Feature\\"
Auxilliary = dst_path + "Auxilliary\\"
Original = Image + "Original\\"
Crispy = Image + "Crispy\\"

os.mkdir(dst_path)
os.mkdir(Image)
os.mkdir(Feature)
os.mkdir(Auxilliary)
os.mkdir(Original)
os.mkdir(Crispy)

#Part 2: Load Images and Convert the data
file_list = os.listdir(src_path)
for file in file_list:
	full_path = src_path + file
	full_path_out = Original + file
	image = cv2.imread(full_path)
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imwrite(full_path_out,gray_image)