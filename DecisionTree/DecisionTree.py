import math
#imports finished 

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