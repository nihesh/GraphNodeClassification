# Author : Nihesh Anderson
# File   : inference.py
# Date 	 : 23 March, 2020

ROOT = "./embeddings_32.pkl"
LABELS = "../data/group-edges.csv"
SPLIT = 0.8							# Train : Test ratio

import random
import torch
import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

def ResetWorkspace():

	random.seed(0)
	np.random.seed(0)
	torch.manual_seed(0)
	torch.backends.cudnn.deterministic = True
	torch.backends.cudnn.benchmark = False

def ReadData(root):

	file = open(root, "rb")
	data = pickle.load(file)[0]
	file.close()
	print(data.shape)
	return data

def ReadLabels(root):

	file = open(root, "r")
	data = []

	num_samples = 0
	for line in file:
		line = line.split(",")
		num_samples = max(num_samples, int(line[0]))
		data.append(line)

	labels = [-1 for i in range(num_samples)]
	for line in data:
		labels[int(line[0]) - 1] = int(line[1]) - 1

	return np.asarray(labels)

if(__name__ == "__main__"):

	ResetWorkspace()

	data = ReadData(ROOT)
	labels = ReadLabels(LABELS)

	num_samples = len(data)
	idx = [i for i in range(num_samples)]
	np.random.shuffle(idx)

	train = idx[:int(num_samples * SPLIT)]
	test = idx[int(num_samples * SPLIT):]

	train_label = labels[train]
	test_label = labels[test]

	train_data = data[train]
	test_data = data[test]

	print(train_data.shape)
	print(test_data.shape)

	model = SVC(C = 1.0, kernel = "linear")
	model.fit(train_data, train_label)

	train_prediction = model.predict(train_data)
	test_prediction = model.predict(test_data)
	print("Train macro: {train_acc}".format(
			train_acc = f1_score(train_label, train_prediction, average = "macro",labels=np.unique(train_prediction))
		))
	print("Test macro: {test_acc}".format(
			test_acc = f1_score(test_label, test_prediction, average = "macro",labels=np.unique(test_prediction))
		))
	print("Train micro: {train_acc}".format(
			train_acc = f1_score(train_label, train_prediction, average = "micro",labels=np.unique(train_prediction))
		))
	print("Test micro: {test_acc}".format(
			test_acc = f1_score(test_label, test_prediction, average = "micro",labels=np.unique(test_prediction))
		))
