import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import tensorflow as tf
# from keras.preprocessing.image import img_to_array
from tensorflow.keras.utils import img_to_array
from keras.models import load_model
import cv2


model = load_model('fruit_model.h5')


def preprocess_image(img):
    
    img_array = cv2.resize(img, (100, 100)).reshape(-1, 100, 100, 3)/255
    return img_array


def predict_image(model, img):
    # Save the image to disk
    img.save('temp.jpg')
    # Read the image from disk using cv2.imread()
    img = cv2.imread('temp.jpg')
    preprocessed_image = preprocess_image(img)
    predictions = model.predict(preprocessed_image)
    predicted_class = np.argmax(predictions[0])
    confidence = round(100 * (np.max(predictions[0])), 2)
    # Delete the temporary file
    os.remove('temp.jpg')
    return predicted_class, confidence


app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": 200,
        "data": {
            "health": "status ok",
        },
        "msg": "Health Check Successful"
    })

@app.route('/predict', methods=['POST'])
def predict():
    # Get the image from the request
    img = request.files['image']

    # The prediction classes available
    classes = ['Apple Braeburn', 'Apricot', 'Kiwi', 'Orange']

    # Make a prediction on the image
    predicted_class, confidence = predict_image(model, img)

    # Convert the predicted_class to a regular Python integer
    predicted_class = int(predicted_class)

    # Return the prediction result as JSON
    return jsonify({
        "status": 200,
        "data": {
            'predicted_class': classes[predicted_class],
            'confidence': confidence
        },
        "msg": "Prediction successful"
    })


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
