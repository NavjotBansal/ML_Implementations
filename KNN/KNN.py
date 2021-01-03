import pandas as pd
from csv import reader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import math
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import time
#import finished

def read_csv(filename):
	dataset = list()
	with open(filename,'r') as file:
		csv_reader = reader(file)
		for rows in csv_reader:
			dataset.append(rows)
	return dataset

def normalize(df):
	mini,maxi=df.min(),df.max()
	for i in range(df.shape[0]):
		df[i] = (df[i]-mini)/(maxi-mini)
	return df

data = pd.read_csv('iris.csv',header=None)
for i in range(data.shape[1]-1):
	data[i] = normalize(data[i])

le = LabelEncoder()
data[4] = le.fit_transform(data[4])
print(data.info())
print(data.describe())

def distance(dfA,dfB):
	d=0.0
	for i in range(len(dfA)-1):
		d = d + (dfA[i]-dfB[i])**2
	return math.sqrt(d)
"""
print(distance(data.iloc[10],data.iloc[0]))
list = [[1,3.5],[0,1.5],[0,2.5],[1,2.5],[1,4.5]]
list.sort(key=lambda x: x[1])
print(list)
"""
def nearest_neighbour(data,row,ncount):
	dist = list()
	row = row.values.tolist()
	data = data.values.tolist()
	for i in range(len(data)):
		record = data[i]
		d = distance(record,row)
		dist.append((record[-1],d))
#	print(dist)
	dist.sort(key = lambda x:x[1])
#	print(dist)
	req = list()
	for i in range(ncount):
		req.append(dist[i][0])
#	print(req)
	return max(set(req),key=req.count)

"""
print(data)
print(nearest_neighbour(data,data.iloc[134],3))
"""

def predict(train,test,ncount):
	p = list()
	for i in range(test.shape[0]):
		p.append(nearest_neighbour(train,test.iloc[i],ncount))
	p = pd.DataFrame(p)
#	print(confusion_matrix(test[4],p))
	return test[4],p

def analyse(data,seed):
	train,test = train_test_split(data,test_size=0.3,random_state=seed)
	error = list()
	for i in range(1,21):
		expected,actual = predict(train,test,i)
		matrix = confusion_matrix(expected,actual)
		c,w=0.0,0
		for i in range(len(matrix)):
			for j in range(len(matrix)):
				if i==j:
					c = c+matrix[i][i]
				else:
					w = w+matrix[i][j]
		if w!=0:
			c=c/w
		error.append(c)
#	color ="C"+str(seed)
#	plt.scatter([i for i in range(1,len(error)+1)],error,color=color,alpha=0.3)
#	plt.plot([i for i in range(1,len(error)+1)],error,color=color,alpha=0.3)
	return error
def main():
	avg_score = [0.0 for i in range(1,21)]
	for seed in range(1,10):
		error_list = list()
		error_list.append(analyse(data,seed))
		for error in error_list:
			for i in range(len(error)):
				avg_score[i] += error[i]
		for error in error_list:
			color ="C"+str(seed)
			plt.scatter([i for i in range(1,len(error)+1)],error,color=color,alpha=0.3)
			plt.plot([i for i in range(1,len(error)+1)],error,color=color,alpha=0.3)
	plt.show()

	plt.scatter([i for i in range(1,len(avg_score)+1)],avg_score)
	plt.plot([i for i in range(1,len(avg_score)+1)],avg_score)
	plt.show()

if __name__ == "__main__":
	main()
