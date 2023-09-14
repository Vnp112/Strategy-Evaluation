import numpy as np
import pandas as pd
import matplotlib as plt
import pdb
from numpy import random
class RTLearner(object):

    def __init__(self, leaf_size, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose

    def add_evidence(self, data_x, data_y):
        #combine data_x and data_y into one matrix since build_tree takes one matrix parameter
        data_y = np.array([data_y])
        data = np.concatenate((data_x, data_y.T), axis = 1)
        self.tree = self.build_tree(data)


    def author(self):
        return "vpatel436"


    def query(self, points):
        predictions = []
        for i in points:
            predictions.append(self.predict_y_val(i))
        return np.asarray(predictions)



    def predict_y_val(self, points):
        #go through each node of DTree, and return predicted y val for x test point

        row = 0
        column = self.tree[int(row)] #get values of row 0
        while column[0] != -1: #check if first val of row 0 is a leaf
            if points[int(column[0])] <= column[1]: #check if point is less than split val of tree's row 0
                row += int(column[2]) #left tree
            else:
                row += int(column[3]) #right tree
            column = self.tree[int(row)]
        return column[1]



    def get_highest_index(self, data_x, data_y): #function to get highest coefficinent index
        factor_coef = [] #store all our coefficients for each x data column, then find the greatest coefficient value
        for i in range(data_x.shape[1]): #go through every x column data
            coefficient = np.absolute(np.corrcoef(data_x[:,i], data_y)[0,1]) #get abs val of coefficients for each x factor
            factor_coef.append(coefficient)
        highest_coef = np.nanmax(factor_coef)
        highest_index = factor_coef.index(highest_coef)
        return highest_index

    def build_tree(self, data):  # each column in data is a factor, very last column is the y labels
        labels = data[:, data.shape[1] - 1]  # gets last column and stores it
        row_count = data.shape[0]  # gets # of rows
        factors = data[:, :data.shape[1] - 1]
        same_y_val = (labels[0] == labels).all()  # compare first y row val with every other y row val
        if row_count <= self.leaf_size:  # check to see if theres only 1 row of data, then return the leaf
            return np.array([[-1, np.mean(labels), np.nan, np.nan]])  # return	[leaf,	data.y,	NA,	NA]
        elif same_y_val:
            return np.array([[-1, np.mean(labels), np.nan, np.nan]])  # return	[leaf,	data.y,	NA,	NA]
        else:
            rand_factor = random.randint(factors.shape[1])  # get index for random factor
            row1 = random.randint(row_count)  # get random row
            row2 = random.randint(row_count)  # get another random row
            while row1 == row2:  # check to see if both rows selected are the same, and change row2 if necessary
                row2 = random.randint(row_count)
            splitval = (factors[row1][rand_factor] + factors[row2][rand_factor]) / 2
            if splitval == max(data[:, rand_factor]):  # check to see if right sub tree is empty
                return np.array([[-1, np.mean(labels), np.nan, np.nan]])
            lefttree = self.build_tree(data[data[:, rand_factor] <= splitval])
            righttree = self.build_tree(data[data[:, rand_factor] > splitval])
            root = np.array([[rand_factor, splitval, 1, lefttree.shape[0] + 1]])
            # DTree = np.vstack([root, lefttree, righttree]) #create tree variable to store all nodes and leaves
            return np.vstack((root, lefttree, righttree))

if __name__ == "__main__":
    print("the secret clue is 'zzyzx'")
