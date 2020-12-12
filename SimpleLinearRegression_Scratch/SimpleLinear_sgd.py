import pandas as pd
from csv import reader
from random import randrange
from sklearn import preprocessing
import math
import matplotlib.pyplot as plt
#reading dataset
def read_file(filename):
	dataset = list()
	with open(filename,'r') as file:
		csv_reader = reader(file)
		for rows in csv_reader:
			if not rows:
				continue
			else:
				dataset.append(rows)
	return dataset

#splitting training test dataset
def split_test_train(dataset,splitvalue):
	train = list()
	test = list(dataset)
	traindatacount = len(dataset)*splitvalue
	while len(train) < traindatacount:
		index = randrange(len(test))
		train.append(test.pop(index))
	return train,test

#prediction 
def predict(rows,cooef):
	yhat = cooef[0]
#	print(type(yhat),type(cooef),type(rows))
	for i in range(0,len(rows)-1):
		yhat = yhat + cooef[i+1]*rows[i]
	return yhat

#schotastic gradient descnet 
def sgd(dataset,lr,epoch):
	cooef= [0.0 for i in range(len(dataset[0]))]
	for ep in range(epoch):
		for rows in dataset:
			yhat = predict(rows,cooef)
			error = (rows[-1] - yhat)
			cooef[0]= cooef[0] + (2*lr*error)/len(dataset)
			for i in range(1,len(cooef)):
				cooef[i] = cooef[i] + (2*lr*error*rows[i-1])/len(dataset)
#		print("error in ",ep," epoch is ",(error)**2/len(dataset))
	return cooef

#model training 
def linear_regression_simple(trainset,testset,lr,epoch):
	cooef = sgd(trainset,lr,epoch)
	print(cooef)
	predict_value = []
	for rows in testset:
		predict_value.append(predict(rows,cooef))
	return predict_value
#root means square error
def rmse(predicted,actual):
	error = 0.0
	for i in range(len(actual)):
		error = (predicted[i]-actual[i])**2
	error = error/len(actual)
	return math.sqrt(error)
def main():
	dataset = read_file('salary_data.csv')
	dataset = dataset[1:]	
	row,col = len(dataset),len(dataset[0])
	for i in range(row):
		for j in range(col):
			dataset[i][j] = float(dataset[i][j])

	#data normalization
	dataset_df = pd.DataFrame(dataset)
	x = dataset_df.values #returns a numpy array
	min_max_scaler = preprocessing.MinMaxScaler()
	x_scaled = min_max_scaler.fit_transform(x)
	dataset_df = pd.DataFrame(x_scaled)
	dataset = dataset_df.values.tolist()

	train,test = split_test_train(dataset,0.8)
	predicted = linear_regression_simple(train,test,0.001,10000)
	actual = [row[-1] for row in test]
	print(rmse(predicted,actual))
	plt.plot(actual,'m')
	plt.plot(predicted,'b')
	plt.show()
if __name__ == "__main__":
	main()
