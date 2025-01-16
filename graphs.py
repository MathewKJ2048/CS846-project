import os
import sys
import ast
import re
import matplotlib.pyplot as plt
import math

LLM_data_path="./out/"
raw_data_path="./corpus/"

data = {}

# key is file_path
# each object has: llmn-prompt, text

ct_e=0
for root, dirs, files in os.walk(LLM_data_path):
	for f in files:
		FP = LLM_data_path+f
		with open(FP) as fi:
			fdataraw = fi.read()
			try:
				fdata = ast.literal_eval(fdataraw)
				fpkey = list(fdata.keys())[0]
				data[fpkey] = {}
				data[fpkey]["output"] = fdata[fpkey]
			except Exception as e:
				print(e)
				ct_e+=1

for f in data:
	with open(f) as fg:
		data[f]["text"]=fg.read()


print(ct_e)
print(len(data))

def get_number(t):
	m = re.search(r"(\d+)",t)
	if m:
		return int(m.group(1))
	return None


models = ["llama3.2","tinyllama"]

numerical_data = {}

for fp in data:
	tem = {}
	for m in models:
		tem[m] = get_number(data[fp]["output"][m])
	tem["length"] = len(data[fp]["text"])
	ans = 0
	m = re.findall(r"\bsig\b",data[fp]["text"])
	if m:
		ans = len(m)
	tem["actual"] = ans
	numerical_data[fp]=tem

# print(numerical_data)


def correctness():
	t1 = 0
	t2 = 0
	diff = 0
	correctness = 0
	c_within_error = 0
	modelid = 0
	num=0
	for f in numerical_data:
		if numerical_data[f][models[modelid]]:
			num+=1
			s1 = numerical_data[f][models[modelid]]
			s2 = numerical_data[f]["actual"]
			if s1==s2:
				correctness+=1
			t1+=s1
			t2+=s2
			
	print(t1/t2)
	print(correctness/num)

def g_0():
	labels = ["illegible","correct","off by 1","off by > 2"]
	def pie(modelid):
		illegible = 0
		correct = 0
		off_1 = 0
		everything_else = 0
		for f in numerical_data:
			if numerical_data[f][models[modelid]]:
				s1 = numerical_data[f][models[modelid]]
				s2 = numerical_data[f]["actual"]
				if s1==s2:
					correct+=1
				elif abs(s1-s2)==1:
					off_1+=1
				else:
					everything_else+=1
			else:
				illegible+=1
		return [illegible,correct,off_1,everything_else]
	for modelid in range(len(models)):
		plt.title("Distribution of responses for: "+str(models[modelid]))
		plt.pie(pie(modelid),labels=labels)
		plt.show()
		print(pie(modelid))



def g1():
	modelid = 0
	CN = 10
	def get_cumulative_correctness(modelid):
		cumulative_correctness = [0]*CN
		num=0
		for f in numerical_data:
			if numerical_data[f][models[modelid]]:
				num+=1
				s1 = numerical_data[f][models[modelid]]
				s2 = numerical_data[f]["actual"]
				for i in range(len(cumulative_correctness)):
					if abs(s1-s2)<=i:
						cumulative_correctness[i]+=1

		cumulative_correctness = [c/num for c in cumulative_correctness]
		return cumulative_correctness

	plt.xlabel("tolerance")
	plt.ylabel("percentage of correct responses among legible answers")
	X = [i for i in range(CN)]
	for modelid in range(len(models)):
		M = models[modelid]
		cumulative_correctness = get_cumulative_correctness(modelid)
		plt.plot(X,cumulative_correctness,label=M)
	plt.legend()
	plt.show()

def g1_5():
	modelid = 0
	CN = 10
	def get_cumulative_correctness(modelid):
		cumulative_correctness = [0]*CN
		num=0
		for f in numerical_data:
			if numerical_data[f][models[modelid]]:
				num+=1
				s1 = numerical_data[f][models[modelid]]
				s2 = numerical_data[f]["actual"]
				for i in range(len(cumulative_correctness)):
					if abs(s1-s2)<=i:
						cumulative_correctness[i]+=1

		cumulative_correctness = [c/len(numerical_data) for c in cumulative_correctness]
		return cumulative_correctness

	plt.xlabel("tolerance")
	plt.ylabel("percentage of correct responses among all answers")
	X = [i for i in range(CN)]
	for modelid in range(len(models)):
		M = models[modelid]
		cumulative_correctness = get_cumulative_correctness(modelid)
		plt.plot(X,cumulative_correctness,label=M)
	plt.legend()
	plt.show()

def g2():
	dist_data = {}
	for n in numerical_data:
		nd = numerical_data[n]
		fgh = str(nd["actual"])
		if fgh not in dist_data:
			dist_data[fgh] = 0
		dist_data[fgh]+=1
	print(dist_data)


def g3(): # probability of correctness, legibility vs length
	SM = 100
	bins = {}
	def bin(l):
		return int(math.log2(l+1))
	for nd in numerical_data:
		datum = numerical_data[nd]
		k = bin(datum["length"])
		if k in bins:
			bins[k]+=1
		else:
			bins[k] = 1
	print(bins)
	data = [numerical_data[nd]["length"] for nd in numerical_data]
	print(len(data))
	data_correct = []
	data_correct_2 = []
	for nd in numerical_data:
		t = numerical_data[nd]
		g = t["length"]
		if t[models[0]] == t["actual"]:
			data_correct.append(g)
		if t[models[1]] == t["actual"]:
			data_correct_2.append(g)

	BINS = [2**i for i in range(15)]
	plotted = [data,data_correct,data_correct_2]#,data_illegible]
	plt.hist(plotted, bins=BINS, label=["total data","correct data - "+models[0],"correct data - "+models[1]])
	plt.yscale('log')
	plt.xscale('log')
	plt.xlabel("length of model")
	plt.ylabel("number of models")
	plt.legend()
	plt.show()

def g3_5(): # probability of correctness, legibility vs length
	SM = 100
	bins = {}
	def bin(l):
		return int(math.log2(l+1))
	for nd in numerical_data:
		datum = numerical_data[nd]
		k = bin(datum["length"])
		if k in bins:
			bins[k]+=1
		else:
			bins[k] = 1
	print(bins)
	data = [numerical_data[nd]["length"] for nd in numerical_data]
	print(len(data))
	data_correct = []
	data_correct_2 = []
	for nd in numerical_data:
		t = numerical_data[nd]
		g = t["length"]
		if t[models[0]]:
			data_correct.append(g)
		if t[models[1]]:
			data_correct_2.append(g)

	BINS = [2**i for i in range(15)]
	plotted = [data,data_correct,data_correct_2]#,data_illegible]
	plt.hist(plotted, bins=BINS, label=["total data","legible data - "+models[0],"legible data - "+models[1]])
	plt.yscale('log')
	plt.xscale('log')
	plt.xlabel("length of model")
	plt.ylabel("number of models")
	plt.legend()
	plt.show()

def g4(): # probability of correctness, legibility vs number
	SM = 100
	bins = {}
	def bin(l):
		return int(math.log2(l+1))
	for nd in numerical_data:
		datum = numerical_data[nd]
		k = bin(datum["length"])
		if k in bins:
			bins[k]+=1
		else:
			bins[k] = 1
	print(bins)
	data = [numerical_data[nd]["actual"] for nd in numerical_data]
	print(len(data))
	data_correct = []
	data_correct_2 = []
	for nd in numerical_data:
		t = numerical_data[nd]
		g = t["actual"]
		if t[models[0]] == g:
			data_correct.append(g)
		if t[models[1]] == g:
			data_correct_2.append(g)

	BINS = [2**i for i in range(10)]
	plotted = [data,data_correct,data_correct_2]#,data_illegible]
	plt.hist(plotted, bins=BINS, label=["total data","correct data - "+models[0],"correct data - "+models[1]])
	plt.yscale('log')
	plt.xscale('log')
	plt.xlabel("length of model")
	plt.ylabel("number of signatures")
	plt.legend()
	plt.show()

def g4_5(): # probability of correctness, legibility vs number
	SM = 100
	bins = {}
	def bin(l):
		return int(math.log2(l+1))
	for nd in numerical_data:
		datum = numerical_data[nd]
		k = bin(datum["length"])
		if k in bins:
			bins[k]+=1
		else:
			bins[k] = 1
	print(bins)
	data = [numerical_data[nd]["actual"] for nd in numerical_data]
	print(len(data))
	data_correct = []
	data_correct_2 = []
	for nd in numerical_data:
		t = numerical_data[nd]
		g = t["actual"]
		if t[models[0]]:
			data_correct.append(g)
		if t[models[1]]:
			data_correct_2.append(g)

	BINS = [2**i for i in range(10)]
	plotted = [data,data_correct,data_correct_2]#,data_illegible]
	plt.hist(plotted, bins=BINS, label=["total data","legible data - "+models[0],"legible data - "+models[1]])
	plt.yscale('log')
	plt.xscale('log')
	plt.xlabel("length of model")
	plt.ylabel("number of signatures")
	plt.legend()
	plt.show()


g4_5()

# correctness()








