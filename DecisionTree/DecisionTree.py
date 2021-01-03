import math
#imports finished 


# gini_score for impurtiy testing
def gini_score(groups,classes):

	gini =0.0
	total_records = 0.0
	for group in groups:
		total_records +=len(group)
	for group in groups:
		group_size = len(group)
		if(group_size==0):
			continue
		propotional_score=0.0
		for c in classes:
			class_list = list()
			for row in group:
				class_list.append(row[-1])
			p = class_list.count(c)/group_size
			propotional_score += p*p
		gini+= (1 - propotional_score)*(group_size/total_records)
	return gini

"""
print(gini_score([[[1, 1], [1, 0]], [[1, 1], [1, 0]]], [0, 1]))
print(gini_score([[[1, 0], [1, 0]], [[1, 1], [1, 1]]], [0, 1]))
"""

def split_groups(data,index,value):
	left,right = list(),list()
	for rows in data:
		if rows[index]<value:
			left.append(rows)
		else:
			right.append(rows)
	return left,right

def get_split(data):
	class_values = [row[-1] for row in data]
	class_values = list(set(class_values))
	opti_index,opti_value,opti_score,opti_group=999,999,math.inf,None
	for i in range(0,len(data[0])-1):
		for row in data:
			group = split_groups(data,i,row[i])
			gini_impurity = gini_score(group,class_values)
			print('X%d < %.3f Gini=%.3f' % ((i+1), row[i], gini_impurity))
			if gini_impurity < opti_score:
				opti_score = gini_impurity
				opti_index = i
				opti_group = group
				opti_value = row[i]
	return {'index':opti_index,'value':opti_value,'group':opti_group}

"""
dataset = [[2.771244718,1.784783929,0],
	[1.728571309,1.169761413,0],
	[3.678319846,2.81281357,0],
	[3.961043357,2.61995032,0],
	[2.999208922,2.209014212,0],
	[7.497545867,3.162953546,1],
	[9.00220326,3.339047188,1],
	[7.444542326,0.476683375,1],
	[10.12493903,3.234550982,1],
	[6.642287351,3.319983761,1]]
split = get_split(dataset)
print('Split: [X%d < %.3f]' % ((split['index']+1), split['value']))
"""
