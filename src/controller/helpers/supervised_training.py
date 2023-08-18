#imports
import numpy as np
from helpers import parse_zip
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_score
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import joblib 

def knn_train(data):
  facies = np.loadtxt('../../data/100163203803W400_Lithology_Facies.las', skiprows=48)
  #facies = pd.DataFrame(facies, columns=['DEPTH', 'Lithology'])
  for face in facies:
    if (face[1] == -999.25):
        face[1] = 0

  data['Lithology'] = facies[:, 1]
  print(data)
  x = data.iloc[:,1:6]
  x.drop('NPHI', inplace=True, axis=1)  

  pipe = make_pipeline(StandardScaler(), KNN(n_neighbors=5))

  # Define stratified sampling CV 
  cv = StratifiedKFold(10, shuffle=True)

  # Cross-validation
  cv_scores = cross_val_score(pipe, x, data['Lithology'], cv=cv, scoring='accuracy')
  mean_cv_scores = np.mean(cv_scores)
  print('Accuracy mean from 10-fold CV:', mean_cv_scores)

  # Fit model to training data
  pipe.fit(x, data['Lithology'])

  # Predict facies on training data
  y_pred = pipe.predict(x)

  #save model
  filename = 'models/knn_model.sav'
  joblib.dump(pipe, filename)

def get_knn_model(filename):
  return joblib.load(filename)

def xgboost_train(data):
  X = data.iloc[:,1:7]
  X.drop('NPHI', inplace=True, axis=1)
  X.drop('LITHOLOGY FACIES_XUEPING', inplace=True, axis=1)
  X.head(10)

  Y = data.iloc[:, 5]
  Y[Y == 3] = 0
  Y[Y == 4] = 1
  Y[Y == 6] = 2
  Y[Y == 7] = 3
  Y[Y == 8] = 4

  X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42) 
  model = XGBClassifier(n_estimators=100, max_depth=10, booster='gbtree',
                        objective='multi:softprob', learning_rate=0.1, random_state=0,
                        subsample=0.9, colsample_bytree=0.9,
                        eval_metric='mlogloss', reg_lambda=1500)
  model.fit(X_train, Y_train)
  filename = 'models/xgboost_model.sav'
  joblib.dump(model, filename)

def get_xgboost_model(filename):
  return joblib.load(filename)

def main():
   data_knn = parse_zip.get_data('../../data/100163203803W400.las', 52)
   data_xgboost = parse_zip.get_data('../../data/100163203803W400_LOG.las', 53)
   knn_train(data_knn)
   xgboost_train(data_xgboost)

  


if __name__ == "__main__":
	main()


