import numpy as np


def predict(model, image, config):
    """Prediction function, to not only predict but also to decode
    prediction into human friendly labels

    Args:
        model (keras.Model): Trained keras model
        image (PIL.Image): Image in PIL format
        config (dict): Configuration dictionary with key to decode predictions

    Returns:
        dict: Dictionary with predictions and probabilities
    """
    input_shape = config["model"]["input_shape"]
    model_input = np.array(image.resize(input_shape))
    model_input = model_input.reshape([1] + input_shape + [3])
    prediction = model.predict(model_input)
    prediction_dictionary = {}

    for i, encoder in enumerate(config["model"]["target_encoder"].keys()):
        labels = config["model"]["target_encoder"][encoder]
        probabilities = prediction[i][0]
        prediction_dictionary[encoder] = dict(zip(labels, probabilities))
    return prediction_dictionary
