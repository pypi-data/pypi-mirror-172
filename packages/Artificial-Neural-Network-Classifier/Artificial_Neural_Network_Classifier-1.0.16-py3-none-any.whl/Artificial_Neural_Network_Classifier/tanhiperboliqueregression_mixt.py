import numpy as np
from numpy.linalg import inv
import math
from .tanhiperboliqueregression import tanhiperboliqueregression as Thr
from .tanhiperboliqueregression_dec import tanhiperboliqueregression_dec as Thr_D

class tanhiperboliqueregression_mixt :
    

    def __init__(self,training_data_X, training_data_Y) :
        
        self.training_data_X = training_data_X # The training data x => features numpy_matrix
        self.training_data_Y = training_data_Y # The training data y => response numpy_matrix
        self.THR = Thr(self.training_data_X,self.training_data_Y)
        self.THR_D = Thr_D(self.training_data_X,self.training_data_Y)

    def predict(self,x):
        r = self.THR.predict(x) + self.THR_D.predict(x)
        return r

if __name__ == "__main__" :
  x = np.matrix([[1,3],[2,4],[4,1],[3,1],[4,2] ])
  y = np.matrix([[0],[0],[1],[0],[0] ] )
  THM = tanhiperboliqueregression_mixt(x,y)
  x_ = np.matrix([[4,1]])
  print(THM.predict(x_))
