#imports
from controller.helpers import supervised_training
from controller.helpers import parse_zip 
from controller.helpers import visualizer
import sys

def transform_data(data):
    x = data.iloc[:,1:len(data)]

def predict(x, model):
     y_pred = model.predict(x)


def main(file):
    print(file)
    model = supervised_training.get_xgboost_model('controller/models/xgboost_model.sav')
    data, x_train = parse_zip.get_data(file)
    result = predict(x_train, model)
    visualizer.main(data, result)
    

if __name__ == "__main__":
    main(sys.argv[1:])  