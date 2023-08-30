from flask import Flask, render_template, request, send_from_directory
from controller import hierarchical
from controller import kmeans
import os

app = Flask(__name__, template_folder=os.path.join(os.pardir, 'frontend'))

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

@app.route('/page1', methods=['POST'])
def page1():
    if request.method == 'POST':
        unsupervised_type = request.form["user_input"]
        user_file = request.files["file_input"]
        if user_file and unsupervised_type:
            file_path = os.path.join('../data/', user_file.filename)  # Adjust the path
            user_file.save(file_path)
            result = process_unsupervised_type(file_path, unsupervised_type)
            return render_template('unsupervised.html', result = result)
        else:
            return "Please provide both values"

@app.route('/display_images', methods=['GET', 'POST'])
def display_images(): 
    image_files = []
    final = []
    if request.method == 'POST':
        image_folder = os.path.join(os.path.dirname(app.root_path), 'frontend/images')
        image_files = [f'images/{filename}' for filename in os.listdir(image_folder)]
        final = [f'images/{filename}' for filename in os.listdir(image_folder) if filename.split('.')[0] == 'final']
        return render_template('unsupervised.html', image_files=image_files, final = final)

@app.route('/final_output', methods=['GET', 'POST'])
def final_output():
    if request.method == 'POST':
        image_folder = os.path.join(os.path.dirname(app.root_path), 'frontend/images')
        image_files = [f'images/{filename}' for filename in os.listdir(image_folder) if filename.split('.')[0] == 'final']
        print(image_files)
        return render_template('unsupervised.html', image_files=image_files)


@app.route('/hyperparameter', methods=['GET', 'POST'])
def hyperparameter():
    if request.method == 'POST':
        param = request.form["user_input"]
        result = process_hyperparameter(param)
        return render_template('unsupervised.html', result = result)

def process_unsupervised_type(file, input_data):
    if (input_data == "K-Means"):
        kmeans.main(file)
    else:
        hierarchical.main(file, input_data)

def process_hyperparameter(input_data):
	kmeans.hyperparameter = int(input_data)


if __name__ == '__main__':
    app.run(debug=True, port=5001)