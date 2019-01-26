import psycopg2
from dateutil import parser

def connect_to_database():
	DATABASE_CONN_INFO = "dbname='DICOM_Database' user='postgres' host='localhost' password='18Jan1997'"

	try:
		#connect to postgreSQL server and return the connection object
	    return psycopg2.connect(DATABASE_CONN_INFO)

	except(Exception) as error:
	    print("Unable to connect to database")
	    print(error)


def create_tables(conn): 
	commands = (
			"""
			CREATE TABLE patient_series (
				study_description VARCHAR(255) NOT NULL,
				series_description VARCHAR(255) NOT NULL,
				date_time timestamp NOT NULL,
				PRIMARY KEY (study_description, series_description, date_time, series_instance_UID),
				study_instance_UID VARCHAR(255) NOT NULL,
				series_instance_UID VARCHAR(900) NOT NULL
			)
			""",
			"""
			CREATE TABLE protocol_parameters (
				study_description VARCHAR(255) NOT NULL,
				series_description VARCHAR(255) NOT NULL,
				date_time timestamp NOT NULL,
				series_instance_UID VARCHAR(255) NOT NULL,
				FOREIGN KEY (study_description, series_description, date_time, series_instance_UID)
					REFERENCES patient_series (study_description, series_description, date_time, series_instance_UID)
					ON UPDATE CASCADE ON DELETE CASCADE,
				PRIMARY KEY (study_description, series_description, date_time, series_instance_UID),
				slice_thickness DECIMAL,
				repetition_time DECIMAL,
				echo_time DECIMAL,
				number_of_averages DECIMAL,
				percent_sampling DECIMAL,
				pixel_bandwidth DECIMAL,
				rows INTEGER,
				columns INTEGER,
				inversion_time DECIMAL,
				spacing_between_slices DECIMAL,
				number_of_phase_encoding_steps INTEGER,
				echo_train_length INTEGER,  
				percent_phase_field_of_view DECIMAL,
				transmit_coil_name VARCHAR(255),
				flip_angle DECIMAL,
				plane_phase_encoding_direction VARCHAR(255)
			)
			""")

	cur = conn.cursor()
	
	try:
		#create table one by one using commands defined earlier
	    for command in commands:
	    	print(command)
	    	cur.execute(command)
	    
	    #close communication ith PostgreSQL server	
	    cur.close()
	    #commit changes to database
	    conn.commit()
	    #close connection with server
	    conn.close()
	    print("Created and uploaded all tables successfully")
	except (Exception, psycopg2.DatabaseError) as error:
	    print("All tables not created")
	    print(error)

def add_dicom_data_to_db(conn, dicom_image, cur):
	
	#insert into tables from dicom object
	try:
		if (not dataAlreadyInDB(cur, dicom_image)):

			#insert into patient_series table from dicom object
			cur.execute("""INSERT INTO patient_series VALUES (%s, %s, %s, %s, %s)""", (dicom_image.StudyDescription, dicom_image.SeriesDescription, checkDateTimeValidity(dicom_image), str(dicom_image.StudyInstanceUID), str(dicom_image.SeriesInstanceUID)))
			conn.commit()
			
			#insert into protocol_parameters table from dicom object
			cur.execute("""INSERT INTO protocol_parameters VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (dicom_image.StudyDescription, dicom_image.SeriesDescription, checkDateTimeValidity(dicom_image), dicom_image.SeriesInstanceUID, checkSliceThicknessValididty(dicom_image), checkRepetitionTimeValididty(dicom_image), checkEchoTimeValididty(dicom_image), checkNumberOfAveragesValididty(dicom_image), checkPercentSamplingValididty(dicom_image), checkPixelBandwidthValididty(dicom_image), checkRowsValididty(dicom_image), checkColumnsValididty(dicom_image), checkInversionTimeValididty(dicom_image), checkSpacingBetweenSlicesValididty(dicom_image), checkNumberOfPhaseEncodingStepsValididty(dicom_image), checkEchoTrainLengthValididty(dicom_image), checkPercentPhaseFieldOfViewValididty(dicom_image), checkTransmitCoilNameValididty(dicom_image), checkFlipAngleValididty(dicom_image), checkInPlanePhaseEncodingDirectionValididty(dicom_image)))
			conn.commit()

	except(Exception) as error:
		print error

#---------------------------------------------------------------------------------------Testing-------------------------------------------------------------------------------------#

def testPatientSeriesTable(dicom_image):
	print dicom_image.StudyDescription
	print dicom_image.SeriesDescription
	print dicom_image.StudyDate
	print checkAcquisitionTimeValidity(dicom_image)
	print ""

def testProtocolParamatersTable(dicom_image):
	print "study description: " + dicom_image.StudyDescription
	print "series description: " + dicom_image.SeriesDescription
	print "study date: " + dicom_image.StudyDate
	print "acquisition time: " + checkAcquisitionTimeValidity(dicom_image)
	print checkSliceThicknessValididty(dicom_image)
	print checkRepetitionTimeValididty(dicom_image)
	print checkEchoTimeValididty(dicom_image)
	print checkNumberOfAveragesValididty(dicom_image)
	print checkPercentSamplingValididty(dicom_image)
	print checkPixelBandwidthValididty(dicom_image)
	print checkRowsValididty(dicom_image)
	print checkColumnsValididty(dicom_image)
	print checkInversionTimeValididty(dicom_image)
	print checkSpacingBetweenSlicesValididty(dicom_image)
	print checkNumberOfPhaseEncodingStepsValididty(dicom_image)
	print checkEchoTrainLengthValididty(dicom_image)
	print checkPercentPhaseFieldOfViewValididty(dicom_image)
	print checkTransmitCoilNameValididty(dicom_image)
	print checkFlipAngleValididty(dicom_image)
	print checkInPlanePhaseEncodingDirectionValididty(dicom_image)
	print ""

#------------------------------------------------------------------parameter validity checks for table protocol_parameters-----------------------------------------------------------#

def checkDateTimeValidity(dicom_image):
	try:
		date = dicom_image.StudyDate
		time = dicom_image.AcquisitionTime

		return parser.parse(date + " " +time)
	except:
		return parser.parse("20110110" + " " + "123040")

def checkSliceThicknessValididty(dicom_image):
	try:
		return float(dicom_image.SliceThickness)
	except:
		return None

def checkRepetitionTimeValididty(dicom_image):
	try:
		return float(dicom_image.RepetitionTime)
	except:
		return None

def checkEchoTimeValididty(dicom_image):
	try:
		return float(dicom_image.EchoTime)
	except:
		return None

def checkNumberOfAveragesValididty(dicom_image):
	try:
		return float(dicom_image.NumberOfAverages)
	except:
		return None

def checkPercentSamplingValididty(dicom_image):
	try:
		return float(dicom_image.PercentSampling)
	except:
		return None

def checkPixelBandwidthValididty(dicom_image):
	try:
		return float(dicom_image.PixelBandwidth)
	except:
		return None

def checkRowsValididty(dicom_image):
	try:
		return dicom_image.Rows
	except:
		return None

def checkColumnsValididty(dicom_image):
	try:
		return dicom_image.Columns
	except:
		return None

def checkInversionTimeValididty(dicom_image):
	try:
		return float(dicom_image.InversionTime)
	except:
		return None

def checkSpacingBetweenSlicesValididty(dicom_image):
	try:
		return float(dicom_image.SpacingBetweenSlices)
	except:
		return None

def checkNumberOfPhaseEncodingStepsValididty(dicom_image):
	try:
		return dicom_image.NumberOfPhaseEncodingSteps
	except:
		return None

def checkEchoTrainLengthValididty(dicom_image):
	try:
		return dicom_image.EchoTrainLength
	except:
		return None

def checkPercentPhaseFieldOfViewValididty(dicom_image):
	try:
		return float(dicom_image.PercentPhaseFieldOfView)
	except:
		return None

def checkTransmitCoilNameValididty(dicom_image):
	try:
		return dicom_image.TransmitCoilName
	except:
		return None

def checkFlipAngleValididty(dicom_image):
	try:
		return float(dicom_image.FlipAngle)
	except:
		return None

def checkInPlanePhaseEncodingDirectionValididty(dicom_image):
	try:
		return dicom_image.InPlanePhaseEncodingDirection
	except:
		return None

#-------------------------------------------------------------------------------------------Other Functions-------------------------------------------------------------------------------#

def dataAlreadyInDB(cur, dicom_image):
	redundantDataQuery = """SELECT EXISTS(SELECT 1 FROM patient_series WHERE series_instance_UID = %s)""" % ("""'""" + str(dicom_image.SeriesInstanceUID) + """'""")
	FIRST_ELEMENT_OF_QUERY = 0

	cur.execute(redundantDataQuery)

	return  cur.fetchone()[FIRST_ELEMENT_OF_QUERY]


if __name__ == '__main__':
	#run this file if need to create database
	databaseConnection = connect_to_database()
	create_tables(databaseConnection)