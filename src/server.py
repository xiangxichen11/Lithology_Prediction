from flask import Flask, render_template, request, send_from_directory
from controller import hierarchical
from controller import kmeans
from controller import knn
from controller import xgboost_model
import os

app = Flask(__name__, template_folder='templates')
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/unsupervised')
def unsupervised():
    image_file = []
    final = []
    return render_template('unsupervised.html', image_file = image_file, final = final)

@app.route('/supervised')
def supervised():
    return render_template('supervised.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('templates', filename)

@app.route('/unsupervised_render', methods=['POST'])
def unsupervised_render():
    if request.method == 'POST':
        unsupervised_type = request.form["user_input"]
        user_file = request.files["file_input"]
        if user_file and unsupervised_type:
            file_path = os.path.join('../data/', user_file.filename)  # Adjust the path
            user_file.save(file_path)
            result = process_class_type(file_path, unsupervised_type)
            return render_template('unsupervised.html',  result = result)
        else:
            return "Please provide both values"
    return render_template('unsupervised.html')

@app.route('/supervised_render', methods=['POST'])
def supervised_render():
    if request.method == 'POST':
        unsupervised_type = request.form["user_input"]
        user_file = request.files["file_input"]
        if user_file and unsupervised_type:
            file_path = os.path.join('../data/', user_file.filename)  # Adjust the path
            user_file.save(file_path)
            result = process_class_type(file_path, unsupervised_type)
            return render_template('supervised.html',  result = result)
        else:
            return "Please provide both values"
    return render_template('supervised.html')

@app.route('/display_images', methods=['GET', 'POST'])
def display_images(): 
    image_files = None
    if request.method == 'POST':
        image_folder = os.path.join(app.root_path, 'templates/images')
        image_files = [f'images/{filename}' for filename in os.listdir(image_folder) if filename.split('.')[0] != 'final']
        return render_template('unsupervised.html', image_files=image_files)
    return render_template('unsupervised.html')
    
@app.route('/display_lithology', methods=['GET,', 'POST'])
def display_lithology():
    if request.method == 'POST':
        image_folder = os.path.join(app.root_path, 'templates/images')
        final = [f'images/{filename}' for filename in os.listdir(image_folder) if filename.split('.')[0] == 'final']
        return render_template('unsupervised.html', final = final)
    return render_template('unsupervised.html')

    
@app.route('/display_supervised', methods=['GET', 'POST'])
def display_supervised():
    if request.method == 'POST':
        image_folder = os.path.join(app.root_path, 'templates/images')
        final = [f'images/{filename}' for filename in os.listdir(image_folder) if filename.split('.')[0] == 'final']
        return render_template('supervised.html', final = final)
    return render_template('supervised.html')

@app.route('/hyperparameter', methods=['GET', 'POST'])
def hyperparameter():
    if request.method == 'POST':
        param = request.form["user_input"]
        result = process_hyperparameter(param)
        return render_template('unsupervised.html', result = result)
    return render_template('unsupervised.html')
    
@app.route('/display_output', methods=['GET', 'POST'])
def display_output():
    if request.method == 'POST':
        print(kmeans.output)
        df = kmeans.output
        html_table = df.to_html(classes='table')
        return render_template('unsupervised.html', table=html_table)
    return render_template('unsupervised.html')
    
# @app.route('/update_classify', methods=['GET', 'POST'])
# def update_classify():
#     if request.method == 'POST':
#         output = []
#         for item in request.form:
#             if item:
#                 output.append(item)
#         process_update_classify(output)

# def process_update_classify(output):
    
def process_class_type(file, input_data):
    remove_images()
    if (input_data == "K-Means"):
        kmeans.main(file)
    elif (input_data == "knn"):
        knn.main(file)
    elif (input_data == "xgboost"):
        xgboost_model.main(file)
    else:
        hierarchical.main(file, input_data)

def remove_images():
    image_folder = os.path.join(app.root_path, 'templates/images')
    for file in os.listdir(image_folder):
        if file.endswith('.png'):
            print(os.path.join(image_folder, file))
            os.remove(os.path.join(image_folder, file))
    


def process_hyperparameter(input_data):
    kmeans.hyperparameter = int(input_data)
    hierarchical.hyperparameter = int(input_data)


if __name__ == '__main__':
    app.run(debug=True, port=5001)