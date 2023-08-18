#imports
from sklearn.metrics import accuracy_score
from helpers import supervised_training
from helpers import parse_zip 
from helpers import visualizer

def transform_data(data):
    x = data.iloc[:,1:len(data)]
    x.drop('NPHI', inplace=True, axis=1)
    x.drop('LITHOLOGY FACIES_XUEPING', inplace=True, axis=1)
    swap_list = ['GR', 'PE', 'DEN', 'AC']
    x = x.reindex(columns=swap_list)
    return x

def predict(x, model, data):
     y_pred = model.predict(x)
     accuracy = accuracy_score(data['LITHOLOGY FACIES_XUEPING'], y_pred)
     print("Accuracy: %.2f%%" % (accuracy * 100.0))
     return y_pred


def main():
    model = supervised_training.get_knn_model('models/knn_model.sav')
    data = parse_zip.get_data('../../data/102060503903W400_log.las', 53)
    x_train = transform_data(data)
    result = predict(x_train, model, data)
    visualizer.main(data, result)
    
		
    print(result)
    

if __name__ == "__main__":
	main()