from flask import Flask, request, jsonify
import torch
from datetime import datetime
import os
import numpy as np
from db import db, init_db, add_model_result, add_midog_result, get_all_model_results, get_all_midog_results, get_midog_results_by_image

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
init_db(app)

# Placeholder for model loading and processing functions
def load_model(model_path):
    return torch.load(model_path)

def save_model(model, model_path):
    torch.save(model, model_path)

def result_40hpf(x_coordinate, y_coordinate):
    # Placeholder function for 40hpf transformation
    return x_coordinate + 1, y_coordinate + 1

# Placeholder for machine learning model
class Model:
    def __init__(self):
        self.model = None
        self.version = "initial"

    def load(self, path):
        self.model = load_model(path)
        self.version = os.path.basename(path)

    def save(self, path):
        save_model(self.model, path)
        self.version = os.path.basename(path)

    def predict(self, x, y):
        # Implement your prediction logic here
        return np.random.choice(['yes', 'maybe', 'no'])

    def train(self, data):
        # Implement your training logic here
        print(f"Training model with {len(data)} samples")

model = Model()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    id = data.get('id')
    password = data.get('password')
    # Implement your authentication logic here
    return jsonify({
        'Id': id,
        'model_general': 'mitoseek_model_general',
        'model_personal': 'mitoseek_model_personal'
    })

@app.route('/<id>/model_general', methods=['POST'])
def model_general(id):
    data = request.json
    model_gen = data.get('model_gen')
    # Implement logic to fetch and return the general model
    return jsonify({
        'model_gen': 'model.pt'
    })

@app.route('/<id>/model_personal', methods=['POST'])
def model_personal(id):
    data = request.json
    model_per = data.get('model_per')
    # Implement logic to fetch and return personal models
    return jsonify({
        'model_gen_ver_1': 'model_personal_2407221739.pt',
        'model_gen_ver_2': 'model_personal_2407191439.pt'
    })

@app.route('/<id>/model_result', methods=['POST'])
def model_result(id):
    data = request.json
    x_coordinates = data.get('x_coordinates', [])
    y_coordinates = data.get('y_coordinates', [])
    image_id = data.get('image_id')
    
    results = []
    for x, y in zip(x_coordinates, y_coordinates):
        x_40hpf, y_40hpf = result_40hpf(x, y)
        label = model.predict(x_40hpf, y_40hpf)
        confidence = np.random.random()  # Replace with actual confidence calculation
        
        # Add results to both databases
        add_model_result(x_40hpf, y_40hpf, label, model.version)
        add_midog_result(image_id, x_40hpf, y_40hpf, label, confidence)
        
        results.append({
            'x_coordinate': x_40hpf,
            'y_coordinate': y_40hpf,
            'label': label,
            'confidence': confidence
        })
    
    # Retrain the model with all data from both databases
    all_data_main = get_all_model_results()
    all_data_midog = get_all_midog_results()
    
    combined_data = [(result.x_coordinate, result.y_coordinate, result.label) for result in all_data_main]
    combined_data.extend([(result.x_coordinate, result.y_coordinate, result.classification) for result in all_data_midog])
    
    model.train(combined_data)
    
    # Save the updated model
    new_model_path = f"model_personal_{datetime.now().strftime('%y%m%d%H%M')}.pt"
    model.save(new_model_path)
    
    return jsonify({
        'results': results,
        'new_model_path': new_model_path
    })

@app.route('/<id>/model_learning', methods=['POST'])
def model_learning(id):
    data = request.json
    model_path = data.get('model_per_learning')
    
    model.load(model_path)
    
    # Retrain the model with all data from both databases
    all_data_main = get_all_model_results()
    all_data_midog = get_all_midog_results()
    
    combined_data = [(result.x_coordinate, result.y_coordinate, result.label) for result in all_data_main]
    combined_data.extend([(result.x_coordinate, result.y_coordinate, result.classification) for result in all_data_midog])
    
    model.train(combined_data)
    
    new_model_path = f"model_personal_{datetime.now().strftime('%y%m%d%H%M')}.pt"
    model.save(new_model_path)
    
    return jsonify({
        'model_gen_update': os.path.basename(new_model_path)
    })

@app.route('/query_midog', methods=['GET'])
def query_midog():
    image_id = request.args.get('image_id')
    results = get_midog_results_by_image(image_id)
    
    return jsonify({
        'results': [{
            'x_coordinate': result.x_coordinate,
            'y_coordinate': result.y_coordinate,
            'classification': result.classification,
            'confidence': result.confidence
        } for result in results]
    })

if __name__ == '__main__':
    app.run(debug=True)