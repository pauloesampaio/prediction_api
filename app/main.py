from fastapi import FastAPI, HTTPException
import orjson
from utils.io_utils import download_image, yaml_loader
from utils.model_utils import predict
from tensorflow.keras.models import load_model


try:
    config = yaml_loader("./config/config.yml")
    model = load_model(config["paths"]["model_path"])
except IOError as e:
    errno, strerror = e.args
    print("Error loading config or model({0}): {1}".format(errno, strerror))

app = FastAPI()


@app.get("/")
def check_api():
    return {"API status": "Up and running!"}


@app.get("/predict/")
async def get_prediction(url: str):
    try:
        image = download_image(url)
        predictions = predict(model, image, config)
        predictions = orjson.loads(
            orjson.dumps(predictions, option=orjson.OPT_SERIALIZE_NUMPY)
        )
    except IOError:
        predictions = None
        raise HTTPException(status_code=300, detail="Download error")
    response = {"url": url, "predictions": predictions}

    return response
