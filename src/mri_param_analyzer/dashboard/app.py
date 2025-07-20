import dash as dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from ..utils.data_formatter import createDataFrameFromDB
from datetime import datetime as dt
import dash_table_experiments as dte
import pandas as pd
import numpy as np


app = dash.Dash()

df = createDataFrameFromDB()
df['year'] = df['date_time'].apply(lambda x: x.strftime('%Y'))

header = html.H1(
	children = 'DICOM Parameter Visualization',
	style={
		'textAlign':'center',
	}
)

dropDownStudyDescription = dcc.Dropdown(
	id='drop_down_studyd',
	options=[
		{'label':studyD , 'value':studyD} for studyD in df['study_description'].unique()
	],
	placeholder='Select Study Description',
)

dropDownSeriesDescription = dcc.Dropdown(
	id='drop_down_seriesd',
	options=[
		{'label':seriesD , 'value':seriesD} for seriesD in df['series_description'].unique()
	],
	placeholder='Select Series Description'
)

checkboxStatistics = dcc.Checklist(
	id='checkboxStatistics',
	options = [
		{'label':'Mean', 'value':'mean'},
		{'label':'Bounds', 'value':'bounds'}
	],
	values= [],
	labelStyle={'display': 'inline-block'}
)

datePickRange = dcc.DatePickerRange(
    id='date-picker-range',
    start_date=df['year'].min(),
    end_date=df['year'].max(),
    stay_open_on_select = True,
    number_of_months_shown = 2,
    end_date_placeholder_text='Select a date!'
)

dateYearSlider = dcc.RangeSlider(
    id='year-slider',
    marks={int(year): int(year) for year in df['year'].unique()},
    min=int(df['year'].min()),
    max=int(df['year'].max()),
    value=[int(df['year'].min()), int(df['year'].max())]
)

#{'label':'Repetition Time', 'value':'RT'},
#{'label':'Number of Phase Encoding Steps', 'value':'NPES'},
dropDownParam = dcc.Dropdown(
	id='drop_down_param',
	options=[
		{'label':'Slice Thickness', 'value':'slice_thickness'},
		{'label':'Echo Time', 'value':'echo_time'},
		{'label':'Number of Averages', 'value':'number_of_averages'},
		{'label':'Percent Sampling', 'value':'percent_sampling'},
		{'label':'Pixel Bandwidth', 'value':'pixel_bandwidth'},
		{'label':'Rows', 'value':'rows'},
		{'label':'Columns', 'value':'columns'},
		{'label':'Inversion Time', 'value':'inversion_time'},
		{'label':'Spacing Between Slices', 'value':'spacing_between_slices'},
		{'label':'Echo Train Length', 'value':'echo_train_length'},
		{'label':'Percent Phase of Field View', 'value':'percent_phase_field_of_view'},
		{'label':'Flip Angle', 'value':'flip_angle'}
	],
	placeholder="Select DICOM Parameter(s)",
	multi=True
)

#initial table data generation in the form of a dataframe
def createNewDataFrameForTable():
	paramName = np.array(['Slice Thickness', 'Echo Time', 'Number of Averages', 'Percent Sampling', 'Pixel Bandwidth', 'Rows', 'Columns', 'Inversion Time', 'Spacing Between Slices', 'Echo Train Length', 'Percent Phase of Field View', 'Flip Angle'])
	modalValues = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
	numberOfUniqueValues = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
	allValuesChanged = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
	percentChange = np.array([0,0,0,0,0,0,0,0,0,0,0,0])
	percentAbnormalValues = np.array([0,0,0,0,0,0,0,0,0,0,0,0])

	matrix = np.column_stack((paramName, modalValues, numberOfUniqueValues, allValuesChanged, percentChange, percentAbnormalValues))
	
	return pd.DataFrame(matrix , columns = ['Parameter Name', 'Modal Value', 'Number of Unique Values', 'Total Values', '% Values Unique', '% Values Abnormal'])

paramInfoTable = dte.DataTable(
	id='parameter-table',
	rows = createNewDataFrameForTable().to_dict('records'),
	sortable=True,
	editable=False,
	columns=['Parameter Name', 'Modal Value', 'Number of Unique Values', 'Total Values', '% Values Unique', '% Values Abnormal']
)

def findEquivilantParamName(tagName):
	if (tagName == 'slice_thickness'):
		return 'Slice Thickness'
	elif (tagName == 'echo_time'):
		return 'Echo Time'
	elif (tagName == 'number_of_averages'):
		return 'Number of Averages'
	elif (tagName == 'percent_sampling'):
		return 'Percent Sampling'
	elif (tagName == 'pixel_bandwidth'):
		return 'Pixel Bandwidth'
	elif (tagName == 'rows'):
		return 'Rows'
	elif (tagName == 'columns'):
		return 'Columns'
	elif (tagName == 'inversion_time'):
		return 'Inversion Time'
	elif (tagName == 'spacing_between_slices'):
		return 'Spacing Between Slices'
	elif (tagName == 'echo_train_length'):
		return 'Echo Train Length'
	elif (tagName == 'percent_phase_field_of_view'):
		return 'Percent Phase Field of View'
	elif (tagName == 'flip_angle'):
		return 'Flip Angle'

app.layout = html.Div([
	
	header,
	
	html.Div(
		dropDownStudyDescription,	
		style={
			'padding':7
		}
	),
	
	html.Div(
		dropDownSeriesDescription,	
		style={
			'padding':7
		}
	),	

	html.Div(
		dropDownParam,	
		style={
			'padding':7
		}
	),	

	html.Div(
		checkboxStatistics,
		style={
			'textAlign':'center',
			'padding':7
		}
	),

	html.Div(dcc.Graph(id='parameter_scatterplot')),

	html.Div(
		dateYearSlider,
		style={
			'padding':20
		}
	),

	html.Div(
		datePickRange,
		style={
			'padding':15
		}
	),

	html.Div(children=[
		html.H2('Other Parameter Information for Selected Dates'),
		paramInfoTable
	])
])

def calculatePercentChange(valueChanged, valueTotal):
	return round(float(valueChanged)/float(valueTotal) * 100, 1)

def findNumberOfAbnormalValues(param, df):
	valCount=0

	ub = calculateUpperBound(param, df)[0]
	lb = calculateLowerBound(param, df)[0]

	for val in df[param]:
		if ((val > ub) or (val < lb)):
			valCount+=1

	return valCount
def calculatePercentAbnormality(abnormalValueCount, valueTotal):
	return round(float(abnormalValueCount)/float(valueTotal) * 100, 1)

#dynamically update table
@app.callback(
	Output('parameter-table', 'rows'),
	[Input('date-picker-range', 'start_date'), 
	Input('date-picker-range', 'end_date'),
	Input('drop_down_studyd', 'value'),
	Input('drop_down_seriesd', 'value')])
def update_table(startYear, endYear, studyD, seriesD):
	paramNames = ['slice_thickness', 'echo_time', 'number_of_averages', 'percent_sampling', 'pixel_bandwidth', 'rows', 'columns', 'inversion_time', 'spacing_between_slices', 'echo_train_length', 'percent_phase_field_of_view', 'flip_angle']
	modalValues = []
	numberOfUniqueValues = []
	finalValuesTotal = []
	percentChange = []
	percentAbnormalValues = []

	dfBtwStartAndEndDate = df[(df.year >= startYear) & (df.year <= endYear) & (df.study_description == studyD) & (df.series_description == seriesD)]

	for param in paramNames:
		paramModalValue = dfBtwStartAndEndDate[param].mode()[0]
		valueChanged = len(dfBtwStartAndEndDate[param].unique())
		valueTotal = len(dfBtwStartAndEndDate[param])
		abnormalValueCount = findNumberOfAbnormalValues(param, dfBtwStartAndEndDate)

		modalValues.append(paramModalValue)
		numberOfUniqueValues.append(valueChanged)
		finalValuesTotal.append(valueTotal)
		percentChange.append(calculatePercentChange(valueChanged, valueTotal))
		percentAbnormalValues.append(calculatePercentAbnormality(abnormalValueCount, valueTotal))

	matrix = np.column_stack((paramNames, modalValues, numberOfUniqueValues, finalValuesTotal, percentChange, percentAbnormalValues))
	finalDF = pd.DataFrame(matrix , columns = ['Parameter Name', 'Modal Value', 'Number of Unique Values', 'Total Values', '% Values Unique', '% Values Abnormal'])

	return finalDF.to_dict('records')

#dynamically update figure
@app.callback(
	Output('parameter_scatterplot', 'figure'),
	[Input('drop_down_studyd', 'value'),
	Input('drop_down_seriesd', 'value'), 
	Input('drop_down_param', 'value'), 
	Input('checkboxStatistics', 'values'), 
	Input('date-picker-range', 'start_date'), 
	Input('date-picker-range', 'end_date')])
def update_figure(studyDescription, seriesDescription, params, selectedCheckboxes, selectedStartDate, selectedEndDate):
	traces = []
	filteredDF = df[(df.study_description == studyDescription) & (df.series_description == seriesDescription) & (df.year >= selectedStartDate) & (df.year <= selectedEndDate)]
	for param in params:
		traces.append(
			go.Scatter(
				x = filteredDF['date_time'],
				y = filteredDF[param],
				mode = 'markers',
				opacity = 0.7,
				marker = {
					'size': 15,
                	'line': {'width': 0.5, 'color': 'white'}
				},
				showlegend = True,
				name = findEquivilantParamName(param)
			)
		)

	for param in params:
		for checkbox in selectedCheckboxes:
			if (checkbox == 'mean'):
				traces.append(
					go.Scatter(
						x = filteredDF['date_time'],
						y = calculateParamMean(param, filteredDF),
						mode = 'lines',
						line = go.Line(color="#005B96"),
						showlegend = False,
						text = "Mean of " + findEquivilantParamName(param),
						hoverinfo = "y+text"
					)
				)
			elif (checkbox == 'bounds'):
				traces.append(
					go.Scatter(
						x = filteredDF['date_time'],
						y = calculateUpperBound(param, filteredDF),
						mode = 'lines',
						line = go.Line(color="#00C3FF"),
						showlegend = False,
						text = "Upper Bound of " + findEquivilantParamName(param),
						hoverinfo = "y+text"
					)
				)

				traces.append(
					go.Scatter(
						x = filteredDF['date_time'],
						y = calculateLowerBound(param, filteredDF),
						mode = 'lines',
						line = go.Line(color="#00C3FF"),
						showlegend = False,
						text = "Lower Bound of " + findEquivilantParamName(param),
						hoverinfo = "y+text"
					)
				)

	return {
		'data': traces,
		'layout': go.Layout(
            xaxis = {'title': 'Time Stamp'},
            yaxis = {'title': 'Parameter Value'},
            legend = {'x': 0, 'y': 1},
            hovermode = 'closest'
        ),
	}

#dynamically update series description according to study
@app.callback(
	Output('drop_down_seriesd', 'options'),
	[Input('drop_down_studyd', 'value')])
def update_series_description_dropdown_from_study_description(chosenStudyDescription):
	filteredStudyDF = df[df.study_description == chosenStudyDescription]
	return [{'label': newSeries, 'value': newSeries} for newSeries in filteredStudyDF['series_description'].unique()]

#update date picker start date from slider value
@app.callback(
	Output('date-picker-range', 'start_date'),
	[Input('year-slider', 'value')])
def updateStartDate(startAndEndYear):
	return str(startAndEndYear[0])

#update date picker end date from slider value
@app.callback(
	Output('date-picker-range', 'end_date'),
	[Input('year-slider', 'value')])
def updateEndDate(startAndEndYear):
	return str(startAndEndYear[1])

def calculateParamMean(param, df):
	mean = []
	for i in df[param]:
		mean.append(df[param].mean())

	return mean

def calculateUpperBound(param, df):
	ub = []
	
	mean = df[param].mean()
	std = df[param].std()
	upperbound = mean + (std/2)

	for i in df[param]:
		ub.append(upperbound)

	return ub

def calculateLowerBound(param, df):
	lb = []
	
	mean = df[param].mean()
	std = df[param].std()
	lowerbound = mean - (std/2)

	for i in df[param]:
		lb.append(lowerbound)

	return lb

def main():
	"""Main function to run the dashboard."""
	app.run_server(debug=True)


if __name__ == '__main__':
	main()