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

def get_class(group):
	classes = [row[-1] for row in group]
	return max(classes,key=group.count)

def split_tree(root,min_rows,max_depth,depth):
	left,right = root['group']
	del(root['group'])
	if not left or not right:
		terminal = get_class(left+right)
		root['left']=root['right']=terminal
		return 
	
	if depth>=max_depth:
		root['left']=get_class(left)
		root['right']=get_class(right)
		return 

	if len(left)<min_rows:
		root['left']=get_class(left)
	else:
		root['left']=get_split(left)
		split_tree(root['left'],min_rows,max_depth,depth+1)

	if len(right)<min_rows:
		root['right']=get_class(right)
	else:
		root['right']=get_split(right)
		split_tree(root['right'],min_rows,max_depth,depth+1)

def make_tree(data,min_rows,max_depth):
	root = get_split(data)
	split_tree(root,min_rows,max_depth,1)
	return root


def print_tree(node, depth=0):
	if isinstance(node, dict):
		print('%s[X%d < %.3f]' % ((depth*' ', (node['index']+1), node['value'])))
		print_tree(node['left'], depth+1)
		print_tree(node['right'], depth+1)
	else:
		print('%s[%s]' % ((depth*' ', node)))
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
tree = make_tree(dataset, 1, 3)
print_tree(tree)
"""



























