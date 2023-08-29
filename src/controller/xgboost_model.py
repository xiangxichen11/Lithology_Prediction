#imports
from sklearn.metrics import accuracy_score
from helpers import supervised_training
from helpers import parse_zip 
from helpers import visualizer

def transform_data(data):
    x = data.iloc[:,1:len(data)]
    #print(type(x))
    #y_result = data.iloc[:, 5]
    #y_result[y_result == 3] = 0
    #y_result[y_result == 4] = 1
    #y_result[y_result == 6] = 2
    #y_result[y_result == 7] = 3
    #y_result[y_result == 8] = 4
    return x

def predict(x, model):
     #print(type(x))
     y_pred = model.predict(x)
     #accuracy = accuracy_score(y, y_pred)
     #print("Accuracy: %.2f%%" % (accuracy * 100.0))
     return y_pred


def main():
    model = supervised_training.get_xgboost_model('models/xgboost_model.sav')
    data, x_train = parse_zip.get_data('../../data/102060503903W400_log.las')
    result = predict(x_train, model)
    visualizer.main(data, result)
    
		
    print(result)
    

if __name__ == "__main__":
	main()