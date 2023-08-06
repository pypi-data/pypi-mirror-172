import numpy as np
from .linearregression import linearregression as LR
from .logisticregession import logisticregression as Lgr
from .lineardiscriminantanalysis import lineardiscriminantananlysis as Lda
from .tanhiperboliqueregression import tanhiperboliqueregression as Thr
from .softmaxregression import softmaxregression as sftmax
from .tanhiperboliqueregression_mixt import tanhiperboliqueregression_mixt as THRM
from .tanhiperboliqueregression_dec import tanhiperboliqueregression_dec as THD

class artificialneuralnetwork_classifier :


  def __init__ (self,training_data_X, training_data_Y) :

    def apply_classification ():
      k = 0
      for i in self.training_data_X :
        for j in i :
          if k == 0 :
            zi = np.matrix([[ THR.predict(j), LGR.predict(j), THd.predict(j), THM.predict(j) ]])
          else :
            zi = np.insert(zi , 0 , np.matrix([[THR.predict(j), LGR.predict(j), THd.predict(j), THM.predict(j)  ]]) , axis=0)
          k += 1
      zi = np.flip(zi,0)
      P = Lgr(zi,self.training_data_Y)
      return P



    pading = np.ones(training_data_X.shape[0])
    #self.training_data_X = np.insert(training_data_X, 0, pading, axis=1) # The training data x => features numpy_matrix
    self.training_data_X = training_data_X
    self.training_data_Y = training_data_Y # The training data y => response numpy_matrix
    LGR = Lgr(self.training_data_X,self.training_data_Y)
    THR = Thr(self.training_data_X,self.training_data_Y)
    THd = THD(self.training_data_X,self.training_data_Y)
    THM = THRM(self.training_data_X,self.training_data_Y)
    PF = apply_classification ()
    self.THR = THR
    self.LGR = LGR
    self.THM = THM
    self.THd = THd
    self.PF = PF

  def predict(self,x):
    zi = np.matrix([[ self.THR.predict(x), self.LGR.predict(x), self.THd.predict(x), self.THM.predict(x) ]])
    return self.PF.predict(zi)




if __name__ == "__main__" :
  def pre_x(x):
      x_ = np.matrix( x )
      print(x_ , "--->" , Ann.predict(x_))
  df = pd.read_csv('admission_data.csv')
  df = df.apply(pd.to_numeric, errors='coerce')
  df = df.dropna()
  x = np.matrix(df[["GRE Score","TOEFL Score","University Rating","SOP","LOR ","CGPA"]].to_numpy() )
  y = np.matrix(df[["Research"]].to_numpy())
  Ann = artificialneuralnetwork_classifier(x,y)
  pre_x([[318,110,3,4,3,8.8] ])
  pre_x([[321,110,3,3.5,5,8.85] ])
  pre_x([[324,112,4,4,2.5,8.1] ])
