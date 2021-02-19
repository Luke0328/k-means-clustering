from mpl_toolkits import mplot3d
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 

# import data
data = pd.read_csv('data.csv')
reps = data.iloc[602:605]
data = data[:-5]

zeros = []
for i in range(600):
	zeros.append(0)
data['GroupID'] = zeros

groups = [1,2,3]
reps['GroupID'] = groups

iters = 0
prev = pd.DataFrame()
while not(reps.equals(prev)):
	prev = reps.copy()
	for i in data.index:
		dists = []
		dataX = data['Unnamed: 1'][i]
		dataY = data['Unnamed: 2'][i]
		dataZ = data['Unnamed: 3'][i]

		for l2, r2 in reps.iterrows():
			repX = r2['Unnamed: 1']
			repY = r2['Unnamed: 2']
			repZ = r2['Unnamed: 3']
			# calculate Euclidean distance and append to list
			dists.append(round(np.sqrt(((dataX - repX)** 2) + ((dataY - repY)** 2) + ((dataZ - repZ)** 2)),6))

		# get the index of the smallest distance and assign the correct groupID to the data point
		minpos = dists.index(min(dists)) 
		data.loc[i, 'GroupID'] = minpos + 1

	for j in range(3):
		totalX = 0
		totalY = 0
		totalZ = 0
		extracted = data.loc[(data['GroupID'] == j+1)].copy()

		for label, row in extracted.iterrows():
			totalX += row.loc['Unnamed: 1']
			totalY += row.loc['Unnamed: 2']
			totalZ += row.loc['Unnamed: 3']

		meanX = round(totalX/(len(extracted)),6)
		meanY = round(totalY/(len(extracted)),6)
		meanZ = round(totalZ/(len(extracted)),6)

		# set group reps to mean of all its group members
		reps.loc[j+602, 'Unnamed: 1'] = meanX
		reps.loc[j+602, 'Unnamed: 2'] = meanY
		reps.loc[j+602, 'Unnamed: 3'] = meanZ
	iters += 1
print(iters)


fig = plt.figure() 
ax = plt.axes(projection ='3d') 

x_data = data.loc[:,'Unnamed: 1'].values
y_data = data.loc[:,'Unnamed: 2'].values
z_data = data.loc[:,'Unnamed: 3'].values
colors = data.loc[:, 'GroupID'].values
colors_strings = []

# process colors
for item in colors:
	if item == 1:
		colors_strings.append('c')
	if item == 2:
		colors_strings.append('m')
	if item == 3:
		colors_strings.append('y')

ax.scatter(x_data, y_data, z_data, c=colors_strings, alpha=0.15) 

# original cluster centers
plt.plot(12.8, 14.2, 16.3, marker='o', color="b")
plt.plot(6.62,2.49,13.3, marker='o', color="b")
plt.plot(13.7,10.3,9.31, marker='o', color="b")

#final cluster centers
plt.plot(15.919500,11.091100,16.06950, marker='o', color="g")
plt.plot(2.980406,3.010442,7.16195, marker='o', color="g")
plt.plot(8.800600,14.023000,8.92485, marker='o', color="g")

plt.style.use('seaborn')

plt.show() 