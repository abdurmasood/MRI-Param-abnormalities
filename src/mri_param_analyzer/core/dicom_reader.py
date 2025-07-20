import pydicom as dicom
import glob
import re
from .database import connect_to_database, add_dicom_data_to_db

DICOM_DATA_START_DIR = "Test_DICOM_Data"
START_PATH = "/home/rafey/Programming/Python/projects/KURF/" + DICOM_DATA_START_DIR	#path where DICOM data is present

def main():
	"""Main function for processing DICOM files."""
				
	#----------------------------------functions----------------------------------#

	#load DICOM data at specified path
	def loadDICOM(path):
		return dicom.dcmread(path)

	#return all the possible image file paths
	def allImagePaths(path):
		return glob.glob(path + "/*/*/*")

	#use regex to extract part of the complete path
	def segmentCompleteImagePath(path):
		return re.findall(DICOM_DATA_START_DIR + ".*", path)	

	#------------------------------------main-------------------------------------#

	dbConnection = connect_to_database()
	cur = dbConnection.cursor()

	"""
	get paths for all DICOM files from directory 'START_PATH' one by one
	and load the dicom files so that they can then be added to the 
	database
	"""
	for complete_image_path in allImagePaths(START_PATH):
		match = segmentCompleteImagePath(complete_image_path)
		for load_image_path in match:
			try:
				current_DICOM = loadDICOM(load_image_path)
				add_dicom_data_to_db(dbConnection, current_DICOM, cur)	#loads data object onto database
				
			except (Exception) as error:
				print(error)

	dbConnection.close()


if __name__ == '__main__':
	main()


	#-------------------------------------testing----------------------------------#