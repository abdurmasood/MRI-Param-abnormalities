import pydicom as dicom
import glob
import re
import random
import time
from datetime import datetime

DICOM_DATA_READ_PATH = "/home/rafey/Programming/Python/projects/KURF/Test_DICOM_Data/"	#path where DICOM data is present
DICOM_DATA_WRITE_PATH = "/home/rafey/Programming/Python/projects/KURF/Test_DICOM_Data/Generated-Random-DICOM/"

#load DICOM data at specified path
def loadDICOM(path):
	return dicom.dcmread(path)

def addRandomParamsToDICOM(dicomImage):
	dicomImage.StudyDate = str(random.randint(2000, 2018)) + str(random.randint(10, 12)) + str(random.randint(10, 30))
	dicomImage.AcquisitionTime = str(random.randint(10, 12)) + str(random.randint(10, 60)) + str(random.randint(10, 60))
	dicomImage.SeriesInstanceUID = dicomImage.SeriesInstanceUID + str(random.randint(1, 100))
	dicomImage.SliceThickness = random.randint(1, 150)
	dicomImage.RepetitionTime = random.randint(3000, 5000)
	dicomImage.EchoTime = random.randint(1, 150)
	dicomImage.NumberOfAverages = random.randint(1, 150)
	dicomImage.PercentSampling = random.randint(1, 100)
	dicomImage.PixelBandwidth = random.randint(1, 150)
	dicomImage.Rows = random.randint(1, 15)
	dicomImage.Columns = random.randint(1, 15)
	dicomImage.InversionTime = random.randint(1, 150)
	dicomImage.SpacingBetweenSlices = random.randint(1, 150)
	dicomImage.NumberOfPhaseEncodingSteps = random.randint(1, 100)
	dicomImage.EchoTrainLength = random.randint(1, 150)
	dicomImage.PercentPhaseFieldOfView = random.randint(1, 100)
	dicomImage.TransmitCoilName = "Missing"
	dicomImage.FlipAngle = random.randint(1, 150)
	dicomImage.InPlanePhaseEncodingDirection = "Missing"

def generateFileName(dcm, i):
	return dcm.StudyDescription + dcm.SeriesDescription + "_" + str(i) + ".dcm"

def createAndSaveTestFiles(dcm, i):
	addRandomParamsToDICOM(dcm)
	dcm.save_as(DICOM_DATA_WRITE_PATH + generateFileName(dcm, i))

if __name__ == '__main__':
	try:
		dcm1 = loadDICOM(DICOM_DATA_READ_PATH + "Mri-1/MR2/19665")
		dcm2 = loadDICOM(DICOM_DATA_READ_PATH + "Mri-1/MR4/21409")
		dcm3 = loadDICOM(DICOM_DATA_READ_PATH + "Mri-2/MR3/10496")
		dcm4 = loadDICOM(DICOM_DATA_READ_PATH + "Mri-2/MR6/9174")
		dcm5 = loadDICOM(DICOM_DATA_READ_PATH + "Mri-2/MR7/9835")
		dcm6 = loadDICOM(DICOM_DATA_READ_PATH + "Mri-2/MR2/9143")
		dcm7 = loadDICOM(DICOM_DATA_READ_PATH + "Mri-2/MR4/11217")
		dcm8 = loadDICOM(DICOM_DATA_READ_PATH + "Mri-1/MR3/20658")

		for i in range(0,39):
			createAndSaveTestFiles(dcm1, i)
			createAndSaveTestFiles(dcm2, i)
			createAndSaveTestFiles(dcm3, i)
			createAndSaveTestFiles(dcm4, i)
			createAndSaveTestFiles(dcm5, i)
			createAndSaveTestFiles(dcm6, i)
			createAndSaveTestFiles(dcm7, i)
			createAndSaveTestFiles(dcm8, i)
			
	except (Exception) as error:
		print(error)