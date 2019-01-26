import pandas as pd
import numpy as np
from dbsetup import connect_to_database
from numpy import nan

def listToArrayConversionDecimal(numpyArr, listIn):
	for subList in listIn:
			numpyArr.append(decimalToFloat(subList[0]))

def listToArrayConversion(numpyArr, listIn):
	for subList in listIn:
			numpyArr.append(noneToNan(subList[0]))

def decimalToFloat(element):
	try:
		return float(element)
	except:
		return nan

def noneToNan(element):
	if (element == None):
		return nan
	else:
		return element
	
"""
get parameters from the database and convert them into arrays 
from the list type they are already in and concatinate them
together to return a matrix of data
"""
def getDataMatrix():
	dbConnection = connect_to_database()
	cur = dbConnection.cursor()

	studyDescriptionArray = []
	seriesDescriptionArray = []
	dateTimeArray = []
	sliceThicknessArray = []
	repetitionTimeArray = []
	echoTimeArray = []
	numberOfAveragesArray = []
	percentSamplingArray = []
	pixelBandwidthArray = []
	rowsArray = []
	columnsArray = []
	inversionTimeArray = []
	spacingBetweenSlicesArray = []
	numberOfPhaseEncodingStepsArray = []
	echoTrainLengthArray = []
	percentPhaseFieldOfViewArray = []
	flipAngleArray = []

	cur.execute("""SELECT study_description FROM protocol_parameters""")
	studyDescriptionList = cur.fetchall()
	listToArrayConversion(studyDescriptionArray, studyDescriptionList)

	cur.execute("""SELECT series_description FROM protocol_parameters""")
	seriesDescriptionList = cur.fetchall()
	listToArrayConversion(seriesDescriptionArray, seriesDescriptionList)

	cur.execute("""SELECT date_time FROM protocol_parameters""")
	dateTimeList = cur.fetchall()
	listToArrayConversion(dateTimeArray, dateTimeList)

	cur.execute("""SELECT slice_thickness FROM protocol_parameters""")
	sliceThicknessList = cur.fetchall()
	listToArrayConversionDecimal(sliceThicknessArray, sliceThicknessList)

	cur.execute("""SELECT repetition_time FROM protocol_parameters""")
	repetitionTimeList = cur.fetchall()
	listToArrayConversionDecimal(repetitionTimeArray, repetitionTimeList)

	cur.execute("""SELECT echo_time FROM protocol_parameters""")
	echoTimeList = cur.fetchall()
	listToArrayConversionDecimal(echoTimeArray, echoTimeList)
	
	cur.execute("""SELECT number_of_averages FROM protocol_parameters""")
	numberOfAveragesList = cur.fetchall()
	listToArrayConversionDecimal(numberOfAveragesArray, numberOfAveragesList)

	cur.execute("""SELECT percent_sampling FROM protocol_parameters""")
	percentSamplingList = cur.fetchall()
	listToArrayConversionDecimal(percentSamplingArray, percentSamplingList)

	cur.execute("""SELECT pixel_bandwidth FROM protocol_parameters""")
	pixelBandwidthList = cur.fetchall()
	listToArrayConversionDecimal(pixelBandwidthArray, pixelBandwidthList)

	cur.execute("""SELECT rows FROM protocol_parameters""")
	rowsList = cur.fetchall()
	listToArrayConversionDecimal(rowsArray, rowsList)

	cur.execute("""SELECT columns FROM protocol_parameters""")
	columnsList = cur.fetchall()
	listToArrayConversionDecimal(columnsArray, columnsList)

	cur.execute("""SELECT inversion_time FROM protocol_parameters""")
	inversionTimeList = cur.fetchall()
	listToArrayConversionDecimal(inversionTimeArray, inversionTimeList)

	cur.execute("""SELECT spacing_between_slices FROM protocol_parameters""")
	spacingBetweenSlicesList = cur.fetchall()
	listToArrayConversionDecimal(spacingBetweenSlicesArray, spacingBetweenSlicesList)

	cur.execute("""SELECT number_of_phase_encoding_steps FROM protocol_parameters""")
	numberOfPhaseEncodingStepsList = cur.fetchall()
	listToArrayConversionDecimal(repetitionTimeArray, repetitionTimeList)

	cur.execute("""SELECT echo_train_length FROM protocol_parameters""")
	echoTrainLengthList = cur.fetchall()
	listToArrayConversionDecimal(echoTrainLengthArray, echoTrainLengthList)

	cur.execute("""SELECT percent_phase_field_of_view FROM protocol_parameters""")
	percentPhaseFieldOfViewList = cur.fetchall()
	listToArrayConversionDecimal(percentPhaseFieldOfViewArray, percentPhaseFieldOfViewList)

	cur.execute("""SELECT flip_angle FROM protocol_parameters""")
	flipAngleList = cur.fetchall()
	listToArrayConversionDecimal(flipAngleArray, flipAngleList)

	cur.close()
	dbConnection.close()

	return np.column_stack((studyDescriptionArray, seriesDescriptionArray, dateTimeArray ,sliceThicknessArray, echoTimeArray, numberOfAveragesArray, percentSamplingArray, pixelBandwidthArray, rowsArray, columnsArray, inversionTimeArray, spacingBetweenSlicesArray, echoTrainLengthArray, percentPhaseFieldOfViewArray, flipAngleArray)) # 'number_of_phase_encoding_steps', 'repetition_time' NOT ADDED BECASUE OF ERROR 'ValueError: all the input array dimensions except for the concatenation axis must match exactly'


def createDataFrameFromDB():
	matrix = getDataMatrix()
	dataFrame = pd.DataFrame(matrix , columns = ['study_description', 'series_description', 'date_time', 'slice_thickness', 'echo_time', 'number_of_averages', 'percent_sampling', 'pixel_bandwidth', 'rows', 'columns', 'inversion_time', 'spacing_between_slices', 'echo_train_length', 'percent_phase_field_of_view', 'flip_angle']) # 'number_of_phase_encoding_steps', 'repetition_time' NOT ADDED BECASUE OF ERROR 'ValueError: all the input array dimensions except for the concatenation axis must match exactly'
	return dataFrame