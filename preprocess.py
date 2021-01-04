import pandas as pd

#loading csv as dataframe
df = pd.read_csv('weekly_in_situ_co2_mlo.csv', 
                 skiprows = 44, names=['date','level'])
			 
n_weeks = len(df) #total weeks of data we have
df.date = pd.to_datetime(df.date) #column values to datetime objects

import matplotlib.pyplot as plt

#plotting all original data
plt.figure(figsize=(20,10))
plt.plot(df.date, df.level)
plt.ylabel('CO2 Levels (ppm)')
plt.xlabel('Time')
plt.show()

import datetime

#selecting the present day (latest) datapoint
present = df.date.iloc[-1]

#adding datapoints to hold future values, until end of the year 2060
#2089 weeks more as of coding this, ref: https://www.weeksuntil.com/date/2060/december/31
for i in range(3199, 5288):
  new_row = {'date': df.date[i-1] + datetime.timedelta(days=7), 'level':None}
  df = df.append(new_row, ignore_index=True) 

#taking the first datapoint
start = df.date[0]

#take integer values of the days from start
df['days'] = (df.date - start).dt.days

import numpy as np
def plot_model(func, nthWeek):
	'''
	Plot the model generated samples overlayed original data
	'''
	plt.figure(figsize=(20, 10))
	plt.plot(df.date[:nthWeek], df.level[:nthWeek], label = 'Original')
	plt.plot(df.date[:nthWeek], func[:nthWeek], label = 'Model')
	plt.title('Model')
	plt.xlabel('Time')
	plt.ylabel('CO2 (ppm)')
	plt.legend()
	plt.show()

from scipy import signal
def plot_acf(x):
    '''
    Plot the autocorrelation function for a series x. This corresponds to the
    acf() function in R. The series x is detrended by subtracting the mean of
    the series before computing the autocorrelation.
    '''
    plt.acorr(x, maxlags=20, 
              detrend=lambda x: signal.detrend(x, type='constant'))

import seaborn as sns
def pair_plot_model(samples, parameters):
	'''
	Generate pair plots for stan model parameters
	'''
	df1 = pd.DataFrame(data = np.transpose([samples[param] for param in parameters]), columns = parameters)
	sns.pairplot(df1, height = 2.5, plot_kws = {'marker': '.', 'alpha': 0.2})
	plt.show()